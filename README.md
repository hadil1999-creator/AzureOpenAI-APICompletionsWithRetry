# Azure OpenAI API Completions With Retry

This repo provides step by step instructions on how to setup environment and use python scripts to deploy Azure OpenAI models as well as make API calls to the models for inferencing. 

## Pre-requisite 

1. A up and running Azure OpenAI instance is required. The steps to achieve this via code are available on my other repo here: https://github.com/arkr-msft/Azure-IaC

2. The setup here was developed and tested in Github codespaces, but will work in any machine

## Create a virtual env:
Needed to use a  consistent virtual environment every time. Follow steps below in terminal window:

Steps: 
	1. Create a virtual environment:
    >virtualenv ~/.venv
	
	2. Activate virtual env and confirm current python is in newly created virtual env

    >source ~/.venv/bin/activate
	>which python
	
	3. To add this setting everytime a new terminal is started edit bashrc file
    vim ~/.bashrc

	4. navigate to bottom of file using 'shift + g' then insert using 'shift + I'
    #source virtual environment
    >source ~/.venv/bin/activate

	5. Exit vim by 'escape + :wq"

With this, every time a new terminal is created, it will have same virtual environment

## Verify all required libraries are listed in requirements.txt

## Execute install command as configured in Makefile via below command

make install

## Change mode of .py files to be executable

chmod 777 *.py

## execute python files

python azureopenai_deploy.py