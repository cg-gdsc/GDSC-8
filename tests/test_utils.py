"""
Basic tests for GDSC utilities.

Run with: pytest tests/

Pro tip: Always write tests for your submission logic!
Even in a competition, tests save debugging time.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock, Mock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import src.utils as utils
from src.utils import (
    validate_submission_format,
    save_json,
    read_json,
    load_file_content,
    get_job_paths,
    get_training_paths,
    calculate_cost,
    track_api_call,
    print_cost_summary,
    reset_cost_tracker,
    send_results,
    sanity_check
)


class TestSubmissionValidation:
    """Test submission format validation."""
    
    def test_validate_submission_format_valid(self):
        """Test that valid submissions pass validation."""
        valid_results = [
            {
                "persona_id": "persona_001",
                "predicted_type": "jobs+trainings",
                "jobs": [
                    {
                        "job_id": "job_001", 
                        "suggested_trainings": ["training_001", "training_002"]
                    }
                ]
            },
            {
                "persona_id": "persona_002",
                "predicted_type": "trainings_only",
                "trainings": ["training_001", "training_003"]
            },
            {
                "persona_id": "persona_003",
                "predicted_type": "awareness",
                "predicted_items": "too_young"
            }
        ]
        
        # Should not raise any exception
        validate_submission_format(valid_results)
    
    def test_validate_submission_empty(self):
        """Test that empty submissions are rejected."""
        with pytest.raises(ValueError, match="Results list is empty"):
            validate_submission_format([])
    
    def test_validate_submission_missing_persona_id(self):
        """Test that missing persona_id is caught."""
        invalid = [{"predicted_type": "awareness"}]
        with pytest.raises(ValueError, match="missing required fields.*persona_id"):
            validate_submission_format(invalid)
    
    def test_validate_submission_invalid_type(self):
        """Test that invalid predicted_type is caught."""
        invalid = [
            {
                "persona_id": "persona_001",
                "predicted_type": "invalid_type"
            }
        ]
        with pytest.raises(ValueError, match="invalid predicted_type"):
            validate_submission_format(invalid)
    
    def test_validate_jobs_missing_list(self):
        """Test that jobs+trainings without jobs list is caught."""
        invalid = [
            {
                "persona_id": "persona_001",
                "predicted_type": "jobs+trainings"
                # Missing 'jobs' field
            }
        ]
        with pytest.raises(ValueError, match="missing 'jobs' field"):
            validate_submission_format(invalid)
    
    def test_validate_jobs_invalid_structure(self):
        """Test that invalid job structure is caught."""
        invalid = [
            {
                "persona_id": "persona_001",
                "predicted_type": "jobs+trainings",
                "jobs": [
                    {"job_id": "job_001"}  # Missing suggested_trainings
                ]
            }
        ]
        with pytest.raises(ValueError, match="missing 'suggested_trainings'"):
            validate_submission_format(invalid)
    
    def test_validate_trainings_missing_list(self):
        """Test that trainings_only without trainings list is caught."""
        invalid = [
            {
                "persona_id": "persona_001",
                "predicted_type": "trainings_only"
                # Missing 'trainings' field
            }
        ]
        with pytest.raises(ValueError, match="missing 'trainings' field"):
            validate_submission_format(invalid)


class TestFileIO:
    """Test file I/O operations."""
    
    def test_json_round_trip(self, tmp_path):
        """Test that JSON save/load preserves data."""
        test_data = {
            "test": "data",
            "number": 42,
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }
        
        test_file = tmp_path / "test.json"
        save_json(test_file, test_data)
        loaded = read_json(test_file)
        
        assert loaded == test_data
    
    def test_json_creates_directory(self, tmp_path):
        """Test that save_json creates parent directories."""
        test_file = tmp_path / "subdir" / "another" / "test.json"
        test_data = {"test": "data"}
        
        save_json(test_file, test_data)
        
        assert test_file.exists()
        loaded = read_json(test_file)
        assert loaded == test_data
    
    def test_read_missing_file(self):
        """Test that reading missing file raises proper error."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            read_json("nonexistent_file.json")
    
    def test_load_file_content(self, tmp_path):
        """Test loading text file content."""
        test_file = tmp_path / "test.txt"
        test_content = "This is test content\nWith multiple lines"
        
        test_file.write_text(test_content)
        loaded = load_file_content(test_file)
        
        assert loaded == test_content


