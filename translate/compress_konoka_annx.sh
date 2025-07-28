set -xe
if [ $# -ne 2 ]; then
    echo usage bash $0 INPUT.mp3 OUTPUT.mp4
    exit 0
fi

SCRIPT_DIR=$(dirname $(realpath $0))
AUDIO_PATH=$(realpath $1)
OUTPUT_PATH=$(realpath $2)

if [[ $(echo $OUTPUT_PATH|rev|cut -b -4|rev) != .mp4 ]]; then
    OUTPUT_PATH=$OUTPUT_PATH/$(basename $AUDIO_PATH|sed 's/.mp3/.mp4/')
fi

DATE=$(basename $AUDIO_PATH|cut -b -4).$(basename $AUDIO_PATH|cut -b 5-6).$(basename $AUDIO_PATH|cut -b 7-8)
sed "s/YYYY.MM.DD/$DATE/" $SCRIPT_DIR/assets/KONOKA_ANNX.ass > $SCRIPT_DIR/assets/KONOKA_ANNX_tmp.ass

ffmpeg -y \
    -loop 1 -i $SCRIPT_DIR/assets/KONOKA_ANNX.jpg -i $AUDIO_PATH -shortest -r 24 \
    -vf subtitles=$SCRIPT_DIR/assets/KONOKA_ANNX_tmp.ass -c:v h264_nvenc -c:a copy $OUTPUT_PATH

rm $SCRIPT_DIR/assets/KONOKA_ANNX_tmp.ass
