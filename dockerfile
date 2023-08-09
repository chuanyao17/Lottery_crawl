# Use Python 3.7.8 as the base image
FROM python:3.7.8

# Set the working directory
WORKDIR /app

# Copy the contents of the current directory to the /app directory in the container
COPY . /app

# Install the required packages in the Docker image
RUN pip install selenium==4.9.1 undetected-chromedriver==3.4.7

# Install the Chrome browser
RUN apt-get update && apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Set up Chrome options
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV CHROME_DRIVER=/usr/local/bin/chromedriver


# Run the program
CMD ["bash", "-c", "if [[ -z \"$DEBUG\" ]]; then python ./lottery_crawl.py; else /bin/bash; fi"]
