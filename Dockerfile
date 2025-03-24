FROM python:3.12-slim

WORKDIR /project

COPY . /project

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r /project/requirements.txt --no-cache-dir


# Start the application with Gunicorn
CMD ["gunicorn", "project.wsgi:application","--bind", "0.0.0.0:8000"]