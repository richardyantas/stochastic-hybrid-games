FROM python:3.8
USER root

COPY . /app
WORKDIR /app

RUN mkdir __logger


# # install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable

# # install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # set display port to avoid crash
# ENV DISPLAY=:99

# install dependencies
# RUN apt-get install tar tree nano
RUN apt-get install -y apt-utils
RUN apt-get install -y tar tree nano


# RUN pip install --upgrade pip
# RUN pip install -r requirements/prod.txt


# Install Uppaal Stratego
# CMD ["python", "./uppaal_downloader.py"]

# RUN python ./uppaal_downloader.py
# RUN unzip uppaal-4.1.20-stratego-9-linux64.zip uppaal


# we can also run 
# docker build -t --rm ucsp-solar:latest .
# docker run -it --rm -name ucsp-solar ucsp-solar
# docker exec nostalgic_wright python app.py

# #!/bin/bash
# docker rm $(docker ps -aq)
# docker rmi $(docker images | grep "^<none>" | awk '{print $3}')




# is needed to install java jdk to run uppaal from terminal 
# can be run using docker container graphics ide ? 


# install python
# install dynibex


#curl -d '{"Name":"richard", "JobTitle":"research", "Company": "ucsp", 
# "Email": "richardyantas5@gmail.com"}' -H "Content-Type: application/json" 
# -x POST  https://www.it.uu.se/research/group/darts/uppaal/download/registration.php?id=0&subid=17