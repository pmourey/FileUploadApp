#!/bin/bash

if [ "$REQUEST_METHOD" = "POST" ]; then
  if [ "$CONTENT_LENGTH" -gt 0 ]; then
      read -n $CONTENT_LENGTH POST_DATA <&0
  fi
fi

echo "$POST_DATA" > data.bin
IFS='=&'
set -- $POST_DATA

#2- Value1
#4- Value2
#6- Value3
#8- Value4

#echo $2 $4 $6 $8

echo "Content-type: text/html"
echo ""
echo "<html><head><title>Saved</title></head><body>"
echo "Data received: $POST_DATA"
echo "</body></html>"
