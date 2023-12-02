# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

from vcr import VCR

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

vcr = VCR(
    cassette_library_dir=str(ROOT / "fixtures" / "cassettes"),
    filter_headers=["Authorization"],
)
