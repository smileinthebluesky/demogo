FROM python:3.9

COPY app/* /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0","--port=80"]
