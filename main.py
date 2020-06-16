"""
This module small demo of fetching organization repos and perform a simple
naming scan on every single one of all repos.
"""
import re
import sys
from github import Github


def is_valid_repo_name(repo_name, prod_list=None):
    """
    Test if a repo name string conforms to the naming convention

    The format of the repo name must match "<product>-<description>".
    1. Legal characters include:
       * -, _, digits 0-9
       * lower case letters
       * upper case letters
    Examples: "nolo-online-ordering", "enterprise-insight", "ncr-mp",
      "ncr-mobilepay" are valid for this rule.
    2. <product> must be one listed in prod_list.
       If prod_list is None, this rule is not enforced.
    Args:
        repo_name: string, name of the repository to test.
        prod_list: list of strings,
    Returns:
        a boolean indicating if the repo name conforms to the naming convention
    """
    prog = re.compile(r"""( \w+ )     # product
                          ( - \w+ )+  # hyphen and desription""", re.VERBOSE)
    product = re.split(r'-', repo_name)[0]
    return (re.fullmatch(prog, repo_name) is not None) and \
           (prod_list is None or product in prod_list)


def test_request_remote(token, org_name, prod_list=None):
    """
    Test scan remote repos
    """
    github = Github(token)
    org = github.get_organization(org_name)
    print(list(org.get_repos()))

    for idx, repo in enumerate(org.get_repos()):
        print('***** Repo #%d *****' % idx)
        print('Name:', repo.name)
        print('Valid: %r' % is_valid_repo_name(repo.name, prod_list=prod_list))
        print()


def test_string(cases, expects, prod_list=None):
    """
    Dummy string test
    """
    total, num_correct = 0, 0
    for case, expect in zip(cases, expects):
        total = total + 1
        correct = is_valid_repo_name(case, prod_list=prod_list) == expect
        if correct:
            num_correct = num_correct + 1
        print('Case: \'{}\' Expect: {} Pass: {}'.format(case, expect, correct))
    print('***** Test complete %d/%d.*****' % (num_correct, total))


if __name__ == '__main__':

    PROD_LIST = [
        'ncr',
        'hello',
        'sre',
        'test'
    ]

    # 1. Test with remote repos
    TOKEN = sys.argv[1]
    ORG_NAME = 'ncr-swt-hospitality'
    test_request_remote(TOKEN, ORG_NAME, PROD_LIST)

    # 2. String test
    CASES_EXPECTS = [
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
    test_string([case_expect[0] for case_expect in CASES_EXPECTS],
                [case_expect[1] for case_expect in CASES_EXPECTS],
                PROD_LIST)
