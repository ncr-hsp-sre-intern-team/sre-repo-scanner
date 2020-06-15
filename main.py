import re
import sys
from github import Github


def isValidRepoName(repoName, prodList=None):
    """Test if a repo name string conforms to the naming convention

    The format of the repo name must match "<product>-<description>".
    1. Legal characters include:
       * -, _, digits 0-9
       * lower case letters
       * upper case letters
    2. <product> must be one listed in prodList.
       If prodList is None, this rule is not enforced.
    Examples: "nolo-online-ordering", "enterprise-insight", "ncr-mp", "ncr-mobilepay".
    Args:
        repoName: string, name of the repository to test.
        prodList: list of strings,
    Returns:
        a boolean indicating if the repo name conforms to the naming convention
    """
    prog = re.compile(r"""( \w+ )     # product
                          ( - \w+ )+  # hyphen and desription""", re.VERBOSE)
    product = re.split(r'-', repoName)[0]
    return (re.fullmatch(prog, repoName) is not None) and \
           (prodList is None or product in prodList)


def testRequestRemote(token, orgName, prodList=None):
    g = Github(token)
    org = g.get_organization(orgName)

    for idx, repo in enumerate(org.get_repos()):
        print('***** Repo #%d *****' % idx)
        print('Name:', repo.name)
        print('Valid: %r' % isValidRepoName(repo.name, prodList=prodList))
        print()


def testString(cases, expects, prodList=None):
    total, numCorrect = 0, 0
    for case, expect in zip(cases, expects):
        total = total + 1
        correct = isValidRepoName(case, prodList=prodList) == expect
        if correct:
            numCorrect = numCorrect + 1
        print('Case: \'{}\' Expect: {} Pass: {}'.format(case, expect, correct))
    print('***** Test complete %d/%d.*****' % (numCorrect, total))


if __name__ == '__main__':

    prodList = [
        'ncr',
        'hello',
        'sre'
    ]

    # 1. Test with remote repos
    token = sys.argv[1]
    orgName = 'ncr-hsp-sre-intern-team'
    testRequestRemote(token, orgName, prodList)

    # 2. String test
    casesExpects = [
        ('', False),
        ('_', False),
        ('-', False),
        ('ncr', False),
        ('nolo-', False),
        ('-mp', False),
        ('ncr-3', True),
        ('_-nolo', False),
        ('ncr-nolo', True),
        ('ncr-nolo_2-', False),
        ('ncr-nolo_2-end', True),
        ('ncr-nolo?', False),
        ('ncr,ncr', False)
    ]
    testString([caseExpect[0] for caseExpect in casesExpects], \
               [caseExpect[1] for caseExpect in casesExpects], \
               prodList)
    