import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from modules.ai_operations import get_betaface_usage

def main():
    get_betaface_usage()

if __name__ == "__main__":
    main()