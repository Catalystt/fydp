# Document Generator

This package generates artifical government documents and saves them to the output directory to be used for deep learning training.

## Installation
```bash
# Install Pipenv first
pipenv install
```

## Usage
```bash
pipenv run python ./document-generator.py
cd ../fastai
conda activate fastai-cpu
cp ../document-generator/classify.py classify.py && python classify.py
```