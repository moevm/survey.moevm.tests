FROM ubuntu:18.04
RUN apt-get update; apt-get clean

RUN apt-get update && apt-get install -y \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg \
	--no-install-recommends \
	&& curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
	&& echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
	&& apt-get update && apt-get install -y \
	google-chrome-stable \
	fontconfig \
	fonts-ipafont-gothic \
	fonts-wqy-zenhei \
	fonts-thai-tlwg \
	fonts-kacst \
	fonts-symbola \
	fonts-noto \
	fonts-freefont-ttf \
	--no-install-recommends \
	&& apt-get purge --auto-remove -y curl gnupg \
	&& rm -rf /var/lib/apt/lists/*

RUN apt-get install -y wget

RUN apt-get update

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev

RUN pip3 install --upgrade pip &&\
	pip3 install setuptools>=41.0.0

RUN apt-get update

RUN apt-get install unzip
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip &&\
    unzip chromedriver_linux64.zip

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/

ENV CHROMEDRIVER_DIR /chromedriver

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 443

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i ru_RU -c -f UTF-8 -A /usr/share/locale/locale.alias ru_RU.UTF-8

ENV LANG ru_RU.UTF-8

CMD pytest .
