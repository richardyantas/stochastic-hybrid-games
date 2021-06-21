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

Before anything modify your vscode.json to add a python formatter

```
{
  "workbench.iconTheme": "vscode-icons",
  "workbench.editorAssociations": [
    {
      "viewType": "jupyter.notebook.ipynb",
      "filenamePattern": "*.ipynb"
    }
  ],
  "git.confirmSync": false,
  "editor.formatOnPaste": true,
  "editor.formatOnSave": true,
  "python.formatting.provider": "autopep8",
  "explorer.confirmDelete": false,
  "python.showStartPage": false,
  "explorer.confirmDragAndDrop": false,
  "python.linting.pylintArgs": ["--load-plugins=pylint_django"],
  "javascript.updateImportsOnFileMove.enabled": "always",
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  }
}
```

if you want to verify the dependencies run `conda list | grep autopep8` for instance.

# 2.- run the project with uppaal

Do ` export PYTHONPATH=.` in main directory otherwise we will get error.

python simulation (works! but before that we also need to make an export i think)

    python sthocastic_hybrid_game/src/simulation.py

add `import argparse` arparse is already incorporated in python (standar packages in python [https://docs.python.org/3/library/]).

# 3.- Uninstall python environment:

```
conda remove --name ucsp_solar --all
```

# 4.- run the project

    export PYTHONPATH=.
    python sthocastic_hybrid_game/src/run_experiment.py

# 5.- Development

    git rm -r --cached . && git add . && git commit -m "fixing .gitignore"

# 5.- Github and Bitbucket

    git remote rename origin github
    git remote add bitbucket https://richardyantas@bitbucket.org/muniz-cs/ucsp-solar.git
    git push github HEAD
    git push bitbucket HEAD
    git push origin github your_branch
    git push origin bitbucket your_branch

# 6.- C++ safe dynbex running to find patterns

    cmake .. && make && make test
