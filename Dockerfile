FROM python:3.11.1

LABEL maintainer="bmswens@gmail.com"
LABEL vcs-url="https://github.com/bmswens/Meshtastic-Web-API"
LABEL docs-url="https://bmswens.github.io/Meshtastic-Web-API/"

WORKDIR /app
RUN mkdir data
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src ./src

ENTRYPOINT ["python", "/app/src/app.py"]