import argparse
from launchpadlib.launchpad import Launchpad

from LpCli.lp_bug import lp_bug


def main(args=None):
    parser = argparse.ArgumentParser(
        description="A script to query Launchpad bugs, e.g. lp-cli 1934747")
    parser.add_argument(
        'bug_id', type=int,
        help="The numeric identifier of the bug to query")
    config = parser.parse_args(args)

    lp = Launchpad.login_with('foundations', 'production', version='devel')
    bug = lp_bug(config.bug_id, lp)
    print(bug)

# =============================================================================
