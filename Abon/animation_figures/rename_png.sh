#!/bin/bash

# the name following the 7digit number in the filename of the png files in the folder  (without .png)

i=2

while [ $i -lt 766 ]; do
    
    if [ $i -lt 10 ]; then
        mv col${i}.png col00000${i}.png

    elif [ $i -gt 9 ] && [ $i -lt 100 ]; then
		mv col${i}.png col0000${i}.png

	elif [ $i -gt 99 ]; then
		mv col${i}.png col000${i}.png
    fi

    i=$((i+1))

done



#col000765.png