from zope import interface


class IGitMeta(interface.Interface):
    'API for authentication and access control.'

    def repopath(self, username, reponame):
        '''
        Given a username and repo name, return the full path of the repo on
        the file system.
        '''


class GitMeta(object):
    interface.implements(IGitMeta)

    def __init__(self):
        pass

    def repopath(self, username, reponame):
        return                  # Path to a repository
