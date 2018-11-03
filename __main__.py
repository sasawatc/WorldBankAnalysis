# -*- coding: utf-8 -*-
"""
Created on Fri Nov 02 14:43:31 2018

For running the whole project
"""

__version__ = '1.0.0'
__author__ = ('Joshua Thang, Kaiyi Zou, Khuyen Yu, '
              'Kristian Nielsen, Sasawat Chanate, Ying Li')

from init_data import init_data
from corr import corr

import conda.cli


def main():
    print("Checking prerequisite packages...")
    try:
        __import__('adjustText')
    except ImportError:
        print("Installing prerequisite packages...")
        conda.cli.main('conda', 'install', '-y', '-c', 'phlya', 'adjustText')

    print("Initializing data...")
    init_data()
    print("Running correlation...")
    corr()

    print()
    print()
    print()

    print("Process complete: please check output figures in figs/ directory...")


if __name__ == "__main__":
    main()
