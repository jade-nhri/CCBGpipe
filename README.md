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

``git clone https://github.com/jade-nhri/CCBGpipe.git``

``cd CCBGpipe/CCBGpipe``

``chmod +x *.py``

``export PATH="$PATH:/opt/CCBGpipe/CCBGpipe/"``

## Dependencies

- [Albacore 2.1.7]
- [Canu v1.6](http://canu.readthedocs.io)
- [samtools 1.7](http://www.htslib.org/)
- [BWA-0.7.17](http://bio-bwa.sourceforge.net)
- [cmake](h/cmkttps://cmake.org/)
- [racon v1.1.1](https://github.com/isovic/racon) - the pipeline will download and build it
- [minimap 2.10](https://github.com/lh3/minimap2) and [miniasm v0.2](https://github.com/lh3/miniasm)
- [nanopolish v0.9.0](https://github.com/jts/nanopolish)
- [Graphmap v0.3.0] (https://github.com/isovic/graphmap)


 > Before installing these dependencies it may be required to install some
 > prerequisite libraries, best installed by a package manager. On Ubuntu
 > theses are:
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
