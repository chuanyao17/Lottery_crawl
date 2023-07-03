# 使用 Python 3.7.8 作為基礎映像
FROM public.ecr.aws/lambda/python:3.7

# 將當前目錄的內容複製到容器的 /var/task 目錄下
COPY . /var/task

# 在 Docker 映像中安裝所需的套件
RUN pip install selenium==4.9.1 undetected-chromedriver==3.4.7

# 安裝 Chrome 瀏覽器及驅動程式
RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# 設置 Chrome 選項
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV CHROME_DRIVER=/usr/local/bin/chromedriver

# 將啟動指令設置為我們的 Python 腳本
CMD [ "lottery_crawl.handler" ]
