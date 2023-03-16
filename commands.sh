# Python

# python3.7 python3-pip
# python3.7 -m pip install pip
# how assign more ram to the docker container
# https://medium.com/codex/how-to-limit-cpu-and-memory-usage-in-docker-containers-a024b429f55e
# g++ 4_rooms.cpp -I/usr/local/include/ibex  -o 4_rooms -L/usr/local/lib -libex -lprim -lClp -lCoinUtils


# Docker

# docker build -t patterns:latest .
# docker run -it --name patterns patterns  bash
# docker exec nostalgic_wright python app.py
# #!/bin/bash
# docker rm $(docker ps -aq)
# docker rmi $(docker images | grep "^<none>" | awk '{print $3}')
# docker exec patterns ./4_rooms

# Git

# git remote -v
# git remote add github git@github.com:richardyantas/stochastic-hybrid-games.git
# git remote set-url bitbucket git@bitbucket.org:muniz-cs/ucsp-solar.git
# git push bitbucket main
# git push individual main

# Docker-compose

# docker-compose up -d --build
# docker-compose down