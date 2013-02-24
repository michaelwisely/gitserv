from twisted.cred.checkers import ICredentialsChecker
from twisted.cred import credentials, error
from twisted.python import log, failure
from twisted.internet import defer
from zope import interface


class TeamPasswordChecker(object):
    interface.implements(ICredentialsChecker)

    credentialInterfaces = ( credentials.IUsernamePassword, )

    def __init__(self, meta):
        self.meta = meta

    def _cbPasswordMatch(self, matched, username):
        if matched:
            return username
        else:
            return failure.Failure(error.UnauthorizedLogin())

    def requestAvatarId(self, user_credentials):
        # Create a deferred to check the password
        d = defer.maybeDeferred(self.meta.checkPassword,
                                str(user_credentials.username),
                                str(user_credentials.password))
        return d.addCallback(self._cbPasswordMatch,
                             str(user_credentials.username))
