default:
	pelican -s settings.py

update:
	# creds.txt: user@server:~path/to/blog
	rsync -arvz --progress --exclude '.*.swp' ./output/ `cat creds.txt`
