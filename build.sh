#! /bin/sh 

pyinstaller --onefile main.py -n ani-tupi
echo "Tornando executável global"
sudo cp dist/ani-tupi /usr/local/bin/ani-tupi
sudo cp -r plugins /usr/local/bin/plugins
