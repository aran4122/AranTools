set -xe
ffmpeg -loop 1 -y -i $1 -i $2 -shortest -r 24 -b:a 400k -b:a 192k $3
