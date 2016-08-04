from subprocess import Popen,STDOUT,DEVNULL
from multiprocessing import cpu_count
import sys
import argparse

class ParallelL2():
    '''Manages subprocess spawning'''
    def __init__(self,pArgs):
        self._parseArgs(pArgs)

    def _parseArgs(self):
        pArgs

    def CmdGenerator(self):
        '''Generates l2gen command line string for next process'''
        pass

    def ProcessRunner(self):
        pass

def Main():
    '''Function to parse out command line and launch l2gen parallel processing'''
    pass

if __name__ == '__main__':
    Main(sys.argv[1:])
