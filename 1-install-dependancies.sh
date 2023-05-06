conda install python=3.8.10 -y # Or use another way to install this version of python

# Download Transformers codes
wget https://github.com/huggingface/transformers/archive/refs/heads/v4.14.1-release.zip
unzip v4.14.1-release.zip
rm v4.14.1-release.zip

# PIP
pip install orderedset
pip install pytorch
pip install seqeval
pip install evaluate
pip install lxml
python -m pip install scipy
pip install protobuf==3.20.*
pip install git+https://github.com/huggingface/accelerate
pip install transformers==4.14.1
pip install 'urllib3<2'
