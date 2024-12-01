#!/bin/sh 

BUILD_CMD="pyinstaller -n ani-tupi --onefile main.py --distpath . --hidden-import plugins "
for plugin in `eval "ls plugins/*.py | sed 's/\.py//' | sed 's/\//\./' | sed 's/plugins.__init__//'"`
do 
	BUILD_CMD+=" --hidden-import ${plugin}"
done
echo "${BUILD_CMD}"
$BUILD_CMD
sudo cp ./ani-tupi /usr/local/bin/ani-tupi
