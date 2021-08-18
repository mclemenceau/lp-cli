#!/usr/bin/python3
# Simple LaunchPad Bug object used to store some informations from LaunchPad
# into a structure that can be stored in and out of a json file

ubuntu_devel = 'Impish'

ubuntu_version = {
    ubuntu_devel: '21.10',
    'Hirsute': '21.04',
    'Groovy': '20.10',
    'Focal': '20.04',
    'Bionic': '18.04',
    'Xenial': '16.04',
    'Trusty': '14.04',
    'Precise': '12.04'
}

class lp_bug():
    def __init__(self, id, lp_api):
        if type(id) is not int:
            raise TypeError("bug id should be an integer")
        self.id = id

        if not lp_api:
            raise ValueError("Error with Launchpad API")

        self.api = lp_api

        self.bug = self.api.bugs[self.id]

    def __repr__(self):
        return "{%d, %s}" % (self.id, self.title)

    @property
    def title(self):
        return self.bug.title

    @property
    def desc(self):
        return self.bug.description

    def affected_packages(self):
        """
        return list of packages affected by this bug in a form of string list
        ['pkg1', 'pkg2' , 'pkg3']
        """
        return [x.bug_target_name.split()[0]
                for x in self.bug.bug_tasks
                if "(Ubuntu)" in x.bug_target_name]

    def affected_series(self, package):
        """
        Returns a list of string containing the series affected by a specific
        bug for a specific package: ['Impish', 'Focal', 'Bionic']
        """
        series = []
        for task in self.bug.bug_tasks:
            task_name = task.bug_target_name
            if package + " (Ubuntu" in task_name:
                serie = task_name[task_name.index("Ubuntu")+7:-1]
                if serie == '':
                    series.append(ubuntu_devel)
                elif serie in ubuntu_version.keys():
                    series.append(serie)

        return series


    def affected_versions(self, package):
        """
        Simply return all the affected version for a specific package affected
        by this bug. Convert affected serie into a version number
        """
        return [ubuntu_version.get(x) for x in self.affected_series(package)]
