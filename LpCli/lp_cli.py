from launchpadlib.launchpad import Launchpad
from optparse import OptionParser
from LpCli.lp_bug import lp_bug

def main():
    usage = """\
    usage: lp-cli bug_id

    Ex: lp-cli 1934747
    """
    opt_parser = OptionParser(usage)
    opts, args = opt_parser.parse_args()

    if len(args) >= 1:
        lp = Launchpad.login_with('foundations', 'production', version='devel')


        bug = lp_bug(int(args[0]),lp)

        print(bug)

        return 0

    return 1

