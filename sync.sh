#!/bin/bash

pelican -s settings.py
rsync -arvz --progress --exclude '.*.swp' ./output/ `cat creds.txt`:~/www/mathieu/blog/

