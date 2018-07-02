from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import os
import sys
		
def scrape_low_tides(driver, element_wait_timeout, county_name, region_name, location_name):
	# make sure we're in the context of the search bar
	driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])

	# select the country
	driver.find_element_by_xpath("//select[@id='country_id']/option[text() = '" + county_name + "']").click()

	# select the region
	region_option_xpath = "//select[@id='region_id']/option[text() = '" + region_name + "']"
	region_option_xpath_present = EC.presence_of_element_located((By.XPATH, region_option_xpath))
	WebDriverWait(driver, element_wait_timeout).until(region_option_xpath_present)
	driver.find_element_by_xpath(region_option_xpath).click()

	# select the location
	location_option_xpath = "//select[@id='location_filename_part']/option[text() = '" + location_name + "']"
	location_option_xpath_present = EC.presence_of_element_located((By.XPATH, location_option_xpath))
	WebDriverWait(driver, element_wait_timeout).until(location_option_xpath_present)
	driver.find_element_by_xpath(location_option_xpath).click()
	
	# click the go button
	driver.find_element_by_xpath("//input").click()

	#wait for the table to load
	table_xpath = "//section/table"
	table_xpath_present = EC.presence_of_element_located((By.XPATH, table_xpath))
	WebDriverWait(driver, element_wait_timeout).until(table_xpath_present)
	driver.find_element_by_xpath(table_xpath).click()
	
	page = BeautifulSoup(driver.page_source, 'lxml')

	# parse html and load it into rows
	rows = []
	current_date = None		
	table = page.find_all('table')[0]
	for tbodyChild in table.tbody.children:
		if tbodyChild.name == 'tr':
			row = {}
			tr = tbodyChild
			for trChild in tr.children:
				if trChild.name == 'td':
					td = trChild
					if len(td.attrs) > 0:					
						if 'date' in td['class']:
							row['date'] = td.string
							current_date = td.string							
						elif 'time' in td['class']:
							row['time'] = td.string
						elif 'time-zone' in td['class']:
							row['time_zone'] = td.string
						elif 'level' in td['class']:
							if len(td['class']) == 1:
								if len(td.contents) > 0:
									row['level'] = td.span.string
							else:
								row['level_metric'] = td.string
						elif 'tide' in td['class']:
							row['tide'] = td.string
					else:
						row['tide'] = td.string
			if not 'date' in row:
				row['date'] = current_date
			rows.append(row)

	# find and store daylight low tides
	(NEED_SUNSET_OR_SUNRISE, NEED_SUNRISE, SUN_ROSE) = range(3)	
	daylight_low_tides = []
	state = NEED_SUNSET_OR_SUNRISE
	for row in rows:
		if state == NEED_SUNSET_OR_SUNRISE:
			if row['tide'] == "Low Tide":
				row['country'] = county_name
				row['region'] = region_name
				row['location'] = location_name	

				daylight_low_tides.append(row) # collect low tide just in case the sun rose
			elif row['tide'] == "Sunrise":
				daylight_low_tides = [] # if it turns out the sun didn't rise, yet, clear lowtides
				state = SUN_ROSE
			elif row['tide'] == "Sunset":
				state = NEED_SUNRISE
		elif state == NEED_SUNRISE:
			if row['tide'] == "Sunrise":
				state = SUN_ROSE
		elif state == SUN_ROSE:
			if row['tide'] == "Low Tide":
				row['country'] = county_name
				row['region'] = region_name
				row['location'] = location_name	

				daylight_low_tides.append(row)
			elif row['tide'] == "Sunset":
				state = NEED_SUNRISE

							
	return daylight_low_tides
	

# create web driver options
option = webdriver.ChromeOptions()
option.add_argument("--disable-gpu")
option.add_argument("--headless")
option.add_argument("--no-sandbox")
option.add_argument("--remote-debugging-port=9222")
option.add_argument("--remote-debugging-address=0.0.0.0")
option.add_argument("--window-size=1440,900")

element_wait_timeout = 30

try:
	driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
	driver.get("https://www.tide-forecast.com/")

	# wait for search bar to load
	iframe_present = EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
	WebDriverWait(driver, element_wait_timeout).until(iframe_present)

	half_moon_bay_lowtides = scrape_low_tides(driver, element_wait_timeout, 'United States', 'California', 'Half Moon Bay')
	huntington_beach_lowtides = scrape_low_tides(driver, element_wait_timeout, 'United States', 'California', 'Huntington Beach')
	providence_lowtides = scrape_low_tides(driver, element_wait_timeout, 'United States', 'Rhode Island', 'Providence')
	wrightsville_beach_lowtides = scrape_low_tides(driver, element_wait_timeout, 'United States', 'North Carolina', 'Wrightsville Beach')
	
	all_lowtides = half_moon_bay_lowtides + huntington_beach_lowtides + providence_lowtides + wrightsville_beach_lowtides
	all_lowtides_json = json.dumps(all_lowtides, indent=4, sort_keys=True)
	
	output_basedir = sys.argv[1]
	output_file = os.path.join(output_basedir, "lowtides.json")
	with open(output_file, 'w') as f:    
		f.write(all_lowtides_json)

finally:
	driver.quit()

