#!/bin/sh
# Encode portfolio videos for the web (sources in ../io2 portfolio/videos, not published).
#   <slug>.mp4      720p H.264 + AAC, faststart: played in the lightbox (with sound)
#   <slug>-p.mp4    360p, 6 s, silent: autoplay preview loop on the card
#   <slug>.webp     poster frame
# Usage: FF=/path/to/ffmpeg sh tools/work_videos.sh
set -e
cd "$(dirname "$0")/.."
SRC="../io2 portfolio/videos"
OUT=assets/work
FF=${FF:-ffmpeg}
enc() { # slug file [preview start s] [poster time s]
  "$FF" -v error -y -i "$SRC/$2" -vf "scale=720:-2:flags=lanczos,fps=30,format=yuv420p" -c:v libx264 -preset slow -crf 24 -profile:v high -c:a aac -b:a 128k -ac 2 -movflags +faststart "$OUT/$1.mp4"
  "$FF" -v error -y -ss ${3:-0.5} -t 6 -i "$SRC/$2" -vf "scale=360:-2:flags=lanczos,fps=24,format=yuv420p" -c:v libx264 -preset slow -crf 30 -an -movflags +faststart "$OUT/$1-p.mp4"
  "$FF" -v error -y -ss ${4:-1.5} -i "$SRC/$2" -frames:v 1 -vf "scale=540:-2:flags=lanczos" -c:v libwebp -quality 72 "$OUT/$1.webp"
  echo "$1 done"
}
enc oman-national-day "Oman National Day CGI.mp4"
enc moc-hologram "KEY MARKETING MINISTRY Of commerce Oman HOLOGRAM .MP4"
enc avenues-labubu "Avenues Mall Oman Labubu Trend.mp4"
enc g-wagon-cgi "Mercedes G Wagon CGI.mp4"
enc pagani-cgi "Pagani Cars CGI.mp4"
enc chanel-cgi "Chanel CGI.mp4"
enc uae-national-day "UAE National Day CGI.MP4"
enc moc-video "Key marketing Ministry of commerce Oman video.mp4"
enc zomorod-cgi "zomorod agency CGI.mp4"
enc star-wars-vfx "Starwars Movie CGFEX.mp4" 3 4.5  # skip the "Part 1" title card
enc cinema-vfx "Cinema VFX Project.mp4"
enc cars-cgi "Cars CGI.mov"
