import sys

def _real_main(argv):
    print(argv)

def main(argv=None):
    try:
        _real_main(argv)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')

__all__ = ['main']