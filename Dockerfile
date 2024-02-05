FROM python:3.11.2
LABEL authors="witch"
WORKDIR ./kaohe
# 将当前目录复制到容器中
COPY . .
RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get install -y mariadb-server

EXPOSE 80
