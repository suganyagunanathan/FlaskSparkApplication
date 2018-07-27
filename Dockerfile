FROM python:3.6-jessie

ADD read_write_s3.py /

RUN apt-get update && \
    apt-get install -y \
    zip

RUN pip install \
        twine \
        wheel \
        pylint \
        tox \
        sphinx \
        sphinx_rtd_theme \
        bandit

RUN apt-get install -y software-properties-common
RUN add-apt-repository "deb http://ppa.launchpad.net/webupd8team/java/ubuntu xenial main"
RUN apt-get update -y
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN apt-get install -y oracle-java8-installer
ENV JAVA_HOME="/usr/lib/jvm/java-8-oracle"
RUN wget http://www.gtlib.gatech.edu/pub/apache/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
RUN tar -xvf spark-2.3.0-bin-hadoop2.7.tgz
ENV SPARK_HOME=/spark-2.3.0-bin-hadoop2.7
ENV PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$PATH 

RUN pip install boto3
RUN pip install Flask==0.10.1


CMD [ "spark-submit", "./read_write_s3.py" ]