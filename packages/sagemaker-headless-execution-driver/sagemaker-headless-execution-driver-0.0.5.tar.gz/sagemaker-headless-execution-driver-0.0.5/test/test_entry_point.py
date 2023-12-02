import subprocess
import unittest


class TestEntryPoint(unittest.TestCase):
    def test_amazon_sagemaker_scheduler_entry_point(self):
        """Test if 'amazon_sagemaker_scheduler' entry point is created and executable."""
        try:
            # Attempt to execute the entry point command
            result = subprocess.run(
                ["amazon_sagemaker_scheduler", "--help"],
                capture_output=True,
                text=True,
                check=True,
            )

            # If no exception is raised, the command is available and executable
            self.assertTrue(result.returncode == 0)
        except FileNotFoundError:
            # If a FileNotFoundError is raised, the entry point is not available
            self.fail("amazon_sagemaker_scheduler entry point is not available.")


if __name__ == "__main__":
    unittest.main()
