#!/bin/bash

mkdir lambda_layer
cd lambda_layer

# Create a python virtual environment named 'myenv'
python3 -m venv myenv
source myenv/bin/activate

# Install requests module
pip install requests

# Create python.zip file
mkdir python
mv myenv/lib python/
zip -r python.zip python/