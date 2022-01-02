import helpers as hlp
import os
import pdf_combiner
from PySide6 import QtCore, QtWidgets
import sys


class PDFCombinerGui(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.selection_type = 'Folder'
        self.output_folder = str(os.path.join(os.getcwd(), 'downloads'))
        self.download_status = 'Status: Pending Inputs'
        self.youtube_filled = False
        self.destination_filled = True  # set to true as it defaults to download directory
        self.download_complete = False
        self.download_button = QtWidgets.QPushButton("Press to Combine", self)
        self.yt_text = QtWidgets.QLabel(self)
        self.folder_text = QtWidgets.QLabel(self)
        self.download_status_button = QtWidgets.QLabel(self)
        self.change_status_text(self.download_status)
        self.init_ui()

    def change_status_text(self, input_text):
        self.download_status_button.setText(input_text)
        self.download_status_button.adjustSize()
        return None

    def check_dl_button_status(self):
        # check if both YouTube box and download destination is filled
        if self.youtube_filled & self.destination_filled:
            self.download_button.setEnabled(True)
        return None

    def init_ui(self):

        # allows user to enter YouTube link
        youtube_btn = QtWidgets.QPushButton('Enter Youtube Link', self)
        youtube_btn.move(20, 20)
        youtube_btn.clicked.connect(self.show_youtube_dialog)
        self.yt_text.move(130, 25)
        self.yt_text.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        # allows user to select file location
        file_location_btn = QtWidgets.QPushButton('Enter folder link', self)
        file_location_btn.move(20, 50)
        file_location_btn.clicked.connect(self.show_folder_dialog)
        self.folder_text.setText(str(self.output_folder))
        self.folder_text.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.folder_text.move(130, 55)

        # create buttons to select video or audio download
        video_button = QtWidgets.QRadioButton('Video', self)
        video_button.move(130, 90)
        audio_button = QtWidgets.QRadioButton('Audio', self)
        audio_button.move(190, 90)

        # continue to fill in audio and video
        buttongroup = QtWidgets.QButtonGroup()
        buttongroup.addButton(video_button)
        buttongroup.addButton(audio_button)

        video_button.toggled.connect(self.on_clicked_video_audio)
        audio_button.toggled.connect(self.on_clicked_video_audio)
        video_button.setChecked(True)  # initialize with Video checked

        # status of download

        self.download_status_button.move(130, 120)
        self.download_status_button.setAlignment(QtCore.Qt.AlignCenter)

        # press button for download

        self.download_button.setEnabled(False)
        self.download_button.move(140, 150)
        self.download_button.clicked.connect(self.youtube_dl)

        # allows user to close
        close_button = QtWidgets.QPushButton("Press to Close", self)
        close_button.move(180, 200)
        close_button.clicked.connect(self.close)

        # create overall interface
        self.setGeometry(300, 300, 450, 200)
        self.setWindowTitle('Youtube Downloader')
        self.show()

    def show_folder_dialog(self):
        text, ok = self.get_directory()
        if ok:
            self.folder_text.setText(str(text))
            self.output_folder = str(text)

    def show_youtube_dialog(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Enter Youtube Link',
                                                  'Enter Youtube Link:')
        # if something is entered
        if ok:
            self.youtube_link = str(text)
            self.yt_text.setText(self.youtube_link)
            self.yt_text.adjustSize()
            self.youtube_filled = True
            self.check_dl_button_status()
            self.change_status_text('Status: Pending Inputs')

    def get_directory(self):
        folder_name = self.output_folder
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDirectory(folder_name)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)  # only allow directory to be opened
        dialog.setViewMode(QtWidgets.QFileDialog.List)
        if dialog.exec():
            folder_name = dialog.selectedFiles()[0]  # returns list so pop first value off
            self.folder_text.adjustSize()
            self.destination_filled = True
            self.check_dl_button_status()
            self.change_status_text('Status: Pending Inputs')

        return folder_name, True

    def on_clicked_video_audio(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.download_type = radio_button.text()
        return None

    def youtube_dl(self):
        self.change_status_text('Status: Downloading')
        hlp.youtube_dl(self.output_folder, self.download_type, self.youtube_link)
        self.change_status_text('Status: Download Complete')


def pdf_combiner_gui():
    hlp.initialize()
    app = QtWidgets.QApplication(sys.argv)
    yt = PDFCombinerGui()
    sys.exit(app.exec())




if __name__ == '__main__':
    pdf_combiner_gui()