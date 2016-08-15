from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from subprocess import Popen, DEVNULL
import requests
import argparse
import re
import os
import sys
import logging


class CDownloader():
    def __init__(self, pArgs):
        self.log = logging.getLogger('ocdownloader.CDownloader')
        self.mainUrl = 'http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/'
        if pArgs.command == 'useList':
            self._ProcessFlist(pArgs.filepath)
        self.saveDir = pArgs.savedir
        # a text file containing file names to download was passed
        # load and parse
        return None

    def _ProcessFlist(self, path):
        try:
            with open(path, 'r') as fr:
                self.flist = fr.read().splitlines()
            if self.flist:
                self.log.info('flist populated')
            else:
                self.log.warning('empty flist!')
        except FileNotFoundError as err:
            self.log.error('File Not Foud... exiting')
            sys.exit(err)
        return None

    def _RetrieveFile(self, fname):
        fUrl = os.path.join(self.mainUrl, fname)
        fpath = os.path.join(self.saveDir, fname)
        self.log.info('attempting download from %s' % fUrl)
        rf = requests.get(fUrl, stream=True)
        if rf.ok:
            self.log.info('file found at %s' % fUrl)
            try:
                with open(fpath, 'wb') as f:
                    for chunk in rf.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            except FileNotFoundError as err:
                self.log.error('Incorrect file path given... exiting')
                sys.extit(err)
        else:
            self.log.warning('%s' % rf.status_code)
        proc = Popen('uncompress -d %s' % fpath, shell=True, stdout=DEVNULL)
        return proc

    def RunParallel(self):
        '''
        Passes list of files to the _RetrieveFile method
        '''
        self.log.debug('setting up parallel download')
        with Pool() as pool:
            results = pool.map(self._RetrieveFile, self.flist)
        return results


def ParseCommandLine(args):
    '''
    Accomodates two possibles usages.
    First usage is to submit a text file w/ a list of filenames to download.
    Second usage is to submit parts of a search pattern as command line args.
    '''
    # Two possible usages. Either submit a text file with a list of files to
    # download or ask for a specific sensor/year/level/coverage
    # The first case is easy, the second case needs some parsing.
    # I'll do the first case first.
    parser = argparse.ArgumentParser(description='OCDownloader')
    parser.add_argument('-s', '--savedir', help='path to save downloaded \
                        files', type=str, default='./')
    parser.add_argument('-v', '--verbose', help='augment verbosity',
                        action='store_true')
    subparsers = parser.add_subparsers(help='commands', dest='command')
    # a useList command with a dedicated set of options
    listParser = subparsers.add_parser('useList',
                                       help='use text file listing\
                                       desired files')
    listParser.add_argument('-p', '--filepath', action='store',
                            help='path to list file')
    listParser.add_argument('-u', '--fullUrl', action='store_true',
                            default='False', help='list includes full url \
                            [False] | True')
    # a command line command
    cdlParser = subparsers.add_parser('useCdl',
                                      help='specify patterns of files to \
                                      download on the command line')
    cdlParser.add_argument('-c', '--coverage', help='coverage type to inform \
                           filename parsing', type=str, default='GAC')
    cdlParser.add_argument('-l', '--level', help='processing level', type=str,
                           default='L1')
    cdlParser.add_argument('-y', '--year',
                           help='year in yyyy format, all years downloaded if \
                           none specified', action='store')
    return parser.parse_args(args)


def SetLogger(verbosity):
    # create logger with 'spam_application'
    logger = logging.getLogger('ocdownloader')
    # create formatter to add it to the handler(s)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \
                                  - %(message)s')
    if verbosity:
        logger.setLevel(logging.DEBUG)
        # create console handler with a higher log level and populate settings
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    else:
        logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('ocd.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    return logger


def Main(argv):
    pArgs = ParseCommandLine(argv)
    logger = SetLogger(pArgs.verbose)
    logger.info('initializing downloader object')
    dwnldObj = CDownloader(pArgs)
    logger.info('downloader object initialized')
    dwnldObj.RunParallel()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        ParseCommandLine(['-h'])
    else:
        Main(sys.argv[1:])
