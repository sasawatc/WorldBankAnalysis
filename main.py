import os
import conda.cli


def main():
    print("Hello World!")

    try:
        __import__('adjustText')
    except ImportError:
        conda.cli.main('conda', 'install', '-y', '-c', 'phlya', 'adjustText')

    os.system('python init_data.py')
    os.system('python corr.py')


if __name__ == "__main__":
    main()
