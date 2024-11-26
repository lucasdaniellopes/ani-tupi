# Sobre
Estava cansado de anúncios e o ani-cli não tinha conteúdo em portuguẽs brasileiro então fiz isso.

# Youtube Demo
[![Demo](https://img.youtube.com/vi/eug6gKLTD3I/maxresdefault.jpg)](https://youtu.be/eug6gKLTD3I)

# Requisitos
mpv, firefox, python, venv e pip

# Release
Basta dar direito de execução a release mais atual e usar.
```bash
chmod +x ./ani-tupi
```

# Buildar do código-fonte
Clone o repositório e execute os seguintes comandos.

## Linux
```bash
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
./build.sh
```

## Windows
```powershell
python -m venv venv
venv/Scripts/activate.ps1
pip install -r requirements.txt
pip install windows-curses
pyinstaller --onefile main.py -n ani-tupi
```
Depois, adicione o diretório dist que foi gerado pelo pyinstaller a variável de sistema PATH. Reinicie seu terminal. 

# Usar
Basta usar agora.
```bash
ani-tupi
```
