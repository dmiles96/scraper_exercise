# Scraper Exercise

## Description

As an exercise, I created a python file that scrapes data from https://www.tide-forecast.com. The python code itself is nothing special; it was written in a day. However, as I worked on the project, it seemed like a number of people ran into issues running Chrome and Selenium in a Docker container. So, this project can be used as a reference/example on how to do just that.

The Dockerfile builds a container with all the necessary dependencies to run scrape.py. As output, scrape.py creates a file called lowtides.json, which contains the requested data.

## How to Run

1. [Install Docker](https://docs.docker.com/install/).
2. Download [the docker image](https://github.com/dmiles96/scraper_exercise/releases/download/v1.0/scraper_exercise.tar).
3. Load the docker image -
	* On OS X/Linux: `docker load --input scraper_exercise.tar`
	* On Windows (at command prompt): `docker load --input scraper_exercise.tar`
4. Run the container -
	* On OS X/Linux: `docker run --rm -v /tmp:/data/scrape scraper:exercise`
	* On Windows (at command prompt): `docker run --rm -v %TMP%:/data/scrape scraper:exercise`
5. Print the output -
	* On OS X/Linux: `cat /tmp/lowtides.json`
	* On Windows (at command prompt): `type %TMP%\lowtides.json`
