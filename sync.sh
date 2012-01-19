#!/bin/bash

rsync -arvz --progress --exclude '.*.swp' ./output/ `cat creds.txt`:~/www/mathieu/blog/

