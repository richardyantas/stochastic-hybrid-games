

# Dependencies
  c++17

  uppaal - dependencies 
  dynibex - dependencies
  jsoncpp - depencencies

# Install 

Install Python Package Manager "anaconda"
[More info](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)

# Run the project 

# 1.- Create an environment with conda 
```
conda env create -f environment.yml
conda env list
conda activate ucsp_solar
conda list 
pip-compile requirements.in
pip-sync requirements.txt
```

# 2.- run the project with uppaal

```
bash ./sthocastic_hybrid_game/tasks/run_projectl.sh
```

# 3.- Uninstall python environment:
```
conda remove --name ucsp_solar --all
```
