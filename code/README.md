

# 1.- create an environment with conda 

## 1.1 with conda
### 1.1.1 environment for running with uppaal (Recommended if you do not have CUDA installed)
    conda env create -f environment_simple.yml
### 1.1.2 environment for runnnign with tensorflow
    conda env create -f environment_pytorch.yml
    conda env list
    conda activate ucsp_solar_pytorch
    conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
## 1.2 with pipenv
### 1.2.1.- create an environment for running with uppaal (Recommended if you do not have CUDA installed)
    


## 1.2 install python dependencies for running the project
    pip install -r requirements.txt


## uninstall python environment:
    conda remove --name ucsp_solar_pytorch --all
    conda remove --name ucsp_solar_uppaal--all

## 1.3 run the project with uppaal
    ./tasks/run_shg_uppaal.sh
## 1.4 run the project with tensorflow
    ./tasks/run_shg_tensorflow.sh

# another format to .md is .rst 
https://eli.thegreenplace.net/2017/restructuredtext-vs-markdown-for-technical-documentation/