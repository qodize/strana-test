FROM python:3.11-alpine
RUN mkdir metricsapp
WORKDIR  /metricsapp
COPY ./pyproject.toml ./
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
