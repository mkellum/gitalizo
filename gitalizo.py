# !/usr/bin/python

import csv
import subprocess
import sys
import time
from urlparse import urlparse


def main():
    log = Log()

    try:
        repo_index = int(sys.argv[1])
        if not repo_index or len(sys.argv) != 2:
            raise Exception("Incorrect arguments: {}".format(sys.argv))

        reader = csv.reader(open('repo_list.csv', 'r'))

        repo_row = None
        for i, row in enumerate(reader):
            if i == repo_index:
                repo_row = row
                break

        if not repo_row:
            raise Exception("Could not find row: {}".format(repo_index))

        r = Repo(repo_row)
        r.download(log)
        r.analyze(log)
        r.yamlToCSV(log)

    except Exception as e:
        log.add(str(e))
        sys.exit(1)


class Log:
    def __init__(self):
        file_name = 'gitalizo_log_{}'.format(int(time.time()))
        self.file = open(file_name, 'a+')
        self.add("Started Log")

    def end_log(self):
        self.add("Finished Log".format(time.ctime()))
        self.file.close()

    def add(self, m):
        self.file.write("{}: {}\n".format(time.ctime(), m))


class Repo:
    HTTPS_TEMPLATE = 'https://github.com/{}.git'

    def __init__(self, repo_row):
        self.id = repo_row[0]
        self.url = Repo.HTTPS_TEMPLATE.format(urlparse(repo_row[1]).path[7:])

    def download(self, log):
        log.add("Cloning repo {}".format(self.id))
        cmd = ['git', 'clone', self.url, './repo{}'.format(self.id)]
        log.add(subprocess.check_output(cmd))
        log.add("Done cloning")

    def analyze(self, log):
        log.add("Analyzing repo {}".format(self.id))
        cmd = ['analizo', 'metrics', './repo{}'.format(self.id), '-o', self.id]
        log.add(subprocess.check_output(cmd))
        log.add("Done analyzing")

    def yamlToCSV(self, log):
        log.add("Converting Analizo's YAML to CSV for repo {}".format(self.id))
        AnalizoToSQLCSV(self.id)
        log.add("Done converting")

    # Takes a YAML file output by Analizo (filename should be '<repoID>.yaml')
    def AnalizoToSQLCSV(self, analizo_metrics_file):
        fileLines = open(analizo_metrics_file).readlines()
        repoID = analizo_metrics_file[:-5]

        repoMetrics = []
        lineIndex = 1  # skip first '---' line
        line = fileLines[lineIndex]
        while ('---' not in line):
            splitLine = line.split(':')
            metric = splitLine[1].strip()
            repoMetrics.append(metric)
            lineIndex += 1
            line = fileLines[lineIndex]

        self.WriteRepoCSVFile(repoMetrics)

    # Writes repo-level metrics as a row to repoMetrics.csv
    # (appending or creating if it does not already exist)
    def WriteRepoCSVFile(self, metrics_list):
        repoMetricsFile = 'repoMetrics.csv'

        CSVrow = self.id + ','
        for metric in metrics_list:
            CSVrow += metric + ','
        CSVrow = CSVrow[:-1]  # strip the trailing comma

        CSVfile = open(repoMetricsFile, 'a+')
        CSVfile.write(CSVrow + '\n')

        CSVfile.close()


if __name__ == '__main__':
    main()
