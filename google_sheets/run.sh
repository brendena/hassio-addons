#!/bin/bash
set -e
#time=$(cat /data/options.json | jq -r '.time // empty')
#upload=$(cat /data/options.json | jq -r '.upload // empty' )
#all=$(cat /data/options.json | jq -r '. // empty' )
#echo $all

echo "started google Sheets add on"
python index.py 