class TestSampleSubmissions:
    """Test sample submission generators."""
    
    def test_lazy_submission(self):
        """Test that lazy submission is valid."""
        # This is what Tutorial 3 will create
        results = [
            {
                "persona_id": f"persona_{i:03}",
                "predicted_type": "jobs+trainings",
                "jobs": [
                    {
                        "job_id": "job_001",
                        "suggested_trainings": []
                    }
                ]
            }
            for i in range(1, 101)
        ]
        
        # Should pass validation
        validate_submission_format(results)
        assert len(results) == 100
        assert all(r["predicted_type"] == "jobs+trainings" for r in results)
    
    def test_mixed_submission(self):
        """Test submission with mixed types."""
        results = []
        
        # Some job recommendations
        for i in range(1, 51):
            results.append({
                "persona_id": f"persona_{i:03}",
                "predicted_type": "jobs+trainings",
                "jobs": [{"job_id": f"job_{i:03}", "suggested_trainings": []}]
            })
        
        # Some training only
        for i in range(51, 76):
            results.append({
                "persona_id": f"persona_{i:03}",
                "predicted_type": "trainings_only",
                "trainings": [f"training_{i:03}"]
            })
        
        # Some awareness
        for i in range(76, 101):
            results.append({
                "persona_id": f"persona_{i:03}",
                "predicted_type": "awareness",
                "predicted_items": "too_young"
            })
        
        validate_submission_format(results)
        assert len(results) == 100


# Pro tip: Add tests for your own matching logic!
class TestYourMatcher:
    """Template for testing your custom matcher."""

    @pytest.mark.skip(reason="Implement your own matcher first")
    def test_my_matcher(self):
        """Test your custom matching function."""
        # from src.matchers import my_awesome_matcher
        # results = my_awesome_matcher()
        # validate_submission_format(results)
        # assert len(results) == 100
        pass


class TestPathFunctions:
    """Test job and training path discovery functions."""

    def test_get_job_paths(self, tmp_path):
        """Test that get_job_paths finds markdown files correctly."""
        # Create test directory structure
        jobs_dir = tmp_path / "data" / "jobs"
        jobs_dir.mkdir(parents=True)

        # Create some test job files
        (jobs_dir / "job_001.md").write_text("Test job 1")
        (jobs_dir / "job_002.md").write_text("Test job 2")
        (jobs_dir / "not_a_job.txt").write_text("Not a markdown file")

        with patch("src.utils.Path") as mock_path:
            mock_jobs_path = MagicMock()
            mock_path.return_value = mock_jobs_path
            mock_jobs_path.exists = MagicMock(return_value=True)
            mock_jobs_path.iterdir = MagicMock(return_value=[
                jobs_dir / "job_001.md",
                jobs_dir / "job_002.md",
                jobs_dir / "not_a_job.txt"
            ])

            # Should only find .md files
            paths = get_job_paths()
            md_paths = [p for p in paths if p.suffix == '.md']
            assert len(md_paths) == 2

    def test_get_training_paths(self, tmp_path):
        """Test that get_training_paths finds markdown files correctly."""
        # Create test directory structure
        trainings_dir = tmp_path / "data" / "trainings"
        trainings_dir.mkdir(parents=True)

        # Create some test training files
        (trainings_dir / "training_001.md").write_text("Test training 1")
        (trainings_dir / "training_002.md").write_text("Test training 2")
        (trainings_dir / "training_003.md").write_text("Test training 3")

        with patch("src.utils.Path") as mock_path:
            mock_trainings_path = MagicMock()
            mock_path.return_value = mock_trainings_path
            mock_trainings_path.exists = MagicMock(return_value=True)
            mock_trainings_path.iterdir = MagicMock(return_value=[
                trainings_dir / "training_001.md",
                trainings_dir / "training_002.md",
                trainings_dir / "training_003.md"
            ])

            paths = get_training_paths()
            assert len(paths) == 3
            assert all(p.suffix == '.md' for p in paths)

    def test_get_job_paths_missing_directory(self):
        """Test that get_job_paths raises error when directory not found."""
        with patch("src.utils.Path") as mock_path:
            mock_path.return_value.exists.return_value = False
            mock_path.return_value.parent.parent.__truediv__.return_value.exists.return_value = False

            with pytest.raises(FileNotFoundError, match="Jobs directory not found"):
                get_job_paths()

    def test_get_training_paths_missing_directory(self):
        """Test that get_training_paths raises error when directory not found."""
        with patch("src.utils.Path") as mock_path:
            mock_path.return_value.exists.return_value = False
            mock_path.return_value.parent.parent.__truediv__.return_value.exists.return_value = False

            with pytest.raises(FileNotFoundError, match="Trainings directory not found"):
                get_training_paths()


