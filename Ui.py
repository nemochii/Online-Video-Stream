from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, QVBoxLayout, \
							QLineEdit, QLabel, QScrollArea, QDesktopWidget

class Ui_set(object):
	def setupUi(self, Mainwindow):
		self.widget = QWidget(self)
		self.setCentralWidget(self.widget)

		self.videoframe = QFrame()
		self.videoframe.setMinimumSize(950, 535)
		self.palette = self.videoframe.palette()
		self.palette.setColor (QPalette.Window, QColor(0,0,0))
		self.videoframe.setPalette(self.palette)
		self.videoframe.setAutoFillBackground(True)

		self.slide = QHBoxLayout()
		self.positionslider = QSlider(Qt.Horizontal, self)
		self.positionslider.setToolTip("Position")
		self.positionslider.setMaximum(1000)
		self.positionslider.sliderMoved.connect(self.setPosition)

		self.now_time = QLabel('00:00:00')
		self.now_time.setFixedSize(49, 15)
		#self.now_time.setReadOnly(True)
		self.now_time.setUpdatesEnabled(True)

		self.total_time = QLabel('/ 00:00:00')
		self.total_time.setFixedSize(57, 15)
		#self.total_time.setReadOnly(True)
		self.total_time.setUpdatesEnabled(True)

		self.slide.addWidget(self.positionslider)
		self.slide.addWidget(self.now_time)
		self.slide.addWidget(self.total_time)

		self.hbuttonbox = QHBoxLayout()
		self.prebutton = QPushButton("Previous")
		self.hbuttonbox.addWidget(self.prebutton)
		self.prebutton.clicked.connect(self.Pre_play)

		self.playbutton = QPushButton("Play")
		self.hbuttonbox.addWidget(self.playbutton)
		self.playbutton.clicked.connect(self.Play_Pause)

		self.nextbutton = QPushButton("Next")
		self.hbuttonbox.addWidget(self.nextbutton)
		self.nextbutton.clicked.connect(self.Next_play)

		'''
		self.stopbutton = QPushButton("Stop")
		self.hbuttonbox.addWidget(self.stopbutton)
		self.stopbutton.clicked.connect(self.Stop)
		'''

		self.hbuttonbox.addStretch(1)
		self.volumeslider = QSlider(Qt.Horizontal, self)
		self.volumeslider.setMaximum(100)
		self.volumeslider.setValue(self.video_player.audio_get_volume())
		self.volumeslider.setToolTip("Volume")
		self.hbuttonbox.addWidget(self.volumeslider)
		self.volumeslider.valueChanged.connect(self.setVolume)

		self.searchareabox = QHBoxLayout()
		self.searchkey = QLineEdit()
		self.searchareabox.addWidget(self.searchkey)

		self.searchbutton = QPushButton("Search")
		self.searchareabox.addWidget(self.searchbutton)
		self.searchbutton.clicked.connect(self.crawler_thread)

		self.vboxlayout = QVBoxLayout()
		self.vboxlayout.addWidget(self.videoframe)
		self.vboxlayout.addLayout(self.slide)
		self.vboxlayout.addLayout(self.hbuttonbox)
		self.vboxlayout.addLayout(self.searchareabox)

		self.hboxlayout = QHBoxLayout()
		#self.hboxlayout.addStretch(1)
		self.hboxlayout.addLayout(self.vboxlayout)

		self.widget.setLayout(self.hboxlayout)

		self.timer = QTimer(self)
		self.timer.setInterval(200)
		self.timer.timeout.connect(self.updateUI)

		self.scroll = QScrollArea()
		self.scroll.setWidgetResizable(True)

		self.refresh_time = QTimer(self)
		self.refresh_time.setInterval(200)
		self.refresh_time.timeout.connect(self.update_list)

	def initial_location(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		x = (screen.width() - size.width()) / 3
		y = (screen.height() - size.height()) / 3
		self.move(x, y)