import sys, shutil
import argparse
from pathlib import Path

from .split import split_file_into_module


def argparser():
    parser = argparse.ArgumentParser(
        description="Split a Python file into separate modules"
    )
    parser.add_argument("filename", help="The Python file to split")
    return parser


def main():
    args = argparser().parse_args()
    created_filenames = split_file_into_module(args.filename)
    print(f"Created files: {created_filenames} from {args.filename}.")

    # create a new dir now named after the original file
    directory = Path(args.filename).stem
    if Path(directory).exists():
        answer = input(
            f"Directory {directory} already exists. Overwrite? [y/N] "
        ).lower()
        if answer != "y":
            print("Aborting.")
            sys.exit(1)
        else:
            shutil.rmtree(directory)

    Path(directory).mkdir()
    print(f"Created directory: {directory}")

    # move the original file into the new dir
    for name in created_filenames:
        Path(name).rename(Path(directory) / name)
    print(f"Moved the created files into {directory}")


if __name__ == "__main__":
    main()