class TestCostTracking:
    """Test cost calculation and tracking functions."""

    def setup_method(self):
        """Reset cost tracker before each test."""
        reset_cost_tracker()

    def test_calculate_cost_mistral_large(self):
        """Test cost calculation for mistral-large model."""
        # 1000 input tokens, 500 output tokens
        cost = calculate_cost(1000, 500, 'mistral-large-latest')
        # Expected: (1000/1M * 2.00) + (500/1M * 6.00) = 0.002 + 0.003 = 0.005
        assert cost == pytest.approx(0.005, rel=1e-6)

    def test_calculate_cost_mistral_medium(self):
        """Test cost calculation for mistral-medium model."""
        cost = calculate_cost(10000, 2000, 'mistral-medium-latest')
        # Expected: (10000/1M * 0.40) + (2000/1M * 2.00) = 0.004 + 0.004 = 0.008
        assert cost == pytest.approx(0.008, rel=1e-6)

    def test_calculate_cost_mistral_small(self):
        """Test cost calculation for mistral-small model."""
        cost = calculate_cost(5000, 1000, 'mistral-small-latest')
        # Expected: (5000/1M * 0.10) + (1000/1M * 0.30) = 0.0005 + 0.0003 = 0.0008
        assert cost == pytest.approx(0.0008, rel=1e-6)

    def test_calculate_cost_unknown_model_defaults_to_medium(self):
        """Test that unknown models default to medium pricing."""
        cost = calculate_cost(10000, 2000, 'unknown-model')
        # Should use medium pricing
        expected = calculate_cost(10000, 2000, 'mistral-medium-latest')
        assert cost == expected

    def test_track_api_call_with_response_object(self):
        """Test tracking API call with response object."""
        # Reset first to ensure clean state
        reset_cost_tracker()

        # Create a simple object with metrics attribute
        class MockResponse:
            def __init__(self):
                self.metrics = type('obj', (object,), {
                    'accumulated_usage': {
                        'inputTokens': 1000,
                        'outputTokens': 500
                    }
                })()

        mock_response = MockResponse()
        cost = track_api_call(mock_response, model='mistral-large-latest')

        assert cost == pytest.approx(0.005, rel=1e-6)
        assert utils.COST_TRACKER['api_calls'] == 1
        assert utils.COST_TRACKER['total_input_tokens'] == 1000
        assert utils.COST_TRACKER['total_output_tokens'] == 500
        assert utils.COST_TRACKER['estimated_cost'] == pytest.approx(0.005, rel=1e-6)
        assert 'mistral-large-latest' in utils.COST_TRACKER['by_model']

    def test_track_api_call_with_token_counts(self):
        """Test tracking API call with direct token counts."""
        # Reset first to ensure clean state
        reset_cost_tracker()

        # Call with model as first positional argument
        cost = track_api_call(
            'mistral-small-latest',
            input_tokens=5000,
            output_tokens=1000
        )

        assert cost == pytest.approx(0.0008, rel=1e-6)
        assert utils.COST_TRACKER['api_calls'] == 1
        assert utils.COST_TRACKER['total_input_tokens'] == 5000
        assert utils.COST_TRACKER['total_output_tokens'] == 1000

    def test_track_api_call_accumulates(self):
        """Test that multiple API calls accumulate correctly."""
        # Reset first to ensure clean state
        reset_cost_tracker()

        # Call with model as first positional argument
        track_api_call('mistral-medium-latest', input_tokens=1000, output_tokens=500)
        track_api_call('mistral-medium-latest', input_tokens=2000, output_tokens=1000)
        track_api_call('mistral-large-latest', input_tokens=500, output_tokens=250)

        assert utils.COST_TRACKER['api_calls'] == 3
        assert utils.COST_TRACKER['total_input_tokens'] == 3500
        assert utils.COST_TRACKER['total_output_tokens'] == 1750
        assert 'mistral-medium-latest' in utils.COST_TRACKER['by_model']
        assert 'mistral-large-latest' in utils.COST_TRACKER['by_model']
        assert utils.COST_TRACKER['by_model']['mistral-medium-latest']['calls'] == 2
        assert utils.COST_TRACKER['by_model']['mistral-large-latest']['calls'] == 1

    def test_reset_cost_tracker(self):
        """Test that reset_cost_tracker clears all tracking data."""
        # Reset first to ensure clean state
        reset_cost_tracker()

        # Add some data - call with model as first positional argument
        track_api_call('mistral-medium-latest', input_tokens=1000, output_tokens=500)
        assert utils.COST_TRACKER['api_calls'] == 1

        # Reset
        reset_cost_tracker()

        # Verify all counters are zero
        assert utils.COST_TRACKER['api_calls'] == 0
        assert utils.COST_TRACKER['total_input_tokens'] == 0
        assert utils.COST_TRACKER['total_output_tokens'] == 0
        assert utils.COST_TRACKER['estimated_cost'] == 0.0
        assert utils.COST_TRACKER['by_model'] == {}

    def test_print_cost_summary(self, capsys):
        """Test that print_cost_summary outputs correct information."""
        # Reset first to ensure clean state
        reset_cost_tracker()

        # Add some test data - call with model as first positional argument
        track_api_call('mistral-medium-latest', input_tokens=10000, output_tokens=5000)
        track_api_call('mistral-large-latest', input_tokens=5000, output_tokens=2500)

        print_cost_summary()

        captured = capsys.readouterr()
        assert "💰 Cost Summary:" in captured.out
        assert "Total API calls: 2" in captured.out
        assert "Total tokens: 22,500" in captured.out  # 10000+5000+5000+2500
        assert "mistral-medium-latest" in captured.out
        assert "mistral-large-latest" in captured.out


