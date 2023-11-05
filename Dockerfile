# Pull base image
FROM python:3.11.0

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 80


CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 80 --reload
