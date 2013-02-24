from twisted.python import log
from zope import interface
from urlparse import urljoin

import requests
import re


class IGitMeta(interface.Interface):
    'API for authentication and access control.'

    def checkPassword(self, team_login, password):
        '''
        Given a team_login and a password, return true if the password
        is correct, else false.
        '''

    def repopath(self, team_login, reponame):
        '''
        Given a team_login and repo name, return the full path of the repo on
        the file system.
        '''


class GitMeta(object):
    interface.implements(IGitMeta)

    TEAMID_RE = re.compile(r'^.*-(?P<teamid>\d+)$')
    REPONAME_RE = re.compile(r'^(?P<repo_name>.*)__\d+\.git$')

    def __init__(self, webserver_address):
        self.webserver_address = webserver_address
        self.auth_url = urljoin(self.webserver_address, "api/repo/auth/")
        self.path_url = urljoin(self.webserver_address, "api/repo/path/")

    def checkPassword(self, team_login, password):
        try:
            teamid = self.TEAMID_RE.match(team_login).group('teamid')
            resp = requests.get(self.auth_url, params={'teamid': teamid,
                                                       "password": password})
            # If the password matches, we get a 200 back. Otherwise,
            # we get a 4XX
            return resp.status_code == 200
        except AttributeError:
            log.msg("Couldn't get the team's id: %s" % team_login)
            # Team ID wasn't in team_login
            return False

    def repopath(self, team_login, reponame):
        try:
            teamid = self.TEAMID_RE.match(team_login).group('teamid')
            resp = requests.get(self.path_url, params={'teamid': teamid})
            full_path = resp.json()['repository']['path']
            pretty_path = self.REPONAME_RE.sub(r'\g<repo_name>.git', full_path)

            # Make sure tat the full path ends with the path that the
            # user is trying to access.
            if pretty_path.endswith(reponame):
                return full_path

            return None
        except AttributeError:
            # Team ID wasn't in team_login
            return None
        except ValueError:
            # JSON couldn't be decoded
            return None
        except KeyError:
            # Received bad data from webserver
            return None
