FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirement.txt

CMD [ "python", "main.py"]

EXPOSE 8000