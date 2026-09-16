#!/usr/bin/env bash
#
#

awk 'BEGIN{FS=" "} {count[$1]++} END{for (i in count) print count[i], $1, $2} ' | sort -k1nr < potential.dat
