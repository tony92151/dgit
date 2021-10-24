"""entry point"""
import sys

from dgit.main import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
