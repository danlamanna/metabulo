FROM opencpu/rstudio

RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev

# https://askubuntu.com/questions/921207/installing-package-containing-glib-h
RUN dpkg -r --force-all libglib2.0-0 && \
    apt install -f -y && \
    apt install libglib2.0-0 -y && \
    apt install libglib2.0-dev -y

RUN apt-get install libcairo2-dev libxt-dev -y

RUN R -e 'install.packages("XML");' && \
    R -e 'install.packages("plotly");' && \
    R -e 'install.packages("BiocManager");' && \
    R -e 'BiocManager::install("genefilter", version = "3.8")' && \
    R -e 'BiocManager::install("GlobalAncova", version = "3.8")' && \
    R -e 'BiocManager::install("impute", version = "3.8")' && \
    R -e 'BiocManager::install("KEGGgraph", version = "3.8")' && \
    R -e 'BiocManager::install("limma", version = "3.8")' && \
    R -e 'BiocManager::install("pcaMethods", version = "3.8")' && \
    R -e 'BiocManager::install("preprocessCore", version = "3.8")' && \
    R -e 'BiocManager::install("Rgraphviz", version = "3.8")' && \
    R -e 'BiocManager::install("siggenes", version = "3.8")' && \
    R -e 'BiocManager::install("SSPA", version = "3.8")' && \
    R -e 'BiocManager::install("sva", version = "3.8")'

RUN R -e 'install.packages("devtools"); library(devtools); devtools::install_github("xia-lab/MetaboAnalystR")'
RUN R -e 'library(devtools); devtools::install_github("klutometis/roxygen")'

ADD metabulo /metabulo
RUN R -e 'library(devtools); library(roxygen2); setwd("/metabulo"); document(); setwd("/"); install("metabulo")'

CMD service cron start && /usr/lib/rstudio-server/bin/rserver && apachectl -DFOREGROUND
