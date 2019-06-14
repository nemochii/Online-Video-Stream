import requests as rq
from bs4 import BeautifulSoup

def grab_video(key_word):
	key_word.replace(" ", "+")

	url = "https://www.youtube.com/results?search_query=" + key_word
	response = rq.get(url)
	html_doc = response.text
	soup = BeautifulSoup(response.text, 'lxml')

	r = soup.select('a.yt-uix-tile-link.yt-ui-ellipsis.yt-ui-ellipsis-2.yt-uix-sessionlink.spf-link')
	title = []
	video_url = []
	thumb_url = []
	for entry in r:
		if entry['href'][1] == "w":
			if len(entry['href']) <= 20:
				title.append(entry['title'])
				video_url.append(entry['href'])
				thumb_url.append("http://i.ytimg.com/vi/" + entry['href'][9:] + "/0.jpg")
		if len(title) >= 50:
			break
			
	return (title, video_url, thumb_url)