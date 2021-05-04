from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def fetch_url(start_url):

	chrome_options = Options()
	#chrome_options.add_argument("--disable-extensions")
	#chrome_options.add_argument("--disable-gpu")
	#chrome_options.add_argument("--no-sandbox") # linux only
	chrome_options.add_argument("--headless")
	# chrome_options.headless = True # also works
	driver = webdriver.Chrome(options=chrome_options)
	
	driver.get(start_url)

	ht=driver.execute_script("return document.documentElement.scrollHeight;")
	url = []
	count = 0
	url_count = 0
	while True:
		count += 1
		prev_ht=driver.execute_script("return document.documentElement.scrollHeight;")
		driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
		time.sleep(5)
		ht=driver.execute_script("return document.documentElement.scrollHeight;")
		if prev_ht==ht:
			break

		links=driver.find_elements_by_xpath('//*[@id="video-title"]')
		for link in links:
			url_count += 1

			print(str(url_count) + ' - ' + str(count) + ' --- ' + link.get_attribute("href"))
			url.append(link.get_attribute("href"))

	with open('urls.csv', 'a+') as f:
		for link in url:
			f.write(link)

# driver.quit()


start_url = "https://www.youtube.com/channel/UC6of7UYhctnYmqABjUqzuxw/videos"

fetch_url(start_url)