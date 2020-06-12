from github import Github
import re


def isValidRepoName(repoName):
    prog = re.compile(r"""( [a-zA-Z] \w* )     # product
                          ( - [a-zA-Z] \w* )+  # hyphen and desription""", re.VERBOSE)
    return re.fullmatch(prog, repoName) is not None


def testRequestRemote(token):
    g = Github(token)
    user =  g.get_user()

    for idx, repo in enumerate(user.get_repos()):
        print('***** Repo #%d *****' % idx)
        
        print('Name:', repo.name)
        print('Valid: %r' % isValidRepoName(repo.name))

        print()


def testString(cases, expects):
    total, numCorrect = 0, 0
    for case, expect in zip(cases, expects):
        total = total + 1
        correct = isValidRepoName(case) == expect
        if correct:
            numCorrect = numCorrect + 1
        print('Case: \'{}\' Expect: {} Pass: {}'.format(case, expect, correct))
    print ('***** Test complete %d/%d.*****' % (numCorrect, total))


if __name__ == '__main__':

    # 1. Test with remote repos
    token = '6c9223d25aaca49ef9a118867b1bd3a40b083c85'
    testRequestRemote(token)
    
    # 2. String test
    casesExpects = [
        ('', False),
        ('_', False),
        ('-', False),
        ('ncr', False),
        ('nolo-', False),
        ('-mp', False),
        ('ncr-3', False),
        ('_-nolo', False),
        ('ncr-nolo', True),
        ('ncr-nolo_2-', False),
        ('ncr-nolo_2-end', True)
    ]
    testString([caseExpect[0] for caseExpect in casesExpects], [caseExpect[1] for caseExpect in casesExpects])