class TestSendResults:
    """Test results submission function."""

    @patch('src.utils.requests.request')
    @patch('src.utils.boto3.Session')
    def test_send_results_dry_run(self, mock_session, mock_request, capsys):
        """Test that dry run validates without sending."""
        valid_results = [
            {
                "persona_id": "persona_001",
                "predicted_type": "awareness"
            }
        ]

        response = send_results(valid_results, dry_run=True)

        assert response is None
        mock_request.assert_not_called()

        captured = capsys.readouterr()
        assert "Dry run mode" in captured.out
        assert "1 results are valid" in captured.out

    @patch('src.utils.requests.request')
    @patch('src.utils.boto3.Session')
    def test_send_results_success(self, mock_session, mock_request, capsys):
        """Test successful submission."""
        # Setup mocks with proper attributes
        mock_credentials = MagicMock()
        mock_credentials.access_key = 'test_key'
        mock_credentials.secret_key = 'test_secret'
        mock_credentials.token = None
        mock_session.return_value.get_credentials.return_value = mock_credentials

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Submission received"}
        mock_request.return_value = mock_response

        valid_results = [
            {
                "persona_id": "persona_001",
                "predicted_type": "awareness"
            }
        ]

        response = send_results(valid_results)

        assert response.status_code == 200
        mock_request.assert_called_once()

        captured = capsys.readouterr()
        assert "✅ Submission successful!" in captured.out
        assert "Submission received" in captured.out

    @patch('src.utils.requests.request')
    @patch('src.utils.boto3.Session')
    def test_send_results_failure(self, mock_session, mock_request, capsys):
        """Test failed submission."""
        # Setup mocks with proper attributes
        mock_credentials = MagicMock()
        mock_credentials.access_key = 'test_key'
        mock_credentials.secret_key = 'test_secret'
        mock_credentials.token = None
        mock_session.return_value.get_credentials.return_value = mock_credentials

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid submission format"
        mock_request.return_value = mock_response

        valid_results = [
            {
                "persona_id": "persona_001",
                "predicted_type": "awareness"
            }
        ]

        response = send_results(valid_results)

        assert response.status_code == 400

        captured = capsys.readouterr()
        assert "❌ Submission failed" in captured.out
        assert "Invalid submission format" in captured.out

    @patch('src.utils.boto3.Session')
    def test_send_results_no_credentials(self, mock_session):
        """Test that missing AWS credentials raises error."""
        mock_session.return_value.get_credentials.return_value = None

        valid_results = [
            {
                "persona_id": "persona_001",
                "predicted_type": "awareness"
            }
        ]

        with pytest.raises(ValueError, match="AWS credentials not found"):
            send_results(valid_results)

    def test_send_results_invalid_format(self):
        """Test that invalid results format is caught before sending."""
        invalid_results = [
            {
                "predicted_type": "awareness"
                # Missing persona_id
            }
        ]

        with pytest.raises(ValueError, match="missing required fields"):
            send_results(invalid_results)


