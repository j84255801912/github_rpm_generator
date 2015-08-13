#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import datetime
import urllib2

from github_archive_downloader import GithubArchiveDownloader

"""
    This script do
    1. download source packages.
    2. generate a new specfile using template specfile.
    3. run rpmbuild and generate rpmpackage.
"""

TEMPLATE_SPECFILE_PATH = "./template.spec"
OPENSSL_VERSION = "1.0.2d"
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

    def create_specfile(self, g_downloader):

        print "Creating specfile..."
        specfile_path = "%s/dencs.spec" % SPEC_PATH
        date = time.strftime("%Y%m%d")
        name = raw_input("Enter your name : ")
        email = raw_input("Enter your email : ")

        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        date_detail = "{} {} {}".format(week[datetime.datetime.today().weekday()],
                        time.strftime("%B")[:3], time.strftime("%m %Y")
                      )
        change_log = "* {} {} <{}> - 0.0.{}git{}\n".format(date_detail,
                        name, email, date, g_downloader.get_commit()[:7]
                     )
        change_log += "- Use the latest commit in branch no_fee_DEV\n"

        with open('template.spec', 'r') as f_r, \
             open(specfile_path, 'w') as f_w:
            for line in f_r:
                if '{ggggg1}' in line:
                    line = re.sub('{ggggg1}', g_downloader.get_commit(), line)
                if '{ggggg2}' in line:
                    line = re.sub('{ggggg2}', date, line)
                if '{ggggg3}' in line:
                    line = re.sub('{ggggg3}', change_log, line)
                f_w.write(line)


if __name__ == '__main__':

    c = GithubArchiveDownloader('OpenNetworking', 'gcoin')
    g = GenerateRpm()
#    g.download_resources(c)
    g.create_specfile(c)
