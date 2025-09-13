"""
Basic tests for GDSC utilities.

Run with: pytest tests/

Pro tip: Always write tests for your submission logic!
Even in a competition, tests save debugging time.
"""
import pytest
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    validate_submission_format, 
    save_json, 
    read_json,
    load_file_content
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