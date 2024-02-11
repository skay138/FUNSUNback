FROM tiangolo/uwsgi-nginx

# MAINTAINER Sebastian Ramirez <tiangolo@gmail.com>

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

COPY ../requirements.txt /tmp/
RUN pip3 install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt

# Add app configuration to Nginx
COPY nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/

# Copy sample app
#COPY .. /app/

# 시간대 맞추기
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# Move the base entrypoint to reuse it
RUN mv /entrypoint.sh /uwsgi-nginx-entrypoint.sh

# Copy the entrypoint that will generate Nginx additional configs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Run the start script provided by the parent image tiangolo/uwsgi-nginx which in turn will start Nginx and uWSGI
CMD ["/start.sh"]