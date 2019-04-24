# CCBGpipe
This pipeline is designed to complete circular bacterial genomes using a sampling strategy from a sinlge MinION with barcoding


**To run with Docker**

Since CCBGpipe implements many analytical tools, we strongly recommend you to run it with Docker. Alternatively, you can install all dependencies as listed in the Installation section.

Firstly, you need to download a Dockerfile:

``wget https://sourceforge.net/projects/sb2nhri/files/CCBGpipe/Dockerfile``

or

``git clone https://github.com/jade-nhri/CCBGpipe.git``

``cd CCBGpipe``

Then, you can build a docker imagae and run it:

``docker build -t "ccbgpipe:v1" ./``

``docker run -h ccbgpipe --name ccbgpipe -t -i -v /:/MyData ccbgpipe:v1 /bin/bash``

    Inside the docker: root@ccbgpipe:/# 
    To install java:
        apt-get update
        apt-get install -y software-properties-common
        add-apt-repository ppa:webupd8team/java
        apt-get update && apt-get install oracle-java8-installer

    Please note: the Oracle JDK license has changed starting April 16, 2019.
    You can download zulu to include Java (https://www.azul.com/downloads/zulu/).
        apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9
        apt-add-repository 'deb http://repos.azulsystems.com/ubuntu stable main'
        echo 'deb http://repos.azulsystems.com/debian stable main' > /etc/apt/sources.list.d/zulu.list
        apt-get update
        apt-get install zulu-8
        

Installation
------------
**Installation from source**

``cd /opt``

``git clone https://github.com/jade-nhri/CCBGpipe.git``

``cd CCBGpipe/CCBGpipe``

``chmod +x *.py``

``export PATH="$PATH:/opt/CCBGpipe/CCBGpipe/"``

## Dependencies

- [Albacore 2.1.7]
- [Canu v1.6](http://canu.readthedocs.io)
- [samtools 1.7](http://www.htslib.org/)
- [BWA-0.7.17](http://bio-bwa.sourceforge.net)
- [racon v1.1.1](https://github.com/isovic/racon) -
- [minimap 2.10](https://github.com/lh3/minimap2) and [miniasm v0.2](https://github.com/lh3/miniasm)
- [nanopolish v0.9.0](https://github.com/jts/nanopolish)
- [Graphmap v0.3.0](https://github.com/isovic/graphmap)


 > Before installing these dependencies it may be required to install some
 > prerequisite libraries, best installed by a package manager. On Ubuntu
 > theses are:
 > * cmake
 > * liblzma-dev
 > * libbz2-dev
 > * libz-dev
 > * libncurses-dev
 > * libcurl4-gnutls-dev
 > * libssl-dev
 > * make
 > * wget
 > * python3-all-dev
 > * parallel
 > * networkx
 > * pandas
 > * pyfastaq

## Usage
``extract.py raw_reads albacore``

``mkdir Run && cd Run``

``runGetFastq.py ../albacore/fast5``

``runmini.py``

``runAssembly.py``

``finalize.py ../results``





