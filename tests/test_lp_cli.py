import pytest

from unittest import mock

from LpCli.lp_cli import main


def test_main_help(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(['--help'])
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert 'bug_id' in captured.out


def test_main_run(capsys, lp):
    with mock.patch('LpCli.lp_cli.Launchpad') as Launchpad:
        Launchpad.login_with.return_value = lp
        main(['1'])
    captured = capsys.readouterr()
    assert 'LP: #1' in captured.out
    assert 'This is the title of a bug' in captured.out
