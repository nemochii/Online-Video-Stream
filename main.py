import time
import vlc
import sys
import urllib.request
import thread
from functools import partial
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QLabel, QTabWidget, QGridLayout
from Ui import Ui_set

class Main(QMainWindow, Ui_set):
	def __init__(self):
		super(self.__class__, self).__init__()
		self.resize(950, 600)

		self.instance = vlc.Instance()
		self.video_player = self.instance.media_player_new()
		#self.audio_player = self.instance.media_player_new()

		self.setWindowTitle("Online Video Stream")
		self.searched = False
		self.played = False

		self.setupUi(self)

	def crawler_thread(self):
		self.add_link = False
		self.amount_link_up = 10
		self.amount_link_down = 0

		self.grab_thread = thread.Crawler(self.searchkey.text())
		self.grab_thread.grab_signal.connect(self.show_search_result)
		self.grab_thread.start()

	def show_search_result(self, title, target, thumb):
		if not self.add_link:
			if self.searched:
				self.temp_widget.deleteLater()
			else:
				self.info_tab = QTabWidget()

			self.search_result = QVBoxLayout()
			self.temp_widget = QWidget()
			self.title = title
			self.target = target
			self.thumb = thumb

			#title, self.target, thumb = grab_video(self.searchkey.text())
		
			self.result = [None] * len(self.title)
			self.label = [None] * len(self.title)

		for entry in range(self.amount_link_down, self.amount_link_up):
			image_url = urllib.request.urlopen(self.thumb[entry]).read()
			image = QImage()
			image.loadFromData(image_url)
			self.label[entry] = QLabel(self)
			self.label[entry].setPixmap(QPixmap(image))
			self.search_result.addWidget(self.label[entry])

			self.result[entry] = QPushButton(self.title[entry])
			self.result[entry].setMaximumWidth(QPixmap(image).width())
			self.result[entry].clicked.connect(partial(self.get_video_thread, entry))
			self.search_result.addWidget(self.result[entry])

		self.scroll.setFixedWidth(QPixmap(image).width() + 50)
		self.info_tab.setFixedWidth(QPixmap(image).width() + 50)

		self.temp_widget.setLayout(self.search_result)
		self.scroll.setWidget(self.temp_widget)
		if not self.searched:
			self.searched = True
			self.info_tab.addTab(self.scroll, "PlayList")
			self.hboxlayout.addWidget(self.info_tab)

		self.refresh_time.start()

	def get_video_thread(self, entry):
		self.now = entry
		target_url = self.target[self.now]
		url = "https://www.youtube.com" + target_url

		self.get_thread = thread.Pafy(url)
		self.get_thread.video_signal.connect(self.setVideo)
		self.get_thread.start()

	def setVideo(self, video, best_video):
		if self.played:
			self.info_tab.removeTab(1)
		else:
			self.played = True

		info_dict = {
		"Title" : video.title,
		"Author" : video.author,
		"Category" : video.category,
		"Description" : video.description,
		"Likes " : str(video.likes),
		"DisLikes" : str(video.dislikes),
		"UploadDate" : video.published,
		"Uploader" : video.username,
		"Viewed" : str(video.viewcount)
		}

		w_video_info = QWidget()
		video_info = QVBoxLayout()
		video_label = [None] * len(info_dict)
		cate_grid = QGridLayout()
		for (i, v), e in zip(info_dict.items(), range(len(info_dict))):
			if i == "Title":
				video_label[e] = QLabel(v)
				video_label[e].setFont(QFont('Arial', 12, QFont.Black))
				video_label[e].setStyleSheet("color : white")
				video_label[e].setWordWrap(True)
				video_info.addWidget(video_label[e])
			else:
				cate = QLabel(i + " : ")
				cate.setFont(QFont('Arial', 8, QFont.Black))
				cate.setStyleSheet("color : white")
				cate_grid.addWidget(cate, e, 0)

				video_label[e] = QLabel(v)
				video_label[e].setStyleSheet("color : white")
				video_label[e].setWordWrap(True)
				cate_grid.addWidget(video_label[e], e ,1)
		
		video_info.addLayout(cate_grid)

		w_video_info.setLayout(video_info)
		w_video_info.setStyleSheet("background : black")
		self.info_tab.addTab(w_video_info, "VideoInfo")
		self.info_tab.setCurrentIndex(1)

		self.video_url = best_video
		#self.audio_url = best_audio

		t_time = video.length - 1
		self.total_time.setText("/ %02d:%02d:%02d" % (t_time // 3600, t_time % 3600 // 60, t_time % 3600 % 60))
		self.setWindowTitle(video.title)
		self.startPlay()
	
	def startPlay(self):
		self.media_video = self.instance.media_new(self.video_url)
		self.media_video.get_mrl()
		self.video_player.set_media(self.media_video)
		self.video_player.set_hwnd(self.videoframe.winId())
		
		'''
		self.media_audio = self.instance.media_new(self.audio_url)
		self.media_audio.get_mrl()
		self.audio_player.set_media(self.media_audio)
		'''
		
		self.Play_Pause()

	def Pre_play(self):
		self.get_video_thread(self.now - 1)

	def Next_play(self):
		self.get_video_thread(self.now + 1)

	def Play_Pause(self):
		if self.video_player.is_playing():
			self.video_player.pause()
			#self.audio_player.pause()
			self.playbutton.setText("Play")
		else:
			self.video_player.play()
			#self.audio_player.play()
			while not self.video_player.is_playing():
				pass
			self.timer.start()
			self.playbutton.setText("Pause")

	def setVolume(self, Volume):
		self.video_player.audio_set_volume(Volume)

	def setPosition(self, position):
		self.video_player.set_position(position / 1000.0)
		#self.audio_player.set_position(position / 1000.0)

	def update_list(self):
		if self.scroll.verticalScrollBar().value() == self.scroll.verticalScrollBar().maximum():
			if not self.add_link:
				if self.amount_link_up < len(self.title):
					self.add_link = True
					self.amount_link_down += 10
					self.amount_link_up = len(self.title) if self.amount_link_up + 10 > len(self.title) else self.amount_link_up + 10

					self.show_search_result(self.title, self.target, self.thumb)
					self.add_link = False
				else:
					self.refresh_time.stop()

	def updateUI(self):
		#self.audio_player.set_position(self.video_player.get_position())

		self.positionslider.setValue(self.video_player.get_position() * 1000)
		time = self.video_player.get_time() / 1000
		self.now_time.setText("%02d:%02d:%02d" % (time // 3600, time % 3600 // 60, time % 3600 % 60))

		if not self.video_player.is_playing():
			self.timer.stop()
			if self.video_player.get_length() - self.video_player.get_time() <=100:
				self.Next_play()

	def stylesheet(self):
		return ("""

			""")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainwindow = Main()
	mainwindow.initial_location()
	mainwindow.show()
	sys.exit(app.exec_())