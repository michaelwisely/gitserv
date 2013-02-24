from twisted.python import procutils

from .errors import GitServException

import logging
logger = logging.getLogger(__name__)


def get_git_shell():
    git_shells = procutils.which('git-shell')
    if git_shells == []:
        logger.error("Couldn't find git-shell. Raising exception.")
        raise GitServException("git-shell isn't installed...")
    if len(git_shells) > 1:
        logger.info("Found multiple git-shells. Using the first.")
    return git_shells[0]
