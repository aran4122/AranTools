import argparse
import os

import cv2
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", nargs="+")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if os.path.isdir(args.input_path[0]):
        args.input_path = [
            f"{args.input_path[0]}/{p}" for p in os.listdir(args.input_path[0])
        ]

    print(args.input_path)
    for img_path in args.input_path:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (0, 0), fx=2, fy=2)
        img = cv2.copyMakeBorder(img, 200, 200, 0, 0, cv2.BORDER_CONSTANT)
        cv2.imwrite(img_path, img)


if __name__ == "__main__":
    main()
