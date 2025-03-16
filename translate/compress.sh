set -xe
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo usage bash $0 INPUT [ASS_FILE]
    exit 0
fi

WORKSPACE_DIR=$(dirname $(realpath $0))
MP4_PATH=`realpath "$1"`
if [ -d "$MP4_PATH" ]; then
    DATA_DIR="$MP4_PATH"
    MP4_NAME=`basename "$MP4_PATH"`.mp4
else
    DATA_DIR=`dirname "$MP4_PATH"`
    MP4_NAME=`basename "$MP4_PATH"`
fi
BASE_NAME=`echo "$MP4_NAME"|rev|cut -d . -f 2-|rev`
if [[ x"$2" == x ]]; then
    ASS_NAME="$BASE_NAME".ass
else
    ASS_NAME=`realpath "$2"`
fi

cd "$DATA_DIR"

ffmpeg -y -hwaccel cuda -c:v h264_cuvid \
	-i $MP4_NAME -vf subtitles=$ASS_NAME \
	-c:v h264_nvenc -c:a copy ${BASE_NAME}_sub.mp4
    # -b:v 2500k
    # -ss -to
