from twisted.conch.ssh.transport import DISCONNECT_BY_APPLICATION
from twisted.conch.interfaces import ISession
from twisted.conch.error import ConchError
from twisted.internet import reactor
from twisted.python import log
from zope import interface

import shlex

MOTD = r'''
  ___ ___ ___      ___
 / __|_ _/ __|___ / __|__ _ _ __  ___
 \_ \ | (_ |___| (_ / _` | '  \ -_)
 |___/___\__|    \__\_,_|_|_|_\__|

Well hello, {username}. You've successfully SSH'd to SIG-Game's
git server. Unfortunately, we don't offer shell access.
'''.replace('\n', '\r\n')

BAD_COMMAND = 'Received bad git command.'


class GitSession(object):
    interface.implements(ISession)

    def __init__(self, user):
        self.user = user

    def _disconnect(self, message, short_message, log_str=None):
        if log_str is None:
            log_str = short_message
        log.msg(log_str)
        self.user.conn.transport.sendDisconnect(
            DISCONNECT_BY_APPLICATION,
            message
        )

    def getPty(self, term, windowSize, modes):
        pass

    def openShell(self, proto):
        self._disconnect(MOTD.format(username=self.user.username),
                         'Shell access is not allowed',
                         '%s attemted shell access' % self.user.username)

    def execCommand(self, proto, cmd):
        try:
            # Split the git command. Should only be git-upload-pack
            # or git-receive-pack.
            git_command, reponame = shlex.split(cmd)
            assert git_command in ('git-upload-pack', 'git-receive-pack')
        except (ValueError, AssertionError):
            # If there's a problem with the command, disconnect
            # immediately.
            log_msg = 'Bad command by %s: "%s"' % (self.user.username, cmd)
            self._disconnect(BAD_COMMAND, 'Bad command', log_msg)
            return

        # Check permissions by mapping requested path to file system path
        repopath = self.user.meta.repopath(self.user.username, reponame)
        if repopath is None:
            msg = "Bad reponame: %s" % reponame
            self._disconnect(msg, '', msg)
            return

        command = ' '.join([git_command,  "'{0}'".format(repopath)])
        reactor.spawnProcess(proto, self.user.shell,
                             args=[self.user.shell, '-c', command])

    def windowChanged(self, newWindowSize):
        pass

    def eofReceived(self):
        pass

    def closed(self):
        pass
