#!/bin/bash

BUILD_CMD="pyinstaller -n ani-tupi --onefile main.py --add-data plugins:plugins --hidden-import plugins"
for plugin in $(ls plugins/*.py | grep -v __init__ | sed 's/\.py//' | sed 's/\//\./')
do 
    BUILD_CMD+=" --hidden-import ${plugin}"
done
echo "${BUILD_CMD}"
eval $BUILD_CMD

PLUGIN_CP="cp -r plugins dist"
echo "${PLUGIN_CP}"
$PLUGIN_CP

echo "Build completo! O executável está em dist/ani-tupi"
echo "Para instalar no sistema, execute: sudo cp dist/ani-tupi /usr/local/bin/"