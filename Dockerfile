#FROM python:3.9.19-bullseye
FROM ubuntu:latest
SHELL ["/bin/bash", "-c"]
ENV PROFILES=1,2
ENV TOKEN=temp
RUN apt-get update -y
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install wget chromium-chromedriver python3 python3-venv pip git libffi-dev rustc -y
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt-get -f install -y
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN git clone https://github.com/shankershawn/hushup-invoker
WORKDIR hushup-invoker/
RUN python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install oracledb schedule selenium hvac
CMD [".venv/bin/python3", "-m", "com.shankarsan.instagram.check_profiles.py", "${PROFILES}", "${TOKEN}"]