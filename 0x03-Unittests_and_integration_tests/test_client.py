#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")  # Important: Patch where it’s used, not where it’s defined
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_result)

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
from unittest.mock import patch, PropertyMock
import unittest
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL from mocked org"""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test-org/repos"}
            
            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/test-org/repos")
            from unittest import TestCase
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(TestCase):
    """Unit tests for GithubOrgClient"""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names"""
        # Setup mock payload from get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_payload

        # Mock _public_repos_url using context manager
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test-org/repos"

            client = GithubOrgClient("test-org")
            repos = client.public_repos()

            # Assertions
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
            mock_url.assert_called_once()

