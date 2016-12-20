#!/bin/sh
_cwd="$PWD"

sudo ln -sfn $_cwd/card-reader.sh /etc/init.d/card-reader.sh
sudo update-rc.d card-reader.sh defaults