class TestSanityCheck:
    """Test API connection sanity check."""

    @patch('src.utils.requests.request')
    @patch('src.utils.boto3.Session')
    def test_sanity_check_success(self, mock_session, mock_request, capsys):
        """Test successful API connection check."""
        # Setup mocks with proper attributes
        mock_credentials = MagicMock()
        mock_credentials.access_key = 'test_key'
        mock_credentials.secret_key = 'test_secret'
        mock_credentials.token = None
        mock_session.return_value.get_credentials.return_value = mock_credentials

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        result = sanity_check()

        assert result is True
        mock_request.assert_called_once()

        captured = capsys.readouterr()
        assert "✅ API connection successful!" in captured.out

    @patch('src.utils.requests.request')
    @patch('src.utils.boto3.Session')
    def test_sanity_check_failure(self, mock_session, mock_request, capsys):
        """Test failed API connection check."""
        # Setup mocks with proper attributes
        mock_credentials = MagicMock()
        mock_credentials.access_key = 'test_key'
        mock_credentials.secret_key = 'test_secret'
        mock_credentials.token = None
        mock_session.return_value.get_credentials.return_value = mock_credentials

        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_request.return_value = mock_response

        result = sanity_check()

        assert result is False

        captured = capsys.readouterr()
        assert "❌ API check failed with status: 503" in captured.out

    @patch('src.utils.boto3.Session')
    def test_sanity_check_no_credentials(self, mock_session, capsys):
        """Test sanity check with missing credentials."""
        mock_session.return_value.get_credentials.return_value = None

        result = sanity_check()

        assert result is False

        captured = capsys.readouterr()
        assert "❌ AWS credentials not found" in captured.out

    @patch('src.utils.requests.request')
    @patch('src.utils.boto3.Session')
    def test_sanity_check_exception(self, mock_session, mock_request, capsys):
        """Test sanity check handles exceptions gracefully."""
        mock_session.side_effect = Exception("Network error")

        result = sanity_check()

        assert result is False

        captured = capsys.readouterr()
        assert "❌ Connection check failed: Network error" in captured.out