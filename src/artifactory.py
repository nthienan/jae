import logging

import requests


class Artifactory:
    def __init__(self, url, access_token, **kwargs):
        if url.endswith("/"):
            url = url.s[:-1]
        self.url = url
        logging.debug("Initialize Artifactory: url: %s, accessToken: ****, %s" % (url, kwargs))
        self.access_token = access_token
        self.kwargs = kwargs
        self.authenticate_header = {"Authorization": "Bearer %s" % self.access_token}

    def get_storage_info(self):
        logging.debug("Getting storage info...")
        url = "%s/api/storageinfo" % self.url
        res = requests.get(url=url, headers=self.authenticate_header, **self.kwargs)
        res.raise_for_status()
        return res.json()

    def get_users(self):
        logging.debug("Getting users info...")
        url = "%s/api/security/users" % self.url
        res = requests.get(url=url, headers=self.authenticate_header, **self.kwargs)
        res.raise_for_status()
        return res.json()
