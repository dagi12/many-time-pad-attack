#!/bin/sh
set -e
set -x

#bytes=$(stat -f%z 378.xor)
#octets=$((bytes / 512 + 1))
for i in {0..21}; do
    start=$(($i * 512))
    xxd -s $start -l 512 -p 378.xor | tr -dc 0-9a-f > xxd/dump$i.txt
done

