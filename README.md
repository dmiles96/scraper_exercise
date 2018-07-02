# Scraper Exercise

## Description

The scrape.py file scrapes data from https://www.tide-forecast.com, as instructed. The Dockerfile builds a container with all the necessary dependencies to run scrape.py. As output, scrape.py creates a file called lowtides.json, which contains the requested data.

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
