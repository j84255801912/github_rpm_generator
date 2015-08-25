#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
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

    def _create_temp_template_file(self, change_log):
        """
            Create the temp template_file added new change_log
        """

        with open('template.spec', 'r') as f_r, \
             open('temp_template.spec', 'w') as f_w:
            for line in f_r:
                if '{ggggg3}' in line:
                    line = re.sub('{ggggg3}', '{ggggg3}\n' + change_log, line)
                f_w.write(line)

    def _create_specfile(self, specfile_path, date, change_log, g_downloader):

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

    def handle_specfile(self, g_downloader):

        print "\n\n\n\nCreating specfile...\n"

        specfile_path = "%s/dencs.spec" % SPEC_PATH
        date = time.strftime("%Y%m%d")
        name = raw_input("Enter your name : [Mai-Hsuan Chia] ")
        if name == "":
            name = "Mai-Hsuan Chia"
        email = raw_input("Enter your email : [j84255801912@gmail.com] ")
        if email == "":
            email = "j84255801912@gmail.com"

        week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        date_detailed = "{} {} {}".format(
                            week[datetime.datetime.today().weekday()],
                            time.strftime("%B")[:3], time.strftime("%d %Y")
                        )
        change_log1 = "* {} {} <{}> - 0.0.{}git{}\n".format(date_detailed,
                        name, email, date, g_downloader.get_commit()[:7]
                      )
        change_log2 = "- Use the latest commit in branch {}\n".format(
                        g_downloader.get_branch()
                      )
        temp_log = raw_input("Adding change_log to specfile : [{}]\n> ".format(
                                change_log2[:-1]
                             )
                   )
        if temp_log != "":
            change_log = change_log1 + temp_log + "\n"
        else:
            change_log = change_log1 + change_log2

        self._create_temp_template_file(change_log)
        self._create_specfile(specfile_path, date, change_log, g_downloader)

    def run_rpmbuild(self):

        rpmbuild_dir = os.path.dirname(os.path.abspath(__file__)) + "/rpmbuild"

        success = subprocess.call(["rpmbuild", "--define",
                                   "_topdir %s" % rpmbuild_dir,
                                   "-bb", # only generate rpm.
                                   SPEC_PATH + "/dencs.spec"])

        print "\n\n\n\nRpmbuild done, rpm is in rpmbuild/RPMS/\n"

        answer = raw_input('Add new change_log to template.spec ? [y] ')
        if answer == "" or answer[0] != 'n':
            os.rename('template.spec', 'template.spec.bk')
            os.rename('temp_template.spec', 'template.spec')


if __name__ == '__main__':

    c = GithubArchiveDownloader('OpenNetworking', 'gcoin')

    g = GenerateRpm()
    g.download_resources(c)
    g.handle_specfile(c)
    g.run_rpmbuild()
