#!/bin/sh

DEFAULT_AUTOCOMMIT_MSG="changes from $(uname -n) on $(date)"

sudo git add .

sudo git commit -m "Uploaded: $date"

sudo git remote -v

sudo git push origin master

