import configparser

import os
from ..utils import die_msg, PROG_NAME, get_data_dir


class PdaConfig:
    """
    ``PdaConfig`` is a class which implements configuration abstraction 
    for ``ListDB`` class in ``GithubIssues`` module.

    """

    DEFAULTS = {
        "database-path": str((get_data_dir() / "pda_database").absolute()),
        "username": None,
        "repo-name": None,
        "auth-token": None,
    }

    def __init__(self, test_cfg=None):
        """
        :param test_cfg: :class: `file <file>` object or None
        """

        try:
            # load configurations from several possible locations
            self._config = configparser.RawConfigParser(self.DEFAULTS)

            if not test_cfg:
                self._config.read([os.path.expanduser("~/.pdaconfig")])
            else:
                self._config.read_file(test_cfg)

        except configparser.ParsingError as err:
            # crash pda when configuration file is ill-formatted
            die_msg(PROG_NAME, msg=err)

    @property
    def local_db_path(self):
        """local_db_path attribute getter
        """

        try:
            path = self._config.get("pda", "database-path")
        except configparser.NoSectionError or configparser.DuplicateSectionError:
            path = self.DEFAULTS["database-path"]

        return path if path != "" else self.DEFAULTS["database-path"]

    @property
    def username(self):
        """username attribute getter
        """

        try:
            name = self._config.get("github", "username")
        except configparser.NoSectionError or configparser.DuplicateSectionError:
            name = self.DEFAULTS["username"]

        return name if name != "" else self.DEFAULTS["username"]

    @property
    def reponame(self):
        """reponame attribute getter
        """

        try:
            name = self._config.get("github", "repo-name")
        except configparser.NoSectionError or configparser.DuplicateSectionError:
            name = self.DEFAULTS["repo-name"]

        return name if name != "" else self.DEFAULTS["repo-name"]

    @property
    def authtoken(self):
        """authtoken attribute getter
        """

        try:
            token = self._config.get("github", "auth-token")
        except configparser.NoSectionError or configparser.DuplicateSectionError:
            token = self.DEFAULTS["auth-token"]

        return token if token != "" else self.DEFAULTS["auth-token"]

    @property
    def remote_mode(self):
        """remote_mode attribute getter
        """

        return (
            (self.username is not None)
            and (self.reponame is not None)
            and (self.authtoken is not None)
        )
