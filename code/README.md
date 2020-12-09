

# Install 
    Install Python Package Manager "anaconda"
    [More info](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)

# Run the project 

# 1.- Create an environment with conda 
    ´´´cmd
    conda env create -f environment.yml
    conda env list
    conda activate ucsp_solar
    pip-compile requirements.in
    pip-sync requirements.txt
    ´´´

# 2.- run the project with uppaal
    ´´´cmd
    bash ./sthocastic_hybrid_game/tasks/run_projectl.sh
    ´´´

# 3.- Uninstall python environment:
    ´´´cmd
    conda remove --name ucsp_solar --all
    ´´´
# another format to .md is .rst 
https://eli.thegreenplace.net/2017/restructuredtext-vs-markdown-for-technical-documentation/