#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

FROM --platform=linux/amd64 python:3

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Or your actual UID, GID on Linux if not the default 1000
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Copy requirements.txt (if found) to a temp location so we can install it. The `*`
# is required so COPY doesn't think that part of the command should fail is nothing is
# found. Also copy "noop.txt" so the COPY instruction copies _something_ to guarantee
# success somehow.
COPY *requirements.txt .devcontainer/noop.txt /tmp/pip-tmp/

# Configure apt and install packages
RUN apt-get update \
	&& apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
	#
	# Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
	&& apt-get -y install git procps lsb-release \
	#
	&& apt-get -y install build-essential libssl-dev \
	# Install pylint
	&& pip --disable-pip-version-check --no-cache-dir install pylint \
	#
	# Update Python environment based on requirements.txt (if presenet)
	&& if [ -f "/tmp/pip-tmp/requirements.txt" ]; then pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt; fi \
	&& rm -rf /tmp/pip-tmp \
	#
	# Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
	&& groupadd --gid $USER_GID $USERNAME \
	&& useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
	# [Optional] Uncomment the next three lines to add sudo support
	# && apt-get install -y sudo \
	# && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
	# && chmod 0440 /etc/sudoers.d/$USERNAME \
	#
	# Clean up
	&& apt-get autoremove -y \
	&& apt-get clean -y \
	&& rm -rf /var/lib/apt/lists/*

RUN wget https://openssl.org/source/openssl-1.0.2k.tar.gz \
	&& tar -xvf openssl-1.0.2k.tar.gz \
	&& cd openssl-1.0.2k/ \
	# --prefix will make sure that make install copies the files locally instead of system-wide
	# --openssldir will make sure that the binary will look in the regular system location for openssl.cnf
	# no-shared builds a mostly static binary
	&&./config --prefix=`pwd`/local --openssldir=/usr/lib/ssl enable-ssl2 enable-ssl3 no-shared \
	&& make depend \
	&& make \
	&& make -i install 
# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=
RUN pip install pandas
RUN pip install matplotlib
RUN pip install requests
RUN pip install bs4
RUN pip install splinter==0.17.0
RUN pip install selenium==3.11
RUN pip install aiohttp
ARG FIREFOX_VERSION=102.0.1esr
RUN FIREFOX_DOWNLOAD_URL=$(if [ $FIREFOX_VERSION = "latest" ] || [ $FIREFOX_VERSION = "nightly-latest" ] || [ $FIREFOX_VERSION = "devedition-latest" ]; then echo "https://download.mozilla.org/?product=firefox-$FIREFOX_VERSION-ssl&os=linux64&lang=en-US"; else echo "https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2"; fi) \
	&& apt-get update -qqy \
	&& apt-get -qqy --no-install-recommends install firefox-esr \
	&& rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
	&& wget --no-verbose -O /tmp/firefox.tar.bz2 $FIREFOX_DOWNLOAD_URL \
	&& apt-get -y purge firefox-esr \
	&& rm -rf /opt/firefox \
	&& tar -C /opt -xjf /tmp/firefox.tar.bz2 \
	&& rm /tmp/firefox.tar.bz2 \
	&& mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
	&& ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

#============
# GeckoDriver
#============
ARG GECKODRIVER_VERSION=0.33.0
RUN GK_VERSION=$(if [ ${GECKODRIVER_VERSION:-latest} = "latest" ]; then echo "0.33.0"; else echo $GECKODRIVER_VERSION; fi) \
	&& echo "Using GeckoDriver version: "$GK_VERSION \
	&& wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz \
	&& rm -rf /opt/geckodriver \
	&& tar -C /opt -zxf /tmp/geckodriver.tar.gz \
	&& rm /tmp/geckodriver.tar.gz \
	&& mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
	&& chmod 755 /opt/geckodriver-$GK_VERSION \
	&& ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver

