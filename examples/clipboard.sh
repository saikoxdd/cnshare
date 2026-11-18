#!/bin/sh
# Copy a share text in the Poizon/Taobao app, then run this to get only the link back on the clipboard.
pbpaste | cnshare --url-only | tee /dev/stderr | pbcopy
