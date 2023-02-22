FROM python:3.10.8-slim
WORKDIR /app
ADD . .

RUN apt-get update --allow-insecure-repositories -y && apt-get install apt-file -y && apt-file update && apt-get install -y python3-dev build-essential
RUN pip install --upgrade pip
RUN pip install pip setuptools wheel
RUN pip install -r requirements.txt
CMD [ "python", "-u", "main.py" ]