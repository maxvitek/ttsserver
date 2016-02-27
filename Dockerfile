FROM python:2.7.11

ADD requirements.txt speech.py tts_server.py /
ADD templates /templates/

RUN pip install -U pip && pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "tts_server.py"]
