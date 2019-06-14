import pafy
from crawler import grab_video
from PyQt5.QtCore import QThread, pyqtSignal

class Crawler(QThread):
	grab_signal = pyqtSignal(object, object, object)

	def __init__(self, search_key):
		QThread.__init__(self)
		self.search_key = search_key

	def __del__(self):
		self.wait()

	def run(self):
		title, video_url, thumb_url = grab_video(self.search_key)

		self.grab_signal.emit(title, video_url, thumb_url)

class Pafy(QThread):
	video_signal = pyqtSignal(object, object)

	def __init__(self, url):
		QThread.__init__(self)
		self.url = url

	def __del__(self):
		self.wait()

	def run(self):
		video = pafy.new(self.url)
		#best_video = video.getbestvideo()
		#best_audio = video.getbestaudio()
		best_video = video.getbest()

		self.video_signal.emit(video, best_video.url)