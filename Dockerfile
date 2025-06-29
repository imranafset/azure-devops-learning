FROM jenkins/jenkins:jdk21
User root
RUN apt-get update && apt-get install -y python3 python3-pip 
RUN python3 --version && pip3 --version
User jenkins