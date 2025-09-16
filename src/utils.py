"""
Shared utilities for GDSC-8 challenge.

Pro tip: Keep notebooks for exploration, modules for production code.
This separation makes your code testable, reusable, and maintainable.
"""
import json
import boto3
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


def save_json(path: str | Path, data: Dict | List) -> None:
    """
    Save data to JSON file with proper error handling.

    Args:
        path: Output file path
        data: Data to save (dict or list)

    Example:
        >>> results = [{"persona_id": "p1", "predicted_type": "awareness"}]
        >>> save_json("submission.json", results)
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_json(path: str | Path) -> Dict | List:
    """
    Load JSON data from file.

    Args:
        path: Input file path

    Returns:
        Loaded JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def load_file_content(path: str | Path) -> str:
    """
    Load raw text content from a file.

    Args:
        path: Input file path

    Returns:
        File contents as string
    """
    path = Path(path)
    with path.open('r', encoding='utf-8') as file:
        return file.read()


def aws_signed_request(
    path: str,
    method: str,
    payload: Optional[Any] = None,
    verbose: bool = True,
) -> Optional[requests.Response | bool]:
    """Make a SigV4 signed request to the challenge API.

    Lean error handling: raises RuntimeError on failure.

    Args:
        path: API path segment (e.g. "chat", "submit", "health")
        method: HTTP verb (GET/POST)
        payload: dict / list / JSON-string / None
        verbose: print status messages

    Returns:
        Response object, True (for health success), or None/False on failure
    """
    base_url = "https://cygeoykm2i.execute-api.us-east-1.amazonaws.com/main"

    # Normalize payload into raw JSON string (boto3 signing sends raw body)
    body = None
    if payload is not None:
        try:
            if isinstance(payload, (dict, list)):
                body = json.dumps(payload)
            elif isinstance(payload, (str, bytes)):
                body = payload if isinstance(payload, str) else payload.decode('utf-8')
            else:  # Fallback attempt json serialization
                body = json.dumps(payload)
        except Exception as e:  # pragma: no cover
            msg = f"Failed to serialize payload for path '{path}'"
            if verbose:
                print(f"❌ {msg}\n   ↳ {e}")
            raise RuntimeError(msg) from e

    try:
        session = boto3.Session(region_name='us-east-1')
        credentials = session.get_credentials()
        if not credentials:
            msg = "AWS credentials not found (configure with aws configure)"
            if verbose:
                print(f"❌ {msg}")
            raise RuntimeError(msg)

        headers = {'Content-Type': 'application/json'}
        request = AWSRequest(url=f"{base_url}/{path}", method=method.upper(), data=body, headers=headers)
        SigV4Auth(credentials, 'execute-api', 'us-east-1').add_auth(request)

        try:
            response = requests.request(
                method=str(request.method),
                url=str(request.url),
                headers=dict(request.headers),
                data=request.body,
            )
        except requests.RequestException as e:
            msg = f"Network error during request to '{path}'"
            if verbose:
                print(f"❌ {msg}\n   ↳ {e}")
            raise RuntimeError(msg) from e

        if response.status_code == 200:
            if verbose:
                print("✅ API request successful")
            return response if path != "health" else True

        # Non-200 status handling
        msg = f"API call '{path}' failed: status={response.status_code} body={response.text[:300]}"
        if verbose:
            print(f"❌ {msg}")
        raise RuntimeError(msg)

    except Exception as e:  # pragma: no cover - broad fallback
        msg = f"Unexpected error during signed request to '{path}'"
        if verbose:
            print(f"❌ {msg}\n   ↳ {e}")
        raise RuntimeError(msg) from e


def sanity_check(verbose: bool = True) -> bool:
    """Quick connectivity & credentials check.

    Args:
        verbose: print status
    Returns:
        True if reachable + credentials sign correctly, else False
    """
    try:
        result = aws_signed_request("health", "GET", verbose=verbose)
        return bool(result)
    except Exception:
        return False


def chat_with_persona(
    persona_id: str,
    message: str,
    conversation_id: str | None = None,
    verbose: bool = True,
) -> Optional[Tuple[str, str]]:
    """Send a message to a persona and return (response_text, conversation_id).

    Returns None on failure unless raise_on_error=True.
    """
    payload = {
        "persona_id": persona_id,
        "message": message,
        "conversation_id": conversation_id,
    }
    try:
        resp = aws_signed_request(
            path="chat",
            method="POST",
            payload=payload,
            verbose=verbose,
        )
        if not resp:
            return None
        data = resp.json()
        for key in ("response", "conversation_id"):
            if key not in data:
                raise RuntimeError(f"Chat response missing key '{key}'")
        return data["response"], data["conversation_id"]
    except Exception as e:
        if verbose:
            print(f"❌ Chat failed: {e}")
        return None


def make_submission(
    results: List[Dict],
    dry_run: bool = False,
    verbose: bool = True,
) -> Optional[requests.Response]:
    """
    Submit results to GDSC challenge endpoint.

    Args:
        results: List of predictions in challenge format
        dry_run: If True, validate without submitting
        verbose: If True, print status messages

    Returns:
        API response or None if dry run

    Raises:
        ValueError: If results format is invalid

    Example:
        >>> results = generate_predictions()
        >>> response = make_submission(results, dry_run=True)  # Test first!
        >>> response = make_submission(results)  # Then submit
    """
    # Always validate first
    validate_submission_format(results)

    if dry_run:
        if verbose:
            print("🔍 Dry run mode - validating without submitting")
            print(f"✅ {len(results)} results are valid and ready to submit")
        return None

    try:
        response = aws_signed_request(
            path="submit",
            method="POST",
            payload={"submission": results},
            verbose=verbose,
        )
        if not response:
            return None
        if verbose:
            try:
                response_json = response.json()
                print("✅ Submission successful!")
                if response_json:
                    msg = response_json.get('message')
                    sid = response_json.get('submission_id')
                    if msg:
                        print(f"📝 Server message: {msg}")
                    if sid:
                        print(f"🆔 Submission ID: {sid}")
            except ValueError:
                if verbose:
                    print("⚠️  Submission succeeded but response body was not JSON")
        return response
    except Exception as e:
        if verbose:
            print(f"❌ Submission failed: {e}")
        return None

def fetch_my_submissions(verbose: bool = True) -> Optional[List[Dict]]:
    """
    Fetch my team's submissions from GDSC challenge endpoint.

    Args:
        verbose: If True, print status messages

    Returns:
        API response or None if dry run

    Raises:
        ValueError: If my_submissions format is invalid

    Example:
        >>> my_submissions = fetch_my_submissions()
    """

    try:
        response = aws_signed_request(path="submit", method="GET", verbose=verbose)
        if not response:
            return None
        try:
            return response.json()
        except ValueError as e:
            raise RuntimeError("Failed to parse JSON for submissions list") from e
    except Exception as e:
        if verbose:
            print(f"❌ Fetch submissions failed: {e}")
        return None

def validate_submission_format(results: List[Dict]) -> None:
    """
    Validate submission format before sending.

    Good practice: Always validate before external API calls!

    Args:
        results: List of prediction dictionaries

    Raises:
        ValueError: If format is invalid
    """
    if not results:
        raise ValueError("Results list is empty")

    if len(results) != 100:
        print(f"⚠️  Warning: Expected 100 personas, got {len(results)}")

    required_fields = {'persona_id', 'predicted_type'}
    valid_types = {'jobs+trainings', 'trainings_only', 'awareness'}

    for i, result in enumerate(results):
        # Check required fields
        if not required_fields.issubset(result.keys()):
            missing = required_fields - result.keys()
            raise ValueError(f"Result {i} missing required fields: {missing}")

        # Check predicted_type
        pred_type = result['predicted_type']
        if pred_type not in valid_types:
            raise ValueError(
                f"Result {i} has invalid predicted_type: '{pred_type}'. "
                f"Must be one of: {valid_types}"
            )

        # Type-specific validation
        if pred_type == 'jobs+trainings':
            if 'jobs' not in result:
                raise ValueError(f"Result {i} missing 'jobs' field")
            if not isinstance(result['jobs'], list):
                raise ValueError(f"Result {i} 'jobs' must be a list")
            # Validate job structure
            for job in result['jobs']:
                if not isinstance(job, dict):
                    raise ValueError(f"Result {i} job items must be dictionaries")
                if 'job_id' not in job:
                    raise ValueError(f"Result {i} job missing 'job_id'")
                if 'suggested_trainings' not in job:
                    raise ValueError(f"Result {i} job missing 'suggested_trainings'")

        elif pred_type == 'trainings_only':
            if 'trainings' not in result:
                raise ValueError(f"Result {i} missing 'trainings' field")
            if not isinstance(result['trainings'], list):
                raise ValueError(f"Result {i} 'trainings' must be a list")

        elif pred_type == 'awareness':
            # awareness type can have optional predicted_items
            pass

    print(f"✅ Validated {len(results)} results - format is correct!")


