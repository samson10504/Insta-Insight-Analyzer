# Base image
FROM python:3.10.11

# Set the working directory
WORKDIR /app

# Copy the script and configuration files
COPY scrape3.py /app
COPY config.ini /app

# Install dependencies
RUN pip install selenium beautifulsoup4 pytz

# Download and install Chrome driver
RUN apt-get update && apt-get install -y curl unzip \
    && curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb \
    && dpkg -i chrome.deb \
    && apt-get install -f -y \
    && curl https://chromedriver.storage.googleapis.com/$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$(google-chrome-stable --version | awk -F '[ .]' '{print $3}')/chromedriver_linux64.zip -o /tmp/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin \
    && rm /tmp/chromedriver_linux64.zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/local/bin:${PATH}"

# Set the volume mount
VOLUME /data

# Run the script
CMD ["python", "scrape3.py"]