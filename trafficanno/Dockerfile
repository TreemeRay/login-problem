FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-deb-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin.bash mn && chmod 777 /opt /run

WORDIR /mn

RUN mkdir /mn/static && mkdir /mn/media && chown -R mn:mn /mn && chmod 755 /mn

COPY --chown=mn:mn . .

RUN pip install -r requirements.txt

USER mn

CMD ["gunicorn", "-b", "0.0.0.0:8001", "trafficanno.wsgi:application"]