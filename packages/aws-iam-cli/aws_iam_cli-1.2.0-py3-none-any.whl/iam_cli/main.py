import argparse
import sys

from iam_cli.command import Command
from iam_cli import VERSION


def get_arguments():
    parser = argparse.ArgumentParser(description="Process a CSV file for IAM users.")
    parser.add_argument('-v', '--version', action='version', version=f'iam-cli v{VERSION}')
    
    return parser


def main():
    try:
        parser = get_arguments()
        args = parser.parse_args()  # 인자를 파싱하는 부분을 추가함

        Command()
    except KeyboardInterrupt:
        print('Cancelled by user.')
        sys.exit()


if __name__ == '__main__':
    main()
