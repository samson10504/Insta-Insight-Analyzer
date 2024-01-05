FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium

# Set the working directory
WORKDIR /app

# Copy the script and configuration files
COPY scrape4.py /app
COPY config.ini /app

# Install dependencies
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y curl unzip 
