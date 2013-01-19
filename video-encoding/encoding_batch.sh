obj=$1
format=$2
output_obj=${obj%.*}.$format
picloud bucket get $obj .
ffmpeg -i $obj $output_obj
picloud bucket put $output_obj $output_obj
