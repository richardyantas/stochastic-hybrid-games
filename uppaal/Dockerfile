
# FROM scrapper:latest
# USER root

FROM python:3.7
USER root
RUN mkdir /app
COPY ./uppaal_downloader.py /app

WORKDIR /app

RUN mkdir __logger

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt -y update
RUN apt install -y google-chrome-stable

# install chromedriver
RUN apt install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # set display port to avoid crash
ENV DISPLAY=:99

# install dependencies
RUN apt install -y apt-utils tar tree nano
RUN pip install --upgrade pip
RUN pip install webdriver-manager selenium

RUN python uppaal_downloader.py                     
# CMD ["python", "./uppaal_downloader.py"]
RUN unzip uppaal-4.1.20-stratego-9-linux64.zip && \
    rm uppaal-4.1.20-stratego-9-linux64.zip && \
    mv uppaal-4.1.20-stratego-9-linux64 uppaal

# docker build -t scrapper .
# docker run -it --name scrapper scrapper bash

# Install Jsoncpp
RUN apt install -y libjsoncpp-dev cmake
COPY config config
RUN cd config && mkdir build && \
    cd build && cmake .. && make && \
    cp libconfig.so ../../uppaal/bin/

# RUN cp /config/build/libconfig.so ./uppaal/bin/

ENV LD_LIBRARY_PATH=/home/app/uppaal/bin/


# docker build -t uppaal:latest .
# docker run -it -v /home/serendipita/Documents/tesis/ucsp-solar/uppaal/templates:/app/templates -v /home/serendipita/Documents/tesis/ucsp-solar/data:/app/data --name uppaal uppaal bash
# docker run -it -v ${pwd}:/app/ --name uppaal uppaal bash
# export LD_LIBRARY_PATH=/home/app/uppaal/bin/
# ./uppaal/bin/verifyta templates/swh.xml templates/swh.q
# docker exec uppaal ./uppaal/bin/verifyta templates/swh.xml templates/swh.q

# docker-compose exec uppaal ./uppaal/bin/verifyta templates/swh.xml templates/swh.q