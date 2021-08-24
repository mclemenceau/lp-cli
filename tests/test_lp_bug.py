import pytest

from unittest import TestCase
from unittest.mock import Mock

from LpCli.lp_bug import lp_bug, ubuntu_devel


class test_lp_bug(TestCase):

    def setUp(self):
        self.bug1 = Mock()
        self.bug1.title = "This is the title of a bug"
        self.bug1.description = "This is the longer description"
        self.bug1.heat = "100"
        self.bug1.importance = "Undecided"
        self.bug1.bug_tasks = []

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
        self.task1.status = 'New'
        self.task1.importance = 'Critical'
        self.task2.bug_target_name = 'vim (Debian)'
        self.task2.status = 'Confirmed'
        self.task3.bug_target_name = 'glibc (Ubuntu)'
        self.task3.status = 'New'
        self.task4.bug_target_name = 'glibc (Ubuntu Focal)'
        self.task4.status = 'Incomplete'
        self.task5.bug_target_name = 'glibc (Ubuntu None)'
        self.task5.status = 'Triaged'
        self.task6.bug_target_name = 'glibc !@#$)'
        self.task6.status = 'Incomplete'
        self.task7.bug_target_name = 'systemd (Ubuntu Focal)'
        self.task7.status = 'Fix Committed'
        self.task8.bug_target_name = 'systemd (Ubuntu Bionic)'
        self.task8.status = 'Fix Released'
        self.task9.bug_target_name = 'glibc (Ubuntu Bionic)'
        self.task9.status = 'Triaged'

        self.task10.bug_target_name = 'casper (Ubuntu)'
        self.task10.status = 'New'
        self.task11.bug_target_name = 'casper (Ubuntu '+ubuntu_devel+')'
        self.task11.status = 'Fix Released'

        self.lp = Mock()
        self.lp.bugs = {1234567: self.bug1}

    def tearDown(self):
        pass

    def test_bug_init_bad_lp_api(self):
        with pytest.raises(ValueError):
            return lp_bug(1234567, None)

    def test_bug_init_bad_type_bug(self):
        with pytest.raises(TypeError):
            return lp_bug("bad", self.lp)

    def test_bug_init_bad_bug_doesnt_exist(self):
        with pytest.raises(KeyError):
            return lp_bug(123456789, self.lp)

    def test_default_init(self):
        bug = lp_bug(1234567, self.lp)
        self.assertEqual(bug.id, 1234567)
        self.assertEqual(bug.title, "This is the title of a bug")
        self.assertEqual(bug.description, "This is the longer description")
        self.assertEqual(bug.heat, "100")

    def test_affected_packages(self):
        self.bug1.bug_tasks = [self.task1, self.task2, self.task3]
        bug = lp_bug(1234567, self.lp)

        packages = bug.affected_packages()
        self.assertEqual(len(packages), 2)
        self.assertListEqual(
            packages, ['systemd', 'glibc'])

        self.bug1.bug_tasks = [self.task1, self.task7, self.task8]
        bug = lp_bug(1234567, self.lp)
        packages = bug.affected_packages()
        self.assertEqual(len(packages), 1)
        self.assertListEqual(
            packages, ['systemd'])

    def test_affected_series(self):
        self.bug1.bug_tasks = [
                            self.task1, self.task2, self.task3,
                            self.task4, self.task5, self.task6,
                            self.task7, self.task8, self.task9]

        bug = lp_bug(1234567, self.lp)

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
        self.bug1.bug_tasks = [self.task10, self.task11]

        bug = lp_bug(1234567, self.lp)

        series = bug.affected_series('casper')
        self.assertEqual(len(series), 1)
        self.assertListEqual(
            series, ['Impish'])

    def test_affected_versions(self):
        self.bug1.bug_tasks = [
                            self.task1, self.task2, self.task3,
                            self.task4, self.task5, self.task6,
                            self.task7, self.task8, self.task9,
                            self.task10, self.task11]

        bug = lp_bug(1234567, self.lp)

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

    def test_package_detail(self):
        self.bug1.bug_tasks = [
                            self.task1, self.task2, self.task3,
                            self.task4, self.task5, self.task6,
                            self.task7, self.task8, self.task9,
                            self.task10, self.task11]

        bug = lp_bug(1234567, self.lp)

        # test with a missing serie and make sure it defaults to ubuntu_devel
        self.assertEqual(
            bug.package_detail("glibc", 'Focal', "status"), "Incomplete"
            )
        self.assertEqual(
            bug.package_detail("systemd", ubuntu_devel, "status"), "New"
            )
        # test for detail that doesn't exist
        self.assertEqual(
            bug.package_detail("systemd", ubuntu_devel, "age"), ""
            )

    def test_bug_str(self):
        bug = lp_bug(1234567, self.lp)
        bug_str = "LP: #1234567 : This is the title of a bug\nHeat: 100"
        self.assertEqual(str(bug),bug_str)

        self.bug1.bug_tasks = [self.task1]
        bug = lp_bug(1234567, self.lp)
        bug_str = "LP: #1234567 : This is the title of a bug\n"\
            "Heat: 100\n - systemd:\n   - Impish : New (Critical)"
        self.assertEqual(str(bug), bug_str)

    def test_bug_dict(self):
        bug = lp_bug(1234567, self.lp)
        bug_dict = {'id': 1234567,
                    'title': 'This is the title of a bug',
                    'packages': {}}

        self.assertDictEqual(bug.dict(), bug_dict)

    def test_bug_repr(self):
        bug = lp_bug(1234567, self.lp)
        bug_dict = {'id': 1234567,
                    'title': 'This is the title of a bug',
                    'packages': {}}

        self.assertEqual(bug.__repr__(), bug_dict.__str__())

# =============================================================================
