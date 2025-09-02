import os
import re
import yt_dlp  # type: ignore
import PySide6.QtWidgets as w
from PySide6.QtCore import Qt


class MainScreen(w.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 600, 400)

        # Set a light gray background color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border-color: #357abd;
            }
            QPushButton {
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 12px;
                color: white;
                min-width: 180px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
            #videoButton {
                background-color: #4a90e2;
            }
            #videoButton:hover {
                background-color: #357abd;
            }
            #audioButton {
                background-color: #28a745;
            }
            #audioButton:hover {
                background-color: #218838;
            }
        """)

        central_widget = w.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = w.QVBoxLayout(central_widget)

        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)

        main_layout.addStretch()

        self.url_input = w.QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube Link")
        self.url_input.setSizePolicy(
            w.QSizePolicy.Policy.Expanding, w.QSizePolicy.Policy.Fixed
        )
        self.url_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.url_input)

        button_layout = w.QHBoxLayout()
        button_layout.setSpacing(20)

        self.video_button = w.QPushButton("Download as Video")
        self.video_button.setObjectName("videoButton")
        self.video_button.clicked.connect(self.show_video_quality_dialog)

        self.audio_button = w.QPushButton("Download as Audio")
        self.audio_button.setObjectName("audioButton")
        self.audio_button.clicked.connect(self.download_audio)

        button_layout.addWidget(self.video_button)
        button_layout.addWidget(self.audio_button)

        main_layout.addLayout(button_layout)

        main_layout.addStretch()

    def show_video_quality_dialog(self) -> None:
        url = self.url_input.text().strip()

        if not url:
            w.QMessageBox.warning(self, "Warning", "Please enter a YouTube URL first!")
            return

        if not self.check_link(url):
            w.QMessageBox.warning(self, "Warning", "Please enter a valid YouTube URL!")
            return

        dialog = w.QDialog(self)
        dialog.setWindowTitle("Select Video Quality")
        dialog.setModal(True)
        dialog.resize(300, 200)

        layout = w.QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Quality options
        qualities = ["Best Quality", "1080p", "720p", "480p", "360p", "Worst Quality"]

        label = w.QLabel("Choose video quality:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        quality_combo = w.QComboBox()
        quality_combo.addItems(qualities)
        quality_combo.setCurrentText("Best Quality")
        layout.addWidget(quality_combo)

        # Buttons
        button_layout = w.QHBoxLayout()
        download_btn = w.QPushButton("Download")
        cancel_btn = w.QPushButton("Cancel")

        download_btn.clicked.connect(
            lambda: self.download_video(quality_combo.currentText(), dialog)
        )
        cancel_btn.clicked.connect(dialog.reject)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(download_btn)
        layout.addLayout(button_layout)

        dialog.exec()

    def get_download_path(self) -> str:
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube")

        os.makedirs(downloads_dir, exist_ok=True)

        return downloads_dir

    def check_link(self, link: str) -> bool:
        regex = re.compile(
            r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?"
        )

        return bool(regex.fullmatch(link))

    def download_video(self, quality: str, dialog: w.QDialog) -> None:
        quality_map = {
            "Best Quality": "best",
            "1080p": "best[height<=1080]",
            "720p": "best[height<=720]",
            "480p": "best[height<=480]",
            "360p": "best[height<=360]",
            "Worst Quality": "worst",
        }

        video_opts = {
            "format": quality_map[quality],
            "quiet": True,
            "outtmpl": os.path.join(self.get_download_path(), "%(title)s.%(ext)s"),
            "noplaylist": True,
        }

        url = self.url_input.text().strip()

        # Show loading cursor
        w.QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        with yt_dlp.YoutubeDL(video_opts) as dl:
            dl.download(url)

        # Restore normal cursor
        w.QApplication.restoreOverrideCursor()

        w.QMessageBox.information(
            self,
            "Download Complete",
            f"Video downloaded in {quality} quality!",
        )

        dialog.accept()

    def download_audio(self) -> None:
        audio_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "outtmpl": os.path.join(self.get_download_path(), "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "noplaylist": True,
        }

        url = self.url_input.text().strip()

        if not url:
            w.QMessageBox.warning(self, "Warning", "Please enter a YouTube URL first!")
            return

        if not self.check_link(url):
            w.QMessageBox.warning(self, "Warning", "Please enter a valid YouTube URL!")
            return

        # Show loading cursor
        w.QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        with yt_dlp.YoutubeDL(audio_opts) as dl:
            dl.download(url)

        # Restore normal cursor
        w.QApplication.restoreOverrideCursor()

        w.QMessageBox.information(
            self, "Download Complete", "Audio downloaded successfully!"
        )


if __name__ == "__main__":
    app = w.QApplication([])
    window = MainScreen()
    window.show()
    app.exec()
