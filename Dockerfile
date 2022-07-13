FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction
# RUN poetry export -f requirements.txt
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
COPY . .
CMD gunicorn mobilequoter.wsgi --bind 0.0.0.0:${PORT}
