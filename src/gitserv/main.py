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


PARSER = argparse.ArgumentParser(description='Run a git ssh server.')
PARSER.add_argument('private_key', type=str, nargs=1,
                    help="The path to the server's private key.")
PARSER.add_argument('public_key', type=str, nargs=1,
                    help="The path to the server's public key.")
PARSER.add_argument('webserver_address', type=str, nargs=1,
                    help="The address of the webserver.")
PARSER.add_argument('webserver_user', type=str, nargs=1,
                    help="The address of the webserver.")
PARSER.add_argument('webserver_password', type=str, nargs=1,
                    help="The address of the webserver.")
PARSER.add_argument('--port', dest='port', action='store', default=2222,
                    help='Specifies a port to listen on')


def run():
    args = PARSER.parse_args()

    # Unpack values. Each should be a list of one item (hence the
    # comma. Yay list unpacking)
    private_key, = args.private_key
    public_key, = args.public_key
    webserver_address, = args.webserver_address
    webserver_user, = args.webserver_user
    webserver_password, = args.webserver_password
    port = int(args.port)

    log.startLogging(sys.stderr)
    log.startLogging(open('gitssh.log', 'w'))

    components.registerAdapter(GitSession, GitConchUser, ISession)

    # Set up authorization
    GitServer.meta = GitMeta(webserver_address,
                             webserver_user, webserver_password)
    GitServer.portal = Portal(GitRealm(GitServer.meta))
    GitServer.portal.registerChecker(TeamPasswordChecker(GitServer.meta))

    # Instantiate a server
    server = GitServer(os.path.abspath(private_key),
                       os.path.abspath(public_key))

    # Start listening
    reactor.listenTCP(port, server)
    reactor.run()


if __name__ == '__main__':
    run()
