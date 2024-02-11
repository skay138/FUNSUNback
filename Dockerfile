FROM robd003/python3.10:latest


RUN set -x \
    && apt-get update \
    # command top
    && apt-get install -y procps \
    # crontab
    && apt-get install -y cron \
    # for uwsgi
    && apt-get install --no-install-recommends --no-install-suggests -y build-essential python-dev vim \
    # supervisord
    && apt-get install -y supervisor \
    # clear
    && apt-get purge -y --auto-remove && rm -rf /var/lib/api/lists/*

# container에 git 설치
RUN apt-get install git -y

RUN mkdir /code


RUN git clone -b practice https://github.com/skay138/FUNSUNback.git /code

COPY requirements.txt /code
#COPY manage.py /code

WORKDIR /code

# RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

#uwsgi 설치
RUN pip3 install uwsgi

# 시간대 맞추기
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# collectstatic 실행
CMD ["python manage.py collectstatic --no-input"]

#RUN python /app/manage.py collectstatic --noinput