#!/bin/sh

runestone build
rm -r ../../static/thinkcspy-online/
mv build/thinkcspy-online/ ../../static/
