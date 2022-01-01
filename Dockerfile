FROM python:3.10 as requirements-stage
WORKDIR /tmp
RUN python -m pip install --upgrade pip
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
ENV DOCKER_RUNNING=true
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./kme /code/kme
COPY ./qcs /code/qcs
CMD ["python", "-m", "kme"]

