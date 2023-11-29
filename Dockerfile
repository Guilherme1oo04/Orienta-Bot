FROM python:3.12

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y nodejs npm

RUN npm install -g pm2

CMD ["pm2-runtime", "start", "main.py", "--name=OrientaBot"]