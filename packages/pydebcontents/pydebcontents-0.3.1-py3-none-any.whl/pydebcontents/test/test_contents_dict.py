from pydebcontents import ContentsDict


class TestContentsDict:
    @staticmethod
    def _test_dict1() -> ContentsDict:
        d = ContentsDict()
        d.add("/a/b/c", ["foo/pkgA", "bar/pkgB"])
        d.add("/d/e/f", ["foo/pkgA", "baz/pkgC", "foo/pkgD", "pkgE"])
        d.add("/unique", ["bar/pkgB"])
        return d

    @staticmethod
    def _test_dict2() -> ContentsDict:
        d = ContentsDict()
        d.add("/a/b/c", ["contrib/foo/pkgF"])  # a new place for same file
        d.add("/g/h/i", ["foo/pkgA", "contrib/baz/pkgG"])  # new pkgs and  new files
        return d

    def test_add(self) -> None:
        d = self._test_dict1()

        assert len(d) == 5, "5 packages are loaded to test"
        assert len(d["foo/pkgA"]) == 2, "2 files are found in pkgA"
        assert not d.results_truncated

    def test_update(self) -> None:
        d1 = self._test_dict1()
        d2 = self._test_dict2()
        d1.update(d2)

        assert len(d1) == 7, "5+2=7 packages are loaded to test"
        assert (
            len(d1["foo/pkgA"]) == 3
        ), "3 files are found in pkgA across multiple searches"
        assert len(d1["contrib/foo/pkgF"]) == 1, "1 file in pkgF"
        assert not d1.results_truncated

    def test_update_truncated(self) -> None:
        d1 = self._test_dict1()
        d2 = self._test_dict2()
        d1.results_truncated = True
        d1.update(d2)
        assert d1.results_truncated

        d1 = self._test_dict1()
        d2 = self._test_dict2()
        d2.results_truncated = True
        d1.update(d2)
        assert d1.results_truncated

        d1 = self._test_dict1()
        d2 = self._test_dict2()
        d1.results_truncated = True
        d2.results_truncated = True
        d1.update(d2)
        assert d1.results_truncated

    def test_str(self) -> None:
        d = self._test_dict1()
        s = str(d)
        assert "pkgA: /a/b/c, /d/e/f" in s
        assert "pkgB: /a/b/c, /unique" in s

    def test_to_string(self) -> None:
        d = self._test_dict1()

        s = d.to_string(lambda s: s)
        assert "pkgA: /a/b/c, /d/e/f" in s
        assert "pkgB: /a/b/c, /unique" in s

        s = d.to_string(lambda s: f"@@{s}@@")
        assert "@@pkgA@@" in s
