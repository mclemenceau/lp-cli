import pytest

from LpCli.lp_bug import lp_bug, ubuntu_devel


def test_bug_init_bad_lp_api():
    with pytest.raises(ValueError):
        return lp_bug(1234567, None)


def test_bug_init_bad_type_bug(lp):
    with pytest.raises(ValueError):
        return lp_bug("bad", lp)


def test_bug_init_bad_bug_doesnt_exist(lp):
    with pytest.raises(KeyError):
        return lp_bug(123456789, lp)


def test_default_init(lp):
    bug = lp_bug(1, lp)
    assert bug.id == 1
    assert bug.title == "This is the title of a bug"
    assert bug.description == "This is the longer description"
    assert bug.heat == "100"


def test_affected_packages(lp):
    bug1 = lp_bug(1, lp)
    assert bug1.affected_packages == ['systemd', 'glibc']

    bug2 = lp_bug(2, lp)
    assert bug2.affected_packages == ['systemd']


def test_affected_series(lp):

    bug = lp_bug(3, lp)

    # Simple default serie test
    series = bug.affected_series('systemd')

    assert series == ['Impish', 'Focal', 'Bionic']

    # Wrong Serie vim (Debian)
    series = bug.affected_series('vim')
    assert series == []

    # Ignore Bad serie glibc !@#$)
    series = bug.affected_series('glibc')
    assert series == ['Impish', 'Focal', 'Bionic']


def test_affected_series_double(lp):
    bug = lp_bug(4, lp)

    series = bug.affected_series('casper')
    assert series == ['Impish']


def test_affected_versions(lp):
    bug = lp_bug(3, lp)

    versions = bug.affected_versions('systemd')
    assert versions == ['21.10', '20.04', '18.04']

    versions = bug.affected_versions('vim')
    assert versions == []

    versions = bug.affected_versions('glibc')
    assert versions == ['21.10', '20.04', '18.04']


def test_package_detail(lp):
    bug = lp_bug(3, lp)

    # test with a missing serie and make sure it defaults to ubuntu_devel
    assert bug.package_detail("glibc", 'Focal', "status") == "Incomplete"

    assert bug.package_detail("systemd", ubuntu_devel, "status") == "New"

    # test for detail that doesn't exist
    assert bug.package_detail("systemd", ubuntu_devel, "age") == ""


def test_bug_str(lp):
    bug = lp_bug(5, lp)
    bug_str = "LP: #5 : This is the title of a bug\nHeat: 100"
    assert str(bug) == bug_str

    bug = lp_bug(6, lp)
    bug_str = "LP: #6 : This is the title of a bug\n"\
        "Heat: 100\n - systemd:\n   - Impish : New (Critical)"
    assert str(bug) == bug_str


def test_bug_dict(lp):
    bug = lp_bug(5, lp)
    bug_dict = {'id': 5,
                'title': 'This is the title of a bug',
                'packages': {}}

    assert bug.dict() == bug_dict


def test_bug_repr(lp):
    bug = lp_bug(5, lp)
    bug_dict = {'id': 5,
                'title': 'This is the title of a bug',
                'packages': {}}

    assert bug.__repr__() == bug_dict.__str__()

# =============================================================================
