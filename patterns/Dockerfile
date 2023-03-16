FROM python:2.7

WORKDIR /app

RUN apt update

# Install DynIbex Dependencies
RUN apt install -y flex bison gcc \
    g++ make pkg-config nano libjsoncpp-dev cmake

# Install DynIbex
RUN wget https://perso.ensta-paris.fr/~chapoutot/dynibex/distrib/dynibex-2.2.tar.gz
RUN tar xvfz dynibex-2.2.tar.gz && cd dynibex-2.2 && ./waf configure && ./waf install
ENV LD_LIBRARY_PATH=/usr/local/lib
COPY . .
RUN echo "updated"

# RUN ./main /data/static_data.json
# RUN g++ -frounding-math -ffloat-store -I/usr/local/include -I/usr/local/include/ibex  -O3 -DNDEBUG -Wno-deprecated -frounding-math  -o 4_rooms 4_rooms.cpp -L/usr/local/lib -libex -lprim -lClp -lCoinUtils
# RUN g++ -I/usr/local/include -I/usr/local/include/ibex -o 4_rooms 4_rooms.cpp -L/usr/local/lib -libex -lprim -lClp -lCoinUtils
# RUN g++ -I/usr/local/include -I/usr/local/include/ibex -I/usr/include/jsoncpp -o main main.cpp -L/usr/local/lib -L/usr/lib/x86_64-linux-gnu/ -libex -lprim -lClp -lCoinUtils -ljsoncpp

# docker build -t patterns:latest .
# docker run -it -v /home/serendipita/Documents/tesis/ucsp-solar/data/solar-water-heating:/app/data  --name patterns patterns bash
