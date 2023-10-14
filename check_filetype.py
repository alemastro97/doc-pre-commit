#!/usr/bin/env python
import sys

def main():
    filenames = sys.argv[1:]
    for filename in filenames:
        if not filename.endswith(".py"):
            print(f"Rejected file {filename} because it's not a Python file.")
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
