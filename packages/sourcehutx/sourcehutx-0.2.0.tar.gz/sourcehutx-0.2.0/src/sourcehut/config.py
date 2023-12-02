# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

"""
Sourcehut client configuration
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

if sys.version_info[:2] >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pydantic import BaseModel, validator

DEFAULT_BASEURL = "sr.ht"
try:
    _XDG_CONFIG_HOME = Path(os.environ["XDG_CONFIG_HOME"])
except KeyError:
    _XDG_CONFIG_HOME = Path.home() / ".config"

CONFIG_PATH = _XDG_CONFIG_HOME / "python-sourcehut.toml"


class SrhtConfig(BaseModel):
    baseurl: str = DEFAULT_BASEURL
    protocol: str = "https://"
    api_token_command: Optional[List[str]] = []
    api_token: Optional[str] = None

    @validator("api_token", always=True, pre=True)
    def v_api_token(cls, value: Optional[str], values) -> str | None:
        token_cmd = values.get("api_token_command")
        if value and token_cmd:
            raise ValueError("api_token and api_token_command are mutually exclusive")
        if value:
            return value
        if token_cmd:
            proc = subprocess.run(
                token_cmd, capture_output=True, text=True, check=False
            )
            out = proc.stdout.strip()
            if proc.returncode or not out:
                raise ValueError("Failed to retrieve api token from api_token_command")
            return out
        return None

    @classmethod
    def read_config(cls, path: Path | None = None) -> SrhtConfig:
        path = path or CONFIG_PATH
        try:
            with path.open("rb") as fp:
                return cls(**tomllib.load(fp))
        except FileNotFoundError:
            return cls()


__all__ = ("SrhtConfig", "DEFAULT_BASEURL", "CONFIG_PATH")
