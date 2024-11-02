FROM python:3.11-slim

WORKDIR /fastapi

COPY ./app /fastapi/app
COPY ./alembic /fastapi/alembic
COPY ./main.py /fastapi
COPY ./alembic.ini /fastapi
COPY ./config.py /fastapi
COPY ./requirements.txt /fastapi
COPY ./start.sh /fastapi


RUN pip install --no-cache-dir -r /fastapi/requirements.txt

RUN echo "APP_CONF__DB__URL=postgresql+asyncpg://Arseniy:12345@pg:5432/images" > /fastapi/.env && \
    echo "APP_CONF__REDIS__URL=redis://redis:6379/0" >> /fastapi/.env && \
    echo "APP_CONF__RABBITMQ__URL=amqp://user:password@rabbitmq:5672" >> /fastapi/.env && \
    echo "APP_CONF__RUN__HOST=0.0.0.0" >> /fastapi/.env && \
    echo "APP_CONF__RUN__PORT=8000" >> /fastapi/.env


RUN echo "APP_CONF__DB__ECHO=1" > /fastapi/.env.template

RUN chmod +x /fastapi/start.sh

CMD ["/fastapi/start.sh"]