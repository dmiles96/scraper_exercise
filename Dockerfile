FROM centos:centos7

LABEL name="scraper-exercise"

# Install deps
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm -o /google-chrome-stable_current_x86_64.rpm \
	&& curl -L https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip -o /chromedriver_linux64.zip \
	&& curl https://bootstrap.pypa.io/get-pip.py -o /get-pip.py \
	&& yum -y install /google-chrome-stable_current_x86_64.rpm \
	&& yum -y install unzip \
	&& unzip ./chromedriver_linux64.zip -d /usr/local/bin \
	&& python /get-pip.py \
	&& pip install selenium \
	&& pip install beautifulsoup4 \
	&& pip install lxml
	
# Install user
RUN groupadd -r chrome \
	&& useradd -r -g chrome -G audio,video chrome \
	&& mkdir -p /home/chrome \
	&& chown -R chrome:chrome /home/chrome \
	&& chown -R root:root /opt/google/chrome \
	&& chmod -R 4755 /opt/google/chrome
	
# Remove downloads and clean yum
RUN rm /google-chrome-stable_current_x86_64.rpm \
	&& rm /chromedriver_linux64.zip \
	&& rm /get-pip.py \
	&& yum clean all

# copy the scraper
RUN mkdir -p /opt/scraper
COPY scrape.py /opt/scraper

# Expose port 9222
EXPOSE 9222

USER chrome

ENTRYPOINT [ "python" ]
CMD [ "/opt/scraper/scrape.py", "/data/scrape" ]
