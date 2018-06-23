for video in ./*.mp4
do
  ffmpeg -i "$video" -s 320x240 -r 8 -b:v 256k -an ds_$(basename "$video")
done
