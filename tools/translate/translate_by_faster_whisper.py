import argparse
import os.path as osp

from faster_whisper import WhisperModel

from arantools.utils import write_list

ASS_HEADER = """[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
Title:
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
ScaledBorderAndShadow: yes
PlayResX: 1280
PlayResY: 720

[Aegisub Project Garbage]
Audio File: {}
Video File: {}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,思源黑体 CN Heavy,54,&H00FFFFFF,&H000019FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2.66667,2,2,7,7,7,1
Style: 备注,思源黑体 CN Heavy,50,&H00FFFFFF,&H000019FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2.66667,2,8,7,7,7,1
Style: 水印,胡晓波男神体,20,&H32FFFFFF,&H000000FF,&HFF000000,&HFF000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,2:00:00.00,水印,,0,0,0,,道德天尊战神菌"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument(
        "-m", "--model_type", default="large-v2", choices=["medium", "large-v2"]
    )
    parser.add_argument(
        "-c", "--compute_type", default="auto", choices=["int8", "float32", "auto"]
    )
    args = parser.parse_args()
    return args


def convert_seconds_to_hms(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(seconds % 1 * 1000)
    hours, minutes, seconds = int(hours), int(minutes), int(seconds)
    output = f"{hours}:{minutes:02}:{seconds:02}.{milliseconds//10:02}"
    return output


def main():
    args = parse_args()
    assert args.output_file.endswith(".ass")

    model = WhisperModel(args.model_type, device="cuda", compute_type=args.compute_type)
    print()

    segments, info = model.transcribe(args.input_file, beam_size=5)
    print(f"{info.language=}, {info.language_probability=}")

    input_name = osp.basename(args.input_file)
    res = [ASS_HEADER.format(input_name, input_name)]
    for count, segment in enumerate(segments):
        start_time = convert_seconds_to_hms(segment.start)
        end_time = convert_seconds_to_hms(segment.end)
        text = segment.text.lstrip()
        res.append(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}")
        print(start_time, end_time, text)
    write_list(res, args.output_file)


if __name__ == "__main__":
    main()
