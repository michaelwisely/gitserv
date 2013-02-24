from twisted.cred.credentials import IUsernamePassword
from twisted.cred.checkers import ICredentialsChecker
from twisted.cred import credentials, error
from twisted.python import log, failure
from twisted.internet import defer
from zope import interface

import sys


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

    def _verify_with_webserver(self, login, passwd):
        print login
        log.msg("Attempted auth %s: %s\n" % (login, passwd))
        # Make a connection to the specified URL
        # TODO implement real password checking
        return login == passwd

    def requestAvatarId(self, user_credentials):
        log.msg("Getting avatar id")
        # Create a deferred to check the password
        d = defer.maybeDeferred(self._verify_with_webserver,
                                str(user_credentials.username),
                                str(user_credentials.password))
        return d.addCallback(self._cbPasswordMatch,
                             str(user_credentials.username))
