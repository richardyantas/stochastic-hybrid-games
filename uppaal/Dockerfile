FROM python:3.8
USER root

COPY . /app
WORKDIR /app

RUN mkdir __logger


# # install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install dependencies
RUN apt-get install -y apt-utils
RUN apt-get install -y tar tree nano
RUN pip install --upgrade pip
RUN pip install -r requirements/prod.txt

# Install Uppaal Stratego
# CMD ["python", "./uppaal_downloader.py"]
RUN python ./uppaal_downloader.py
RUN unzip uppaal-4.1.20-stratego-9-linux64.zip uppaal



# Install Jsoncpp