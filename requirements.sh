# chmod +x requirements.sh to run
#!/bin/bash

pip install virtualenv
python3 -m venv env
source env/bin/activate
pip install GitPython
pip install chardet # 4.0.0
pip install nltk
pip install pylint
# pip install git
pip install shutil
pip install pandas
pip install matplotlib
pip install numpy
pip install seaborn
pip install sklearn
pip install nltk
pip install torch torchvision torchaudio
