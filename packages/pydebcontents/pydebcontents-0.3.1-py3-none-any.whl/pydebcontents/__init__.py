import importlib.metadata


# Import the public API
from ._contents_file import (
    ContentsFile,
    ContentsError,
    glob2re,
    re2re,
    fixed2re,
    pattern2re,
)

from ._contents_dict import ContentsDict

__all__ = [
    "ContentsFile",
    "ContentsError",
    "glob2re",
    "re2re",
    "fixed2re",
    "pattern2re",
    "ContentsDict",
]

# fetch the version from the pyproject.toml / installed wheel
try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"
