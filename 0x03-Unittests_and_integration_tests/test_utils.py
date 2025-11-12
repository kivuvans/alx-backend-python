#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
Task 5: Mocking a property.
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
        """Test GithubOrgClient.org returns correct value."""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)

        result = client.org
        self.assertEqual(result, expected_response)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected value."""
        # Define a fake organization payload
        payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

        # Patch the 'org' property to return the fake payload
        with patch.object(GithubOrgClient, "org", new_callable=property(lambda self: payload)):
            client = GithubOrgClient("test-org")

            # Check if _public_repos_url returns the repos_url from the payload
            self.assertEqual(client._public_repos_url, payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
