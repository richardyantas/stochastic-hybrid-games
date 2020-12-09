#! /bin/bash

for f in *
do
	if [ -d "$f" ]
	then
		chmod 755 "$f"
	fi
done

