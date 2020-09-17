import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from modules.ai_operations import swap_deepfake_reference

def main():
    fn = os.path.join(os.path.dirname(__file__), '../ai/deepfake_ref/swap.mp4')
    print("swapping...")
    swap_deepfake_reference(open(fn, "rb"))

if __name__ == "__main__":
    main()