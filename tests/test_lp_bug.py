import pytest

from unittest import TestCase
from unittest.mock import Mock

from LpCli.lp_bug import lp_bug, ubuntu_devel


class test_lp_bug(TestCase):

    def setUp(self):
        self.bug1 = Mock()
        self.bug1.title = "This is the title of a bug"
        self.bug1.description = "This is the longer description of a bug"

        self.task1 = Mock()
        self.task2 = Mock()
        self.task3 = Mock()
        self.task4 = Mock()
        self.task5 = Mock()
        self.task6 = Mock()
        self.task7 = Mock()
        self.task8 = Mock()
        self.task9 = Mock()
        self.task10 = Mock()
        self.task11 = Mock()

        self.task1.bug_target_name = 'systemd (Ubuntu)'
        self.task2.bug_target_name = 'vim (Debian)'
        self.task3.bug_target_name = 'glibc (Ubuntu)'
        self.task4.bug_target_name = 'glibc (Ubuntu Focal)'
        self.task5.bug_target_name = 'glibc (Ubuntu None)'
        self.task6.bug_target_name = 'glibc !@#$)'
        self.task7.bug_target_name = 'systemd (Ubuntu Focal)'
        self.task8.bug_target_name = 'systemd (Ubuntu Bionic)'
        self.task9.bug_target_name = 'glibc (Ubuntu Bionic)'

        self.task10.bug_target_name = 'casper (Ubuntu)'
        self.task11.bug_target_name = 'casper (Ubuntu '+ubuntu_devel+')'


        self.lp = Mock()
        self.lp.bugs = {1234567: self.bug1}

    def tearDown(self):
        pass

    def test_bug_init_bad_lp_api(self):
        with pytest.raises(ValueError):
            return lp_bug(1234567, None)

    def test_bug_init_bad_bug(self):
        with pytest.raises(TypeError):
            return lp_bug("bad", self.lp)

    def test_default_init(self):
        bug = lp_bug(1234567, self.lp)
        self.assertEqual(bug.id, 1234567)
        self.assertEqual(bug.title, "This is the title of a bug")
        self.assertEqual(bug.desc, "This is the longer description of a bug")

    def test_affected_packages(self):
        bug = lp_bug(1234567, self.lp)

        self.bug1.bug_tasks = [self.task1, self.task2, self.task3]
        packages = bug.affected_packages()
        self.assertEqual(len(packages), 2)
        self.assertListEqual(
            packages, ['systemd', 'glibc'])

        self.bug1.bug_tasks = [self.task1, self.task7, self.task8]
        packages = bug.affected_packages()
        self.assertEqual(len(packages), 1)
        self.assertListEqual(
            packages, ['systemd'])

    def test_affected_series(self):
        bug = lp_bug(1234567, self.lp)

        self.bug1.bug_tasks = [
                            self.task1, self.task2, self.task3,
                            self.task4, self.task5, self.task6,
                            self.task7, self.task8, self.task9]

        # Simple default series test
        series = bug.affected_series('systemd')
        self.assertEqual(len(series), 3)
        self.assertListEqual(
            series, ['Impish', 'Focal', 'Bionic'])

        # Wrong Serie vim (Debian)
        series = bug.affected_series('vim')
        self.assertEqual(len(series), 0)

        # Bad Serie glibc !@#$)
        series = bug.affected_series('glibc')
        print(series)
        self.assertEqual(len(series), 3)

    def test_affected_series_double(self):
        bug = lp_bug(1234567, self.lp)

        self.bug1.bug_tasks = [self.task10, self.task11]

        series = bug.affected_series('casper')
        self.assertEqual(len(series), 1)
        self.assertListEqual(
            series, ['Impish'])

    def test_affected_versions(self):
        bug = lp_bug(1234567, self.lp)

        self.bug1.bug_tasks = [
                            self.task1, self.task2, self.task3,
                            self.task4, self.task5, self.task6,
                            self.task7, self.task8, self.task9]

        versions = bug.affected_versions('systemd')

        self.assertEqual(len(versions), 3)
        self.assertListEqual(
            versions, ['21.10', '20.04', '18.04'])

        versions = bug.affected_versions('vim')

        self.assertEqual(len(versions), 0)

        versions = bug.affected_versions('glibc')

        self.assertEqual(len(versions), 3)
        self.assertListEqual(
            versions, ['21.10', '20.04', '18.04'])

