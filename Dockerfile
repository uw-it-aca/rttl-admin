FROM gcr.io/uwit-mci-axdd/django-container:1.2.7 as app-container

USER root

RUN apt-get update && apt-get install libpq-dev -y

USER acait

ADD --chown=acait:acait rttl_admin/VERSION /app/rttl_admin/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

RUN . /app/bin/activate && pip install nodeenv && nodeenv -p &&\
    npm install -g npm && ./bin/npm install less -g

FROM gcr.io/uwit-mci-axdd/django-test-container:1.2.7 as app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
