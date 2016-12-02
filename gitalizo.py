# !/usr/bin/python

import csv
import os
import subprocess
import sys
import time
from urlparse import urlparse


def main():
    os.chdir('/home/kellum')

    # number in sequence (from condor), 0-indexed
    proc_num = int(sys.argv[1])

    # our bite size per proc - constant per submit!
    repos_per_proc = int(sys.argv[2])

    if proc_num == None or repos_per_proc == None:
        sys.exit("Incorrect arguments: {}".format(sys.argv))

    start_i = proc_num * repos_per_proc
    end_i = start_i + repos_per_proc

    print "Will analyze rows {} to {}".format(start_i, end_i)

    reader = csv.reader(open('./repo_list.csv', 'r'))
    for i, row in enumerate(reader):
        if i >= end_i:
            break
        if i >= start_i:
            print "Starting row {}".format(i)
            try:
                r = Repo(row)
                r.download()
                r.analyze()
                r.yamlToCSV()
                r.cleanup()
            except Exception as e:
                print str(e)


class Repo:
    HTTPS_TEMPLATE = 'https://dummy24601:cafn9w0qrudls@github.com/{}.git'
    # SSH_TEMPLATE = 'git@github.com:{}.git'

    def __init__(self, repo_row):
        self.id = repo_row[0]
        self.url = Repo.HTTPS_TEMPLATE.format(urlparse(repo_row[1]).path[7:])
        # self.url = Repo.SSH_TEMPLATE.format(urlparse(repo_row[1]).path[7:])

    def download(self):
        print "Cloning repo {}".format(self.id)

        cmd = ['git','clone',self.url,'./repo{}'.format(self.id)]
        sp_output = subprocess.check_output(cmd)
        if sp_output:
            print sp_output

        print "Done cloning"

    def analyze(self):
        print "Analyzing repo {}".format(self.id)

        cmd = ['analizo','metrics','./repo{}'.format(self.id),'-o','./{}'.format(self.id)]
        sp_output = subprocess.check_output(cmd)
        if sp_output:
            print sp_output

        print "Done analyzing"

    def yamlToCSV(self):
        print "Converting Analizo's YAML to CSV for repo {}".format(self.id)

        repoMetrics = []
        for line in open('./{}'.format(self.id)).readlines()[1:]:
            if ('---' not in line):
                break
            splitLine = line.split(':')
            metric = splitLine[1].strip()
            repoMetrics.append(metric)

        self.WriteRepoCSVFile(repoMetrics)

        print "Done converting"

    # Writes repo-level metrics as a row to repoMetrics.csv
    # (appending or creating if it does not already exist)
    def WriteRepoCSVFile(self, metrics_list):
        repoMetricsFile = './repo_metrics/{}.csv'.format(self.id)

        CSVrow = self.id + ','
        for metric in metrics_list:
            CSVrow += metric + ','
        CSVrow = CSVrow[:-1]  # strip the trailing comma

        CSVfile = open(repoMetricsFile, 'a+')
        CSVfile.write(CSVrow + '\n')

        CSVfile.close()

    def cleanup(self):
        print "Cleaning up after repo {}".format(self.id)

        cmd = ['rm','-rf','./repo{}'.format(self.id)]
        sp_output = subprocess.check_output(cmd)
        if sp_output:
            print sp_output

        cmd = ['rm','-rf',self.id]
        sp_output = subprocess.check_output(cmd)
        if sp_output:
            print sp_output

        print "Done cleaning up"


if __name__ == '__main__':
    main()
