FROM python:2.7

RUN apt update

# Install DynIbex Dependencies
RUN apt install -y flex bison gcc g++ make pkg-config nano 

# Install DynIbex
RUN wget https://perso.ensta-paris.fr/~chapoutot/dynibex/distrib/dynibex-2.2.tar.gz
RUN tar xvfz dynibex-2.2.tar.gz && cd dynibex-2.2 && ./waf configure && ./waf install

COPY 4_rooms.cpp .
# RUN echo 'export LD_LIBRARY_PATH=/usr/local/lib' >> ~/.bashrc && source ~/.bashrc
RUN g++ -frounding-math -ffloat-store -I/usr/local/include -I/usr/local/include/ibex  -O3 -DNDEBUG -Wno-deprecated -frounding-math  -o 4_rooms 4_rooms.cpp -L/usr/local/lib -libex -lprim -lClp -lCoinUtils
# RUN g++ -I/usr/local/include -I/usr/local/include/ibex -o 4_rooms 4_rooms.cpp -L/usr/local/lib -libex -lprim -lClp -lCoinUtils
RUN echo "updated"
# RUN ./4_rooms

#  https://medium.com/codex/how-to-limit-cpu-and-memory-usage-in-docker-containers-a024b429f55e
# how assign more ram to the docker container
#  g++ 4_rooms.cpp -I/usr/local/include/ibex  -o 4_rooms -L/usr/local/lib -libex -lprim -lClp -lCoinUtils


# we can also run 
# docker build -t patterns:latest .
# docker run -it --name patterns patterns  bash

# docker exec nostalgic_wright python app.py

# #!/bin/bash
# docker rm $(docker ps -aq)
# docker rmi $(docker images | grep "^<none>" | awk '{print $3}')

