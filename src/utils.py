"""
Shared utilities for GDSC-8 challenge.

Pro tip: Keep notebooks for exploration, modules for production code.
This separation makes your code testable, reusable, and maintainable.
"""
import json
import boto3
import requests
from pathlib import Path
from typing import Dict, List, Optional
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


def send_results(
    results: List[Dict], 
    dry_run: bool = False,
    verbose: bool = True
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
        >>> response = send_results(results, dry_run=True)  # Test first!
        >>> response = send_results(results)  # Then submit
    """
    # Always validate first
    validate_submission_format(results)
    
    if dry_run:
        if verbose:
            print("🔍 Dry run mode - validating without submitting")
            print(f"✅ {len(results)} results are valid and ready to submit")
        return None
        
    # Prepare AWS authenticated request
    url = "https://cygeoykm2i.execute-api.us-east-1.amazonaws.com/main/submit"
    session = boto3.Session(region_name='us-east-1')
    credentials = session.get_credentials()
    
    if not credentials:
        raise ValueError("AWS credentials not found. Check your ~/.aws/credentials")
    
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"submission": results})
    
    # Sign request with AWS credentials
    request = AWSRequest(method='POST', url=url, data=payload, headers=headers)
    SigV4Auth(credentials, 'execute-api', 'us-east-1').add_auth(request)
    
    # Send the request (cast to str to satisfy type checker)
    response = requests.request(
        method=str(request.method),
        url=str(request.url),
        headers=dict(request.headers),
        data=request.body,
    )
    
    if verbose:
        if response.status_code == 200:
            print("✅ Submission successful!")
            try:
                msg = response.json().get('message', '')
                if msg:
                    print(f"📝 Server message: {msg}")
            except:
                pass
        else:
            print(f"❌ Submission failed with status: {response.status_code}")
            print(f"Response: {response.text}")
        
    return response


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


def sanity_check() -> bool:
    """
    Verify connection to the challenge API infrastructure.
    
    Returns:
        True if connection successful, False otherwise
    """
    base_url = "https://cygeoykm2i.execute-api.us-east-1.amazonaws.com/main/health"
    
    try:
        # Set up AWS session and credentials
        session = boto3.Session(region_name='us-east-1')
        credentials = session.get_credentials()
        
        if not credentials:
            print("❌ AWS credentials not found")
            return False
            
        headers = {'Content-Type': 'application/json'}
        
        # Create and sign the AWS request
        request = AWSRequest(method='GET', url=base_url, data=None, headers=headers)
        SigV4Auth(credentials, 'execute-api', 'us-east-1').add_auth(request)
        
        # Make the request (cast to str to satisfy type checker)
        response = requests.request(
            method=str(request.method),
            url=str(request.url),
            headers=dict(request.headers),
            data=request.body
        )

        if response.status_code == 200:
            print("✅ API connection successful!")
            return True
        else:
            print(f"❌ API check failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection check failed: {e}")
        return False