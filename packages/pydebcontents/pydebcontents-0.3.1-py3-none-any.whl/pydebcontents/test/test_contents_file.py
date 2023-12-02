from pathlib import Path

import pytest

from pydebcontents import (
    ContentsFile,
    ContentsError,
    glob2re,
    re2re,
    fixed2re,
)


@pytest.mark.usefixtures("dakdata")
class TestContentsFile:
    data: Path

    def test_search_one_arch(self) -> None:
        contents = ContentsFile(
            self.data,
            "sid",
            "amd64",
            ["main", "contrib"],
        )

        # file in sid/amd64/main
        packages = contents.search("usr/bin/perl")
        assert packages
        assert "perl/perl-base" in packages.keys()
        assert packages["perl/perl-base"]

        # file in sid/all/main
        packages = contents.search(r"^bin/ash\s")
        assert not packages

        # file in sid/amd64/contrib
        packages = contents.search("usr/share/doc/gcc-doc/README")
        assert packages

        # file in sid/all/contrib
        packages = contents.search("etc/default/josm")
        assert not packages

        # no file
        packages = contents.search("no-such-file")
        assert not packages

    def test_search_multiple_arch(self) -> None:
        contents = ContentsFile(self.data, "sid", ["amd64", "all"], ["main", "contrib"])

        # file in sid/amd64/main
        packages = contents.search("usr/bin/perl")
        assert packages

        # file in sid/all/main
        packages = contents.search("bin/ash")
        assert packages

        # file in sid/amd64/contrib
        packages = contents.search("usr/share/doc/gcc-doc/README")
        assert packages

        # file in sid/all/contrib
        packages = contents.search("etc/default/josm")
        assert packages

    def test_search_implicit_component(self) -> None:
        contents = ContentsFile(self.data, "sid", "amd64")

        # file in sid/amd64/main
        packages = contents.search("usr/bin/perl")
        assert packages

    def test_search_str_init(self) -> None:
        contents = ContentsFile(self.data, "sid", "amd64", "main")

        # file in sid/amd64/main
        packages = contents.search("usr/bin/perl")
        assert packages

    def test_search_bad_regex(self) -> None:
        contents = ContentsFile(self.data, "sid", "amd64", "main")

        # syntax error in regexp
        with pytest.raises(ContentsError):
            contents.search(r"abc(abc")

    def test_search_bad_init(self) -> None:
        contents = ContentsFile(
            self.data, "no-such-release", "amd64", ["main", "contrib"]
        )
        with pytest.raises(ContentsError):
            contents.search("usr/bin/perl")

        contents = ContentsFile(self.data, "sid", "no-such-arch", ["main", "contrib"])
        with pytest.raises(ContentsError):
            contents.search("usr/bin/perl")

        contents = ContentsFile(self.data, "sid", "amd64", ["no-such-compoment"])
        with pytest.raises(ContentsError):
            contents.search("usr/bin/perl")

        # if there is one successful (arch,component) then proceed
        contents = ContentsFile(
            self.data, "sid", "amd64", ["main", "no-such-component"]
        )
        contents.search("usr/bin/perl")


class TestContentsFileSearchHelpers:
    def test_glob2re(self) -> None:
        testre = glob2re("/usr/bin/perl")
        assert testre.startswith("^")
        assert "usr/bin/perl" in testre
        assert "/usr/bin/perl" not in testre
        assert "$" not in testre

        testre = glob2re("/usr/bin/perl*")
        assert testre.startswith("^")
        assert "usr/bin/perl.*" in testre
        assert "/usr/bin/perl" not in testre
        assert "$" not in testre

        testre = glob2re("bin/perl*")
        assert not testre.startswith("^")
        assert "bin/perl.*" in testre

        testre = glob2re("/usr/share/doc/*/copyright")
        assert testre.startswith("^")
        assert "usr/share/doc/.*/copyright" in testre
        assert "$" not in testre

    def test_re2re(self) -> None:
        testre = re2re("^/usr/bin/perl$")
        assert testre.startswith("^")
        assert "usr/bin/perl" in testre
        assert "/usr/bin/perl" not in testre
        assert "$" not in testre

        testre = re2re("/usr/bin/perl.*")
        assert testre.startswith("^")
        assert "usr/bin/perl.*" in testre
        assert "/usr/bin/perl" not in testre
        assert "$" not in testre

        testre = re2re("bin/perl.*")
        assert testre.startswith("^[^ ]*")
        assert "bin/perl.*" in testre

        testre = re2re("/usr/share/doc/.*/copyright")
        assert testre.startswith("^")
        assert "usr/share/doc/.*/copyright" in testre
        assert "$" not in testre

    def test_fixed2re(self) -> None:
        testre = fixed2re("/usr/bin/perl")
        assert testre == r"^usr/bin/perl\s"

        testre = fixed2re("usr/bin/perl")
        assert testre == r"^usr/bin/perl\s"
