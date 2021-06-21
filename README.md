# Dependencies

c++17
Uppaal - dependencies
Dynibex - dependencies
Jsoncpp - depencencies

# Install

Install Python Package Manager "anaconda"
[More info](https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)

# Run the project

# 1.- Create an environment with conda

    conda env create -f environment.yml
    conda activate ucsp_solar
    pip-compile requirements.in
    pip-sync requirements.txt

# 2.- run the project with MPC controller by default

Do `export PYTHONPATH=.` in the main directory otherwise it could not find the python package.

    python sthocastic_hybrid_game/src/simulation.py

# 3.- Uninstall python environment:

    conda remove --name ucsp_solar --all

# 4.- Run the project with Uppaal Controller

    export PYTHONPATH=.
    python sthocastic_hybrid_game/src/run_experiment.py --controller==UPPAAL

# 5.- Development

    git rm -r --cached . && git add . && git commit -m "fixing .gitignore"

# 6.- To get Pattern.json run CMakeLists.txt

    mkdir build && cd build
    cmake .. && make && make test
