FROM python:3.7.13-slim

#RUN apt-get update && apt-get install -y libgl1
RUN apt-get update && apt-get install -y python3-opencv

COPY ./src /app/src
COPY ./requeriments.txt /app

WORKDIR /app

RUN pip3 install -r requeriments.txt

EXPOSE 8000

#CMD ["uvicorn", "src.api.app:app", "--host=0.0.0.0"]
CMD ["python3", "src/main.py"]