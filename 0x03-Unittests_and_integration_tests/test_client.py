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
            #!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch.object(GithubOrgClient, "get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test-org/repos"

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
            mock_url.assert_called_once()
#!/usr/bin/env python3
"""
Unittest module for GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch.object(GithubOrgClient, "get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names"""
        # Mock the response from get_json
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        # Mock the _public_repos_url property
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test-org/repos"

            # Create client and call method
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Assert returned result
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            # Ensure mocks were called once
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
            mock_url.assert_called_once()
            #!/usr/bin/env python3
"""
Unittest module for GithubOrgClient
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher and mock requests.get().json()"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Mock response .json() behavior depending on URL
        def side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

