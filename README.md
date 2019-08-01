# CCBGpipe
This pipeline is designed to complete circular bacterial genomes using a sampling strategy from a sinlge MinION with barcoding


**To run with Docker**

Since CCBGpipe implements many analytical tools, we strongly recommend you to run it with Docker. Alternatively, you can install all dependencies as listed in the Installation section.

``git clone https://github.com/jade-nhri/CCBGpipe.git``

``cd CCBGpipe``

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

## Quick usage
- To extract fastq and fast5 files using extract.py

``extract.py path-to-raw_reads output (e.g., extract.py raw-reads albacore)``

- To create a Run folder and enter it

``mkdir Run && cd Run``

- To get high-quality and long-length reads using runGetFastq.py

``runGetFastq.py path-to-fast5 (e.g., runGetFastq.py ../albacore/fast5)``

- To get miniasm assemblies using runmini.py

``runmini.py``

- To run canu with the sampling strategy by using runAssembly.py

``runAssembly.py``

- To run racon and nanopolish for consensus sequence generation using runConsensus.py

``runConsensus.py path-to-fast5 (e.g., runConsensus.py ../albacore/fast5/)``

- To get circular genomes by using finalize.py

``finalize.py outpath (e.g., finalize.py ../results)``





