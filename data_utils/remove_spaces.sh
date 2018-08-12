for oldname in ./*_M*/*  # All video dirs are named *_MAKE or *_MISS
do
  newname=`echo $oldname | sed -e 's/ /_/g'`
  mv "$oldname" "$newname"
done