def get_job_paths() -> List[Path]:
    """
    Discover all job description files in the dataset.

    Returns:
        List of Path objects for job files
    """
    data_dir = Path('./data/jobs')
    if not data_dir.exists():
        data_dir = Path('../data/jobs')  # Try parent directory

    if not data_dir.exists():
        raise FileNotFoundError(f"Jobs directory not found. Expected at: {data_dir}")

    paths = sorted([f for f in data_dir.iterdir() if f.suffix == '.md'])
    return paths


def get_training_paths() -> List[Path]:
    """
    Discover all training program files in the dataset.

    Returns:
        List of Path objects for training files
    """
    data_dir = Path('./data/trainings')
    if not data_dir.exists():
        data_dir = Path('../data/trainings')  # Try parent directory

    if not data_dir.exists():
        raise FileNotFoundError(f"Trainings directory not found. Expected at: {data_dir}")

    paths = sorted([f for f in data_dir.iterdir() if f.suffix == '.md'])
    return paths


# Cost tracking utilities for Mistral API usage
MISTRAL_PRICING = {
    'mistral-large-latest': {'input': 2.00, 'output': 6.00},  # per 1M tokens
    'mistral-medium-latest': {'input': 0.40, 'output': 2.00},  # per 1M tokens
    'mistral-small-latest': {'input': 0.10, 'output': 0.30},  # per 1M tokens
}

COST_TRACKER = {
    'api_calls': 0,
    'total_input_tokens': 0,
    'total_output_tokens': 0,
    'estimated_cost': 0.0,
    'by_model': {}
}


def calculate_cost(input_tokens: int, output_tokens: int, model: str = 'mistral-medium-latest') -> float:
    """
    Calculate actual cost based on Mistral's pricing.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model: Mistral model identifier

    Returns:
        Estimated cost in USD
    """
    pricing = MISTRAL_PRICING.get(model, MISTRAL_PRICING['mistral-medium-latest'])
    input_cost = (input_tokens / 1_000_000) * pricing['input']
    output_cost = (output_tokens / 1_000_000) * pricing['output']
    return input_cost + output_cost


def track_api_call(response_or_model=None, input_tokens: int = 0, output_tokens: int = 0, model: str = None) -> float:
    """
    Track costs from Strands agent responses or direct token counts.

    Args:
        response_or_model: Either a response object from Strands agent OR a model string
        input_tokens: Number of input tokens (when passing model as first arg)
        output_tokens: Number of output tokens (when passing model as first arg)
        model: Mistral model identifier (when passing response as first arg)

    Usage:
        # With response object
        track_api_call(response, model='mistral-medium-latest')

        # With token counts
        track_api_call(model='mistral-medium-latest', input_tokens=500, output_tokens=50)

    Returns:
        Cost of this specific API call
    """
    # Handle different call signatures
    if isinstance(response_or_model, str):
        # Called with model as first argument
        model = response_or_model
    elif hasattr(response_or_model, 'metrics') and response_or_model.metrics:
        # Called with response object
        if model is None:
            model = 'mistral-medium-latest'
        input_tokens = response_or_model.metrics.accumulated_usage.get('inputTokens', 0)
        output_tokens = response_or_model.metrics.accumulated_usage.get('outputTokens', 0)
    else:
        # Default case
        if model is None:
            model = 'mistral-medium-latest'

    cost = calculate_cost(input_tokens, output_tokens, model)

    COST_TRACKER['api_calls'] += 1
    COST_TRACKER['total_input_tokens'] += input_tokens
    COST_TRACKER['total_output_tokens'] += output_tokens
    COST_TRACKER['estimated_cost'] += cost

    if model not in COST_TRACKER['by_model']:
        COST_TRACKER['by_model'][model] = {'calls': 0, 'cost': 0.0}
    COST_TRACKER['by_model'][model]['calls'] += 1
    COST_TRACKER['by_model'][model]['cost'] += cost

    return cost


def print_cost_summary():
    """Display running cost summary for API usage."""
    print("💰 Cost Summary:")
    print(f"  Total API calls: {COST_TRACKER['api_calls']}")
    print(f"  Total tokens: {COST_TRACKER['total_input_tokens'] + COST_TRACKER['total_output_tokens']:,}")
    print(f"  Estimated cost: ${COST_TRACKER['estimated_cost']:.4f}")

    if COST_TRACKER['by_model']:
        print("\n  By model:")
        for model, stats in COST_TRACKER['by_model'].items():
            print(f"    {model}: {stats['calls']} calls, ${stats['cost']:.4f}")


def reset_cost_tracker():
    """Reset the cost tracker to zero."""
    global COST_TRACKER
    COST_TRACKER = {
        'api_calls': 0,
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'estimated_cost': 0.0,
        'by_model': {}
    }

