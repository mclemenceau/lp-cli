import pytest

from unittest.mock import Mock

from LpCli.lp_bug import ubuntu_devel


@pytest.fixture
def lp():
    bug1 = Mock()
    bug1.title = "This is the title of a bug"
    bug1.description = "This is the longer description"
    bug1.heat = "100"
    bug1.importance = "Undecided"
    bug1.bug_tasks = [
        Mock(bug_target_name=n, status=s)
        for n, s in zip(['systemd (Ubuntu)',
                         'vim (Debian)',
                         'glibc (Ubuntu)'],
                        ['New',
                         'Confirmed',
                         'New'])
    ]

    bug2 = Mock()
    bug2.title = "This is the title of another bug"
    bug2.description = "This is the longer description"
    bug2.heat = "200"
    bug2.importance = "Undecided"
    bug2.bug_tasks = [
        Mock(bug_target_name=s)
        for s in [
            'systemd (Ubuntu)',
            'systemd (Ubuntu Focal)',
            'systemd (Ubuntu Bionic)',
            'vim (Debian)']
    ]

    bug3 = Mock()
    bug3.title = "This is the title of a third bug"
    bug3.description = "This is the longer description"
    bug3.heat = "300"
    bug3.importance = "Undecided"
    bug3.bug_tasks = [
        Mock(bug_target_name=n, status=s)
        for n, s in zip(
            ['systemd (Ubuntu)',
             'systemd (Ubuntu Focal)',
             'systemd (Ubuntu Bionic)',
             'vim (Debian)',
             'glibc (Ubuntu)',
             'glibc (Ubuntu Focal)',
             'glibc (Ubuntu None)',
             'glibc !@#$)',
             'glibc (Ubuntu Bionic)'],
            ['New',
             'New',
             'New',
             'New',
             'New',
             'Incomplete',
             'New',
             'New',
             'Confirmed']
        )
    ]

    bug4 = Mock()
    bug4.title = "This is the title of a casper bug"
    bug4.description = "This is the longer description"
    bug4.heat = "350"
    bug4.importance = "Undecided"
    bug4.bug_tasks = [
        Mock(bug_target_name=n, status=s)
        for n, s in zip(
            ['casper (Ubuntu)',
             'casper (Ubuntu '+ubuntu_devel+')'],
            ['New', 'New'])
    ]

    bug5 = Mock()
    bug5.title = "This is the title of a bug"
    bug5.heat = "100"
    bug5.bug_tasks = []

    bug6 = Mock()
    bug6.title = "This is the title of a bug"
    bug6.heat = "100"
    bug6.bug_tasks = [Mock(
            bug_target_name='systemd (Ubuntu)',
            status='New',
            importance='Critical')]

    return Mock(bugs={
            1: bug1,
            2: bug2,
            3: bug3,
            4: bug4,
            5: bug5,
            6: bug6
                })
