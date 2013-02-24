from twisted.python import components, log
from twisted.conch.ssh.session import ISession
from twisted.internet import reactor
from twisted.cred.portal import Portal

from .realm import GitRealm
from .meta import GitMeta
from .checkers import TeamPasswordChecker
from .server import GitServer
from .session import GitSession
from .avatar import GitConchUser

import os
import sys
import argparse

log.startLogging(sys.stderr)
log.startLogging(open('gitssh.log', 'w'))


PARSER = argparse.ArgumentParser(description='Run a git ssh server.')
PARSER.add_argument('private_key', type=str, nargs=1,
                    help="The path to the server's private key.")
PARSER.add_argument('public_key', type=str, nargs=1,
                    help="The path to the server's public key.")
PARSER.add_argument('webserver_hostname', type=str, nargs=1,
                    help="The hostname of the webserver")
PARSER.add_argument('--port', dest='port', action='store', default=2222,
                    help='Specifies a port to listen on')

def run():
    args = PARSER.parse_args()
    private_key, = args.private_key
    public_key, = args.public_key

    components.registerAdapter(GitSession, GitConchUser, ISession)

    # Set up authorization
    GitServer.meta = GitMeta()
    GitServer.portal = Portal(GitRealm(GitServer.meta))
    GitServer.portal.registerChecker(TeamPasswordChecker(GitServer.meta))

    # Instantiate a server
    server = GitServer(os.path.abspath(private_key),
                       os.path.abspath(public_key))

    # Start listening
    reactor.listenTCP(args.port, server)
    reactor.run()


if __name__ == '__main__':
    run()