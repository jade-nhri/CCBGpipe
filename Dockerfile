FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    wget dos2unix \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    cmake unzip git
RUN pip3 install networkx
RUN pip3 install pandas
RUN pip3 install pyfastaq

##Download CCGBpipe
WORKDIR /opt
RUN git clone https://github.com/jade-nhri/CCBGpipe.git
WORKDIR /opt/CCBGpipe/CCBGpipe
RUN chmod +x *.py


#albacore 2.1.7
#This software requires the user to download manually!!!


#samtools 1.7
ADD https://github.com/samtools/samtools/releases/download/1.7/samtools-1.7.tar.bz2 /opt
RUN apt-get update && apt-get install -y \
    libncurses-dev \
    apt-file \
    liblzma-dev \
    libz-dev \
    libbz2-dev \
    vim parallel
WORKDIR /opt
RUN tar -xjf /opt/samtools-1.7.tar.bz2
WORKDIR /opt/samtools-1.7
RUN make && make install
WORKDIR /

#bwa BWA-0.7.17
WORKDIR /opt
RUN git clone https://github.com/lh3/bwa.git
WORKDIR /opt/bwa
RUN make
WORKDIR /

#nanopolish v0.9.0
RUN apt-get update && apt-get install -y python-pip python-dev python-biopython build-essential python-matplotlib
WORKDIR /opt
RUN git clone --recursive https://github.com/jts/nanopolish.git
WORKDIR /opt/nanopolish
RUN git checkout v0.9.0
RUN make
WORKDIR /

#canu v1.6
WORKDIR /opt
RUN wget https://github.com/marbl/canu/archive/v1.6.tar.gz
RUN gunzip -dc v1.6.tar.gz | tar -xf -
WORKDIR /opt/canu-1.6/src
RUN make -j 16
WORKDIR /

#MUMmer 3.23
WORKDIR /opt
RUN wget https://sourceforge.net/projects/mummer/files/mummer/3.23/MUMmer3.23.tar.gz
RUN tar -zxvf MUMmer3.23.tar.gz
WORKDIR /opt/MUMmer3.23
RUN make
RUN make install
WORKDIR /

#Minimap2, miniasm-0.2
WORKDIR /opt
RUN curl -L https://github.com/lh3/minimap2/releases/download/v2.10/minimap2-2.10_x64-linux.tar.bz2  | tar -jxvf -
RUN wget https://github.com/lh3/miniasm/archive/v0.2.tar.gz \
    && tar -xzf v0.2.tar.gz \
    && (cd /opt/miniasm-0.2 && make) \
    && rm v0.2.tar.gz
WORKDIR /

#Racon1.1.1
WORKDIR /opt
RUN wget https://github.com/isovic/racon/releases/download/1.1.1/racon-v1.1.1.tar.gz \
    && tar -xzf racon-v1.1.1.tar.gz \
    && (cd /opt/racon-v1.1.1 && cmake -DCMAKE_BUILD_TYPE=Release && make) \
    && rm racon-v1.1.1.tar.gz
WORKDIR /


#Graphmap v0.3.0
WORKDIR /opt
RUN git clone https://github.com/isovic/graphmap.git
WORKDIR /opt/graphmap
RUN make modules && make
WORKDIR /

#set path
ENV PATH $PATH:/opt:/opt/CCBGpipe/CCBGpipe:/opt/samtools-1.7/bin:/opt/bwa:/opt/nanopolish:/opt/canu-1.6/Linux-amd64/bin:/opt/MUMmer3.23:/opt/minimap2-2.10_x64-linux/:/opt/miniasm-0.2:/opt/racon-v1.1.1/bin:/opt/graphmap/bin/Linux-x64
