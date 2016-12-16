#!/bin/sh
if ps -ef | grep -v grep | grep CardReader.py ; then
	exit 0
else
	sudo service card-reader.sh restart
	exit 0
fi
