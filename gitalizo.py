# !/usr/bin/python

import csv
import os
import subprocess
import sys
import time
from urlparse import urlparse

LOG_DIR = 'logs'


def main():
    make_dirs([LOG_DIR, Repo.ANALIZO_OUTS, Repo.REPO_TEMP])
    start_log(LOG_DIR)

    repo_list_file = sys.argv[1]

    if not repo_list_file or len(sys.argv) != 2:
        sys.exit("Usage: gitalizo <repo id filename>")

    for repo_row in csv.reader(open(repo_list_file, 'r')):
        r = Repo(repo_row[0], repo_row[1])
        r.download()
        if r.should_analyze():
            r.analyze()
        r.clean()


def make_dirs(dirs):
    for d in dirs:
        try:
            os.stat(d)
        except:
            os.mkdir(d)


def start_log(log_dir):
    # noinspection PyGlobalUndefined
    global log
    log_path = os.path.join(log_dir, 'gitalizo_log_{}'.format(int(time.time())))
    log = open(log_path, 'a+')
    log.write("Started at {}\n".format(time.ctime()))


def end_log():
    log.write("Finished at {}\n".format(time.ctime()))
    log.close()

class Repo:
    ANALIZO_OUTS = 'analizo_outs'
    REPO_TEMP = 'repo_temp'
    URL_TEMPLATE = 'https://github.com{}.git'

    def __init__(self, repo_id, repo_url):
        self.id = repo_id
        self.url = Repo.URL_TEMPLATE.format(urlparse(repo_url).path[6:])
        self.clone_dir = os.path.join(Repo.REPO_TEMP, self.id)
        self.out_file = os.path.join(Repo.ANALIZO_OUTS, self.id)
        make_dirs([self.clone_dir])

    def download(self):
        log.write("Cloning repo {}\n".format(self.id))

        cmd = ['git', 'clone', self.url, self.clone_dir]

        log.write(subprocess.check_output(cmd))
        log.write("Done cloning\n")

    def analyze(self):
        log.write("Analyzing repo {}\n".format(self.id))

        cmd = ['analizo', 'metrics', self.clone_dir, '-o', self.out_file]

        log.write(subprocess.check_output(cmd))
        log.write("Done analyzing\n")

    def clean(self):
        log.write("Cleaning up after repo {}\n".format(self.id))

        cmd = ['rm', '-rf', self.clone_dir]

        log.write(subprocess.check_output(cmd))
        log.write("Done cleaning up\n")

    def should_analyze(self):
        # placeholder for smarter function to weed out bad repos
        return True


if __name__ == '__main__':
    main()
