import os
try:
	import requests
	from bs4 import BeautifulSoup as bs
	from clint.textui import progress
except ModuleNotFoundError:
	print("[NOTE] Some dependencies were not found on your system. Installing them automatically.")
	os.system('python -m pip install requests bs4 clint')

ids = []
pages = []
urls = []

url = "https://wall.alphacoders.com/search.php?search={}"
pageination_url = "https://wall.alphacoders.com/search.php?search={}&page={}"

def download_image(url, name, term):
	r = requests.get(url, stream=True)
	directory = './Wallpapers/' + term + ' ' + name + '.png'

	with open(directory, 'wb') as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
			if chunk:
				f.write(chunk)
				f.flush()

def download(urls):
	for url in urls:
		global term
		res = requests.get(url).text
		soup = bs(res, 'html.parser')
		image = soup.find('div',{'class':'img-container-desktop'}).find('img').get('src')
		name = soup.find('div',{'class':'img-container-desktop'}).find('img').get('alt')[14:]
		print("\nDownloading ", urls.index(url)+1, "/", len(urls))
		download_image(image, name, term)

def get_urls(pages):
	print("\n[+] Wait we're calculating the number of wallpapers available to download.\n")
	for page in pages:
		res = requests.get(page).text
		soup = bs(res,'html.parser')
		divs = soup.find_all('div',{'class':'boxgrid'})
		for div in divs:
			urls.append('https://wall.alphacoders.com/' + div.find('a').get('href'))

def get_last_page_number(soup):
	try:
		ul = soup.find('ul',{'class':'pagination'})
		number = int(ul.find_all('li')[-2].find('a').text)
		return number
	except AttributeError:
		return 1

def get_id(term):
	try:
		os.mkdir('Wallpapers')
	except FileExistsError:
		pass
	res = requests.get(url.format(term)).text
	soup = bs(res, 'html.parser')
	div = soup.find_all('div', {'class':'boxgrid'})
	for elem in div:
		ids.append(elem.find('a').get('href')[10:])
	number = get_last_page_number(soup)
	for i in range(number):
		pages.append(pageination_url.format(term, i))

	get_urls(pages)
	print("Found total ", len(urls), "wallpapers. Downloading them All (Press Ctrl + C to stop downloading)...\n")
	download(urls)

if __name__ == '__main__':
	print(r'''
  _      __     ____                         ___                  __             __       
 | | /| / /__ _/ / /__  ___ ____  ___ ____  / _ \___ _    _____  / /__  ___ ____/ /__ ____
 | |/ |/ / _ `/ / / _ \/ _ `/ _ \/ -_) __/ / // / _ \ |/|/ / _ \/ / _ \/ _ `/ _  / -_) __/
 |__/|__/\_,_/_/_/ .__/\_,_/ .__/\__/_/   /____/\___/__,__/_//_/_/\___/\_,_/\_,_/\__/_/   
                /_/       /_/                                                             
																	- By /u/SharmaDeepesh''')
	term = input('\n\nEnter the search term : ')
	get_id(term)
