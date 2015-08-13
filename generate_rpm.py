#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2

from github_archive_downloader import GithubArchiveDownloader

"""
    This script do
    1. download source packages.
    2. generate a new specfile using template specfile.
    3. run rpmbuild and generate rpmpackage.
"""

TEMPLATE_SPECFILE_PATH = "./template.spec"
OPENSSL_VERSION = "1.0.1l"
BDB_VERSION = "5.3.28"
SOURCE_PATH = "rpmbuild/SOURCES"
SPEC_PATH = "rpmbuild/SPECS"

class GenerateRpm(object):

    def _download_resource(self, url, file_path):

        print url
        print file_path
        request = urllib2.Request(url)

        result = urllib2.urlopen(request)
        content = result.read()

        with open(file_path, 'w') as f:
            f.write(content)

    def _download_openssl(self):

        openssl_url = "https://www.openssl.org/source/openssl-{}.tar.gz".format(
                        OPENSSL_VERSION
                      )
        openssl_file_path = "{}/openssl-{}.tar.gz".format(SOURCE_PATH,
                                OPENSSL_VERSION
                            )
        if not os.path.isfile(openssl_file_path):
            print "\nDownloading openssl..."
            self._download_resource(openssl_url, openssl_file_path)

    def _download_bdb(self):

        bdb_url = "http://download.oracle.com/berkeley-db/db-{}.tar.gz".format(
                        BDB_VERSION
                  )
        bdb_file_path = "{}/db-{}.tar.gz".format(SOURCE_PATH, BDB_VERSION)
        if not os.path.isfile(bdb_file_path):
            print "\nDownloading bdb..."
            self._download_resource(bdb_url, bdb_file_path)

    def _download_gcoin(self, g_downloader):

        gcoin_file_path = "{}/gcoin-{}.tar.gz".format(SOURCE_PATH,
                            g_downloader.get_commit()
                          )
        if not os.path.isfile(gcoin_file_path):
            print "\nDownloading gcoin..."
            g_downloader.download_archive("./rpmbuild/SOURCES")

    def download_resources(self, g_downloader):
        """
            Download needed resources.
        """

        self._download_openssl()
        self._download_bdb()
        self._download_gcoin(g_downloader)

if __name__ == '__main__':

    c = GithubArchiveDownloader('OpenNetworking', 'gcoin')
    g = GenerateRpm()
    g.download_resources(c)
