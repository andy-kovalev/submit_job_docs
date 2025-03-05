FROM python:3.13.1-alpine
# RUN apk add --no-cache bash
# RUN apk add --no-cache curl

WORKDIR /usr/src/

COPY ./LICENSE ./LICENSE
COPY ./manage.py ./manage.py

COPY ./entrypoint.sh ./entrypoint.sh
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY ./docs_api ./docs_api
COPY ./docs_metadata ./docs_metadata
COPY ./docs_site ./docs_site
COPY ./submit_job_docs ./submit_job_docs
COPY ./templates ./templates
COPY ./templates_static ./templates_static

COPY ./README.md ./README.md

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/submit_job_docs/"

EXPOSE 8000

ENTRYPOINT ["/usr/src/entrypoint.sh"]
