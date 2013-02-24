from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key


class GitServer(SSHFactory):

    def __init__(self, private_key_path, public_key_path):
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    def getPrivateKeys(self):
        return {'ssh-rsa': Key.fromFile(self.private_key_path)}

    def getPublicKeys(self):
        return {'ssh-rsa': Key.fromFile(self.public_key_path)}
