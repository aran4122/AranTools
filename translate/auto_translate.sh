set -xe
if [ $# -ne 1 ]; then
    echo usage bash $0 INPUT
    exit 0
fi

WORKSPACE_DIR=$(dirname $(realpath $0))
MP4_PATH=`realpath $1`
if [ -d $MP4_PATH ]; then
    DATA_DIR=$MP4_PATH
    MP4_NAME=`basename $MP4_PATH`.mp4
else
    DATA_DIR=`dirname $MP4_PATH`
    MP4_NAME=`basename $MP4_PATH`
fi
BASE_NAME=`echo $MP4_NAME|rev|cut -d . -f 2-|rev`

cd $DATA_DIR

python $WORKSPACE_DIR/translate_by_faster_whisper.py $MP4_NAME $BASE_NAME.ass
