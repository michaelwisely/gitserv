from twisted.conch.avatar import ConchUser
from twisted.conch.ssh.session import SSHSession

from .utils import get_git_shell


class GitConchUser(ConchUser):
    shell = get_git_shell()

    def __init__(self, username, meta):
        ConchUser.__init__(self)
        self.username = username
        self.meta = meta
        self.channelLookup.update({"session": SSHSession})

    def logout(self):
        pass
