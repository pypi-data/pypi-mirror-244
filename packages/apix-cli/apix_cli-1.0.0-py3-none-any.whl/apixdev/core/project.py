import logging
import os
import subprocess
from shutil import rmtree

import requests
from requests.exceptions import HTTPError

from apixdev.core.compose import Compose
from apixdev.core.docker import Stack
from apixdev.core.exceptions import DownloadError
from apixdev.core.settings import settings, vars
from apixdev.core.tools import (
    filter_requirements,
    get_requirements_from_path,
    list_to_text,
    text_to_list,
)

_logger = logging.getLogger(__name__)


class Project:
    def __init__(self, name, path=None):
        self.root_path = settings.workdir
        self.path = path or os.path.join(self.root_path, name)
        self.name = name
        self.uuid = None
        self.major_version = None

        os.makedirs(self.path, exist_ok=True)

        if self.is_ready:
            self.read_manifest()

    def __repr__(self) -> str:
        return f"Project({self.name})"

    def __str__(self) -> str:
        return f"{self.name} ({self.major_version})"

    @classmethod
    def from_path(cls, path):
        """Load project from path."""

        name = os.path.basename(path)
        instance = cls(name, path)

        return instance

    @property
    def compose_file(self):
        """Complete filepath to docker-compose.yaml."""

        return os.path.join(self.path, "docker-compose.yaml")

    @property
    def repositories_file(self):
        """Complete filepath to repositories.yaml."""

        return os.path.join(self.path, "repositories.yaml")

    @property
    def manifest_file(self):
        """Complete filepath to manifest.yaml."""

        return os.path.join(self.path, "manifest.yaml")

    @property
    def env_file(self):
        """Complete filepath to .env file."""

        return os.path.join(self.path, ".env")

    @property
    def repositories_path(self):
        """Complete path to repositories."""

        return os.path.join(self.path, "repositories")

    @property
    def is_ready(self):
        """A project is considered ready if all 3 manifests are present."""

        files = [
            self.compose_file,
            self.repositories_file,
            self.manifest_file,
        ]
        return bool(all(map(os.path.exists, files)))

    def _get_manifest(self):
        return Compose.from_path(self.manifest_file)

    def download(self, filename, url, force=False):
        """Generic method to download file from ApiX database."""

        filepath = os.path.join(self.path, filename)
        headers = {
            "X-Api-Token": settings.get_var("apix.token"),
        }

        if force and os.path.exists(filepath):
            _logger.debug("Remove %s file", filepath)
            os.remove(filepath)

        try:
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=False,
                timeout=vars.DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
        except HTTPError as error:
            code = error.response.status_code
            raise DownloadError(filename, url, code) from error

        with open(filepath, "wb") as file:
            file.write(response.content)

        return True

    def pull_repositories(self):
        """Recursively pull code repositories"""
        if not self.repositories_file:
            return False

        env_file = self.env_file if os.path.exists(self.env_file) else settings.env_file

        args = [
            "gitaggregate",
            "-c",
            "repositories.yaml",
            "--expand-env",
            "--env-file",
            env_file,
        ]
        subprocess.call(args, cwd=self.path)

        return True

    def merge_requirements(self):
        """Merge all requirements from manifest and repositories."""

        compose = Compose.from_path(self.compose_file)

        requirements = get_requirements_from_path(self.repositories_path)
        requirements += text_to_list(
            compose.extract("services/odoo/environment/CUSTOM_REQUIREMENTS")
        )
        requirements = filter_requirements(requirements)

        text = list_to_text(requirements)
        compose.update("services/odoo/environment/CUSTOM_REQUIREMENTS", text)
        compose.save(self.compose_file)

    def read_manifest(self):
        """Read YAML manifest."""

        manifest = self._get_manifest()
        self.uuid = manifest.extract("uuid")
        self.major_version = manifest.extract("major_version")

    def load_manifest(self):
        """Load YAML manifest and download files related."""

        manifest = self._get_manifest()

        keys = [
            (self.compose_file, "docker_compose_url"),
            (self.repositories_file, "repositories_url"),
        ]

        for filename, key in keys:
            url = manifest.extract(key)
            self.download(filename, url, True)

    def get_stack(self):
        """Return Stack object."""

        return Stack(self.name, self.path)

    def get_repo(self):
        """Return repositories and branches from YAML manifest."""

        compose = Compose.from_path(self.repositories_file)

        res = {
            k.split("/")[-1]: v["merges"][0].split(" ")[-1]
            for k, v in compose._content.items()
        }

        return res

    def delete(self):
        """Delete project and remove files."""

        rmtree(self.path, ignore_errors=True)
        self.root_path = None
        self.path = None
        self.name = None
