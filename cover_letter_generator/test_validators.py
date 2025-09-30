"""
Test file for the validators module.

This demonstrates:
- How to write simple, readable tests
- How to test edge cases
- How to use Python's unittest framework
- Good testing practices for learning

Run tests with: python -m pytest test_validators.py -v
"""

import unittest
from unittest.mock import Mock
from validators import validate_inputs, detect_file_type, validate_file_size


class TestValidators(unittest.TestCase):
    """Test cases for the validators module."""
    
    def test_validate_inputs_with_valid_data(self):
        """Test that valid inputs return True with no error message."""
        # Arrange: Create mock file object
        mock_file = Mock()
        mock_file.name = "test.pdf"
        
        # Act: Call the function with valid inputs
        is_valid, error_message = validate_inputs(mock_file, "Software Engineer position")
        
        # Assert: Should be valid with no error
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)
    
    def test_validate_inputs_with_no_file(self):
        """Test that missing file returns appropriate error."""
        # Act: Call with no file
        is_valid, error_message = validate_inputs(None, "Software Engineer position")
        
        # Assert: Should be invalid with error message
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "❌ Please upload a resume file.")
    
    def test_validate_inputs_with_empty_job_description(self):
        """Test that empty job description returns appropriate error."""
        # Arrange: Create mock file object
        mock_file = Mock()
        
        # Act: Call with empty job description
        is_valid, error_message = validate_inputs(mock_file, "")
        
        # Assert: Should be invalid with error message
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "❌ Please provide a job description.")
    
    def test_validate_inputs_with_whitespace_only_job_description(self):
        """Test that job description with only whitespace returns error."""
        # Arrange: Create mock file object
        mock_file = Mock()
        
        # Act: Call with whitespace-only job description
        is_valid, error_message = validate_inputs(mock_file, "   \n\t   ")
        
        # Assert: Should be invalid with error message
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "❌ Please provide a job description.")
    
    def test_detect_file_type_pdf(self):
        """Test PDF file type detection."""
        # Act & Assert: Test various PDF file names
        self.assertEqual(detect_file_type("resume.pdf", "auto"), "pdf")
        self.assertEqual(detect_file_type("My Resume.PDF", "auto"), "pdf")
        self.assertEqual(detect_file_type("path/to/file.pdf", "auto"), "pdf")
    
    def test_detect_file_type_docx(self):
        """Test DOCX file type detection."""
        # Act & Assert: Test various DOCX file names
        self.assertEqual(detect_file_type("resume.docx", "auto"), "docx")
        self.assertEqual(detect_file_type("My Resume.DOCX", "auto"), "docx")
        self.assertEqual(detect_file_type("resume.doc", "auto"), "docx")
    
    def test_detect_file_type_text(self):
        """Test text file type detection."""
        # Act & Assert: Test various text file names
        self.assertEqual(detect_file_type("resume.txt", "auto"), "text")
        self.assertEqual(detect_file_type("resume.rtf", "auto"), "text")
        self.assertEqual(detect_file_type("resume", "auto"), "text")  # No extension
    
    def test_detect_file_type_user_override(self):
        """Test that user-specified type overrides auto-detection."""
        # Act & Assert: User specification should override file extension
        self.assertEqual(detect_file_type("resume.pdf", "docx"), "docx")
        self.assertEqual(detect_file_type("resume.docx", "text"), "text")
        self.assertEqual(detect_file_type("resume.txt", "pdf"), "pdf")


class TestFileSizeValidation(unittest.TestCase):
    """Test cases for file size validation."""
    
    def test_validate_file_size_with_valid_file(self):
        """Test file size validation with a valid file."""
        # This test would require creating a temporary file
        # For now, we'll test the error handling
        pass
    
    def test_validate_file_size_with_nonexistent_file(self):
        """Test file size validation with nonexistent file."""
        # Act: Try to validate a file that doesn't exist
        is_valid, error_message = validate_file_size("/nonexistent/file.pdf")
        
        # Assert: Should return error
        self.assertFalse(is_valid)
        self.assertEqual(error_message, "❌ Could not read file size")


if __name__ == "__main__":
    # Run the tests
    unittest.main()
