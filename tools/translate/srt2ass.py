import os
import sys

import regex as re
from common import ASS_HEADER

from arantools.utils import read_list, write_list


def srt2ass(input_path):
    if ".ass" in input_path:
        return

    if not os.path.isfile(input_path):
        print(input_path + " not exist")
        return

    lines = read_list(input_path)
    lines = [line for line in lines[1:] if line != ""]

    sub_lines = []
    dlg_lines = ""
    for idx in range(len(lines)):
        line = lines[idx]
        if line.isdigit() and re.match(r"-?\d\d:\d\d:\d\d", lines[idx + 1]):
            if dlg_lines:
                sub_lines.append(dlg_lines)
            dlg_lines = ""
        elif re.match(r"-?\d\d:\d\d:\d\d", line):
            line = line.replace("-0", "0")
            line = re.sub(r"\s+-->\s+", ",", line)
            line = re.sub(r"\d(\d:\d{2}:\d{2}),(\d{2})\d", "\\1.\\2", line)
            dlg_lines = "Dialogue: 0," + line + ",Default,,0,0,0,,"
            line_count = 0
        else:
            if line_count > 0:
                dlg_lines += "\\N"
            dlg_lines += line
            line_count += 1

    output_path = input_path.replace(".srt", ".ass")
    basename = input_path.split("/")[-1].split(".")[0] + ".mp4"
    output_lines = [ASS_HEADER.format(basename, basename)] + sub_lines
    write_list(output_lines, output_path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for name in sys.argv[1:]:
            srt2ass(name)
