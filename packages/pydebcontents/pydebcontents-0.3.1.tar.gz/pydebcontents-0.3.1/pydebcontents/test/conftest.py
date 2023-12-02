###
# Copyright (c) 2020-2023  Stuart Prescott
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import datetime
from pathlib import Path

from typing import Iterable, Optional

import pytest
import requests


mirror_base = "http://deb.debian.org/debian"
releases = ["sid"]
components = ["main", "contrib"]
resources = [
    "Contents-all.gz",
    "Contents-amd64.gz",
]

max_age = 24 * 3600  # one day
timeout = 120  # seconds to wait for the gz file

###########################################################

# Contents.gz files obtained form the mirror and stored locally
# They are cached for an hour (controlled by max_age above)


def fetch_dak_data(cache: Path, force: bool = False) -> Path:  # pragma: no-cover
    ok_mtime = datetime.datetime.utcnow().timestamp() - max_age

    base = cache / DAK_DATA_PREFIX

    for release in releases:
        for component in components:
            path = base / "dists" / release / component
            path.mkdir(parents=True, exist_ok=True)

            for resource in resources:
                filename = path / resource
                if (
                    not force
                    and filename.exists()
                    and filename.stat().st_mtime >= ok_mtime
                ):
                    continue

                url = f"{mirror_base}/dists/{release}/{component}/{resource}"
                r = requests.get(url, timeout=timeout)
                r.raise_for_status()

                with open(filename, "wb") as fh:
                    for chunk in r.iter_content(chunk_size=2048):
                        fh.write(chunk)

    return base


@pytest.fixture(name="dakdata_downloader", scope="session")
def fixture_dakdata_downloader(
    request: pytest.FixtureRequest, local_cache_dir: Path
) -> Iterable[Path]:
    # pylint: disable=unused-argument
    force = False
    yield fetch_dak_data(local_cache_dir, force)


@pytest.fixture(name="dakdata", scope="class")
def fixture_dakdata(request: pytest.FixtureRequest, dakdata_downloader: Path) -> None:
    # pylint: disable=unused-argument
    request.cls.data = dakdata_downloader


LOCAL_CACHE_LOCATION: Optional[Path] = None
DAK_DATA_PREFIX = "dakdata"


@pytest.fixture(name="local_cache_dir", scope="session")
def fixture_local_cache_dir(tmp_path_factory: pytest.TempPathFactory) -> Iterable[Path]:
    global LOCAL_CACHE_LOCATION  # pylint: disable=global-statement
    if not LOCAL_CACHE_LOCATION:
        # first attempt is to use a persistent directory within the source
        cache_dir = Path(__file__).parent.parent.parent / ".pydebcontents_test_cache"
        try:  # pragma: no cover
            cache_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:  # pragma: no cover
            cache_dir = tmp_path_factory.mktemp(
                "pydebcontents_test_cache", numbered=False
            )
        LOCAL_CACHE_LOCATION = cache_dir

    yield LOCAL_CACHE_LOCATION
