#! /bin/sh 

pyinstaller --onefile main.py -n ani-tupi
sudo cp dist/ani-tupi /usr/local/bin/ani-tupi
