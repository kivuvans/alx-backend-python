#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
Task 4: Parameterize and Patch as Decorators.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once with the correct argument.
        """
        # Arrange
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)

        # Act
        result = client.org

        # Assert
        self.assertEqual(result, expected_response)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == "__main__":
    unittest.main()
