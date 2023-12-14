import unittest

from text2music.__main__ import get_fixed_file_name


class TestMain(unittest.TestCase):
    def test_get_fixed_file_name(self) -> None:
        # Test that get_fixed_file_name correctly replaces characters
        self.assertEqual(get_fixed_file_name("test file.wav"), "test_file")
        self.assertEqual(get_fixed_file_name("test.file"), "test_file")
        self.assertEqual(get_fixed_file_name("test,file"), "test_file")


if __name__ == "__main__":
    unittest.main()
