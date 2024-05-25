# DockerFile
# using base python image 3.10-slim
FROM python:3.10-slim

# app below is the name of the working directory
ENV APP HOME /app
WORKDIR $APP_HOME
# then copy all contents from current working directory into the container
COPY . ./

# pip install all modules mentioned inside requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# last run the gunicorn web server application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app