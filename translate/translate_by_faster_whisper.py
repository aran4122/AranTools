import argparse
import os.path as osp

from common import ASS_HEADER
from faster_whisper import WhisperModel

from arantools.utils import write_list


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument(
        "-m", "--model_type", default="large-v3", choices=["medium", "large-v3"]
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

    model = WhisperModel(
        args.model_type,
        device="cuda",
        compute_type=args.compute_type,
        local_files_only=True,
    )
    print()

    segments, info = model.transcribe(
        args.input_file,
        language="ja",
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=700),
    )
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
