# 使用 Python 3.7.8 作為基礎映像
FROM python:3.7.8

# 設定工作目錄
WORKDIR /app

# 將當前目錄的內容複製到容器的 /app 目錄下
COPY . /app

# 在 Docker 映像中安裝所需的套件
RUN pip install selenium==4.9.1 undetected-chromedriver==3.4.7

# 安裝 Chrome 瀏覽器及驅動程式
RUN apt-get update && apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# 設置 Chrome 選項
ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV CHROME_DRIVER=/usr/local/bin/chromedriver


# 運行程序
CMD ["bash", "-c", "if [[ -z \"$DEBUG\" ]]; then python ./lottery_crawl.py; else /bin/bash; fi"]
