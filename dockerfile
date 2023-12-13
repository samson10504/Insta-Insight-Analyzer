# Base image
FROM python:3.10.11

# Set the working directory
WORKDIR /app

# Copy the script and configuration files
COPY scrape3.py /app
COPY config.ini /app

# Install dependencies
RUN pip install selenium beautifulsoup4 pytz

# TODO: Download and install Chrome driver
RUN apt-get update && apt-get install -y curl unzip 

# Set environment variables
ENV PATH="/usr/local/bin:${PATH}"

# Set the volume mount
VOLUME /data

# Run the script
CMD ["python", "scrape3.py"]