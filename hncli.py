# /usr/bin/Python3

import requests
import json
import sys
import argparse
from collections import OrderedDict


# run this in the command line to set the encoding to UTF-8: 'chcp 65001'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        self.BOLD = ''
        self.UNDERLINE = ''


def getTopStoriesIDs(n=500):
    url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    r = requests.get(url)
    r.raise_for_status()

    topStories = json.loads(r.text)

    return topStories[0:n]


def getNewStoriesIDs(n=500):
    url = 'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty'
    r = requests.get(url)
    r.raise_for_status()

    newStories = json.loads(r.text)

    return newStories[0:n]


def getBestStoriesIDs(n=500):
    url = 'https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty'
    r = requests.get(url)
    r.raise_for_status()

    bestStories = json.loads(r.text)

    return bestStories[0:n]


def getStories(ids):
    stories = OrderedDict()
    i = 1

    for n in ids:
        url = 'https://hacker-news.firebaseio.com/v0/item/' + str(n) + '.json?print=pretty'
        r = requests.get(url)
        r.raise_for_status()

        display = json.loads(r.text)

        try:
            stories[display['title']] = display['url']
        except:
            stories[display['title']] = ''

    for key, values in stories.items():
        key = key.encode('utf-8')
        print(i,  key)
        print(bcolors.OKBLUE + values + bcolors.ENDC + '\n')

        i += 1

def maxItemId():
    url = ' https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty'
    r = requests.get(url)
    r.raise_for_status()

    maxItem = json.loads(r.text)

    return maxItem


def parseArguments(command):
    parser = argparse.ArgumentParser(description="Hacker News command line client")

    parser.add_argument('--top', '-t', action='store_true', help='Shows the current top stories on Hacker News')
    parser.add_argument('--new', '-n', action='store_true', help='Shows the new stories on Hacker News')
    parser.add_argument('--best', '-b', action='store_true', help='Shows best stories on Hacker News')
    parser.add_argument('--results', '-r', help='Returns the number of stories you choose Default '
                                                                     'is set at 500 which will make the '
                                                                     'program run slow')

    namespace = parser.parse_args(command)
    return namespace


def main():
    namespace = parseArguments(sys.argv[1:])
    if namespace.results:
        if namespace.top:
            getStories(getTopStoriesIDs(int(namespace.results)))
        if namespace.best:
            getStories(getBestStoriesIDs(int(namespace.results)))
        if namespace.new:
            getStories(getNewStoriesIDs(int(namespace.results)))
    else:
        if namespace.top:
            getStories(getTopStoriesIDs())
        if namespace.best:
            getStories(getBestStoriesIDs())
        if namespace.new:
            getStories(getNewStoriesIDs())


if __name__ == '__main__':
    main()
