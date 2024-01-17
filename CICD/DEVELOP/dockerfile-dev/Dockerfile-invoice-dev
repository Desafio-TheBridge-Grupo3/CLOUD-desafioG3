# Select the base image to build on top of
FROM python:3.12.1-bullseye

USER root

WORKDIR /home/site/wwwroot

# Copy python code to image
COPY . .

EXPOSE 5001

RUN apt-get update 

# install packages in requirements.txt
RUN pip install --upgrade pip

RUN pip install --upgrade pip setuptools

RUN pip install --upgrade setuptools

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
