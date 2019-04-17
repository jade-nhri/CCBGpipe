# CCBGpipe
This pipeline is designed to complete circular bacterial genomes using a sampling strategy from a sinlge MinION with barcoding

Installation
------------
**To run with Docker**

``wget https://sourceforge.net/projects/sb2nhri/files/CCBGpipe/Dockerfile``

``docker build -t "ccbgpipe:v1" ./``

``docker run -h ccbgpipe --name ccbgpipe -t -i -v /:/MyData ccbgpipe:v1 /bin/bash``

    Inside the docker: root@ccbgpipe:/# 
    To install java:
        apt-get update
        apt-get install -y software-properties-common
        add-apt-repository ppa:webupd8team/java
        apt-get update && apt-get install oracle-java8-installer

**Installation from source**

``cd /opt``
``git clone ``


 > Before installing medaka it may be required to install some
 > prerequisite libraries, best installed by a package manager. On Ubuntu
 > theses are:
 > * gcc
 > * zlib1g-dev
 > * libbz2-dev
 > * liblzma-dev
 > * libffi-dev
 > * libncurses5-dev
 > * libcurl4-gnutls-dev
 > * libssl-dev
 > * make
 > * wget
 > * python3-all-dev
 > * python-virtualenv
