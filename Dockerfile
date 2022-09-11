FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH=/root/.local/bin:$PATH
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
COPY . .
