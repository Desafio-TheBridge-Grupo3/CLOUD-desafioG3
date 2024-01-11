# Select the base image to build on top of
FROM python:3.10-bullseye

USER root

WORKDIR /home/site/wwwroot

ENV CHROME_VERSION="120.0.6099.109" \
    URL_CANDELA="https://agentes.candelaenergia.es/#/login" \
    USER_CANDELA="CA001507" \
    PASSWORD_CANDELA="CI001-507/258071" \
    JAVI_CUPS="ES0022000006250162PZ1P"

# Install essential packages
RUN apt update && \
    wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb

RUN apt install -y ./google-chrome-stable_${CHROME_VERSION}-1_amd64.deb

# Copy python code to image
COPY . .

RUN chmod 777 chromedriver-linux64/chromedriver

RUN cp chromedriver-linux64/chromedriver /usr/local/bin/

# install packages in requirements.txt
RUN pip install -r requirements.txt

CMD ["python3", "function_app.py"]

