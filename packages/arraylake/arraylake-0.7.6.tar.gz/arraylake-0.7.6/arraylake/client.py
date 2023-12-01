"""
The Client module contains the main classes used to interact with the Arraylake service.
For asyncio interaction, use the #AsyncClient. For regular, non-async interaction, use the #Client.

**Example usage:**

```python
from arraylake import Client
client = Client()
repo = client.get_repo("my-org/my-repo")
```
"""

import re
from dataclasses import dataclass, field
from typing import Optional, Sequence, Tuple

from arraylake.asyn import sync
from arraylake.chunkstore import chunkstore
from arraylake.config import config
from arraylake.log_util import get_logger
from arraylake.metastore import HttpMetastore, HttpMetastoreConfig
from arraylake.repo import AsyncRepo, Repo
from arraylake.types import Author
from arraylake.types import Repo as RepoModel

logger = get_logger(__name__)

_VALID_NAME = r"(\w[\w\.\-_]+)"


def _parse_org_and_repo(org_and_repo: str) -> Tuple[str, str]:
    expr = f"{_VALID_NAME}/{_VALID_NAME}"
    res = re.fullmatch(expr, org_and_repo)
    if not res:
        raise ValueError(f"Not a valid repo identifier: `{org_and_repo}`. " "Should have the form `{ORG}/{REPO}`.")
    org, repo_name = res.groups()
    return org, repo_name


def _validate_org(org_name: str):
    if not re.fullmatch(_VALID_NAME, org_name):
        raise ValueError(f"Invalid org name: `{org_name}`.")


def _default_service_uri() -> str:
    return config.get("service.uri", "https://api.earthmover.io")


def _default_token() -> Optional[str]:
    return config.get("token", None)


@dataclass
class AsyncClient:
    """Asyncio Client for interacting with ArrayLake

    Args:
        service_uri (str): [Optional] The service URI to target.
        token (str): [Optional] API token for service account authentication.
    """

    service_uri: str = field(default_factory=_default_service_uri)
    token: Optional[str] = field(default_factory=_default_token, repr=False)
    auth_org: Optional[str] = None

    def __post_init__(self):
        if self.token is not None and not self.token.startswith("ema_"):
            raise ValueError("Invalid token provided. Tokens must start with ema_")
        if not self.service_uri.startswith("http"):
            raise ValueError("service uri must start with http")
        self.auth_org = self.auth_org or config.get("user.org", None)

    async def list_repos(self, org: str) -> Sequence[RepoModel]:
        """List all repositories for the specified org

        Args:
            org: Name of the org
        """

        _validate_org(org)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))
        repos = await mstore.list_databases()
        return repos

    async def get_repo(self, name: str) -> AsyncRepo:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))
        db = await mstore.open_database(repo_name)

        s3_uri = config.get("chunkstore.uri")
        inline_threshold_bytes = int(config.get("chunkstore.inline_threshold_bytes", 0))
        client_kws = config.get("s3", {})
        cstore = chunkstore(s3_uri, inline_threshold_bytes=inline_threshold_bytes, **client_kws)

        user = await mstore.get_user()

        author: Author = user.as_author()
        arepo = AsyncRepo(db, cstore, name, author)
        await arepo.checkout()
        return arepo

    async def get_or_create_repo(self, name: str) -> AsyncRepo:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """
        org, repo_name = _parse_org_and_repo(name)
        all_repos = [result.name for result in await self.list_repos(org)]
        if repo_name in all_repos:
            return await self.get_repo(name)
        else:
            return await self.create_repo(name)

    async def create_repo(self, name: str) -> AsyncRepo:
        """Create a new repo

        Args:
            name: Full name of the repo to create (of the form {ORG}/{REPO})
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))

        s3_uri = config.get("chunkstore.uri")
        inline_threshold_bytes = int(config.get("chunkstore.inline_threshold_bytes", 0))
        client_kws = config.get("s3", {})
        cstore = chunkstore(s3_uri, inline_threshold_bytes=inline_threshold_bytes, **client_kws)

        user = await mstore.get_user()
        author: Author = user.as_author()

        # important: call create_database after setting up the metastore and chunkstore objects
        db = await mstore.create_database(repo_name)
        arepo = AsyncRepo(db, cstore, name, author)
        await arepo.checkout()
        return arepo

    async def delete_repo(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form {ORG}/{REPO})
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))
        await mstore.delete_database(repo_name, imsure=imsure, imreallysure=imreallysure)


@dataclass
class Client:
    """Client for interacting with ArrayLake.

    Args:
        service_uri (str): [Optional] The service URI to target.
        token (str): [Optional] API token for service account authentication.
    """

    service_uri: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    auth_org: Optional[str] = None

    def __post_init__(self):
        if self.token is None:
            self.token = config.get("token", None)
        if self.service_uri is None:
            self.service_uri = config.get("service.uri")
        self.auth_org = self.auth_org or config.get("user.org", None)

        self.aclient = AsyncClient(self.service_uri, token=self.token, auth_org=self.auth_org)

    def list_repos(self, org: str) -> Sequence[RepoModel]:
        """List all repositories for the specified org

        Args:
            org: Name of the org
        """

        repo_list = sync(self.aclient.list_repos, org)
        return repo_list

    def get_repo(self, name: str) -> Repo:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """

        arepo = sync(self.aclient.get_repo, name)
        return Repo(arepo)

    def get_or_create_repo(self, name: str) -> Repo:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """
        arepo = sync(self.aclient.get_or_create_repo, name)
        return Repo(arepo)

    def create_repo(self, name: str) -> Repo:
        """Create a new repo

        Args:
            name: Full name of the repo to create (of the form {ORG}/{REPO})
        """

        arepo = sync(self.aclient.create_repo, name)
        return Repo(arepo)

    def delete_repo(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form {ORG}/{REPO})
        """

        return sync(self.aclient.delete_repo, name, imsure=imsure, imreallysure=imreallysure)
