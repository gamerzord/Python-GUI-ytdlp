from pathlib import Path
from typing import Dict, Any

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QGroupBox, QLabel, QLineEdit, QPushButton, QComboBox,
    QCheckBox, QProgressBar, QTextEdit, QFileDialog, QMessageBox,
    QGridLayout
)
from PySide6.QtCore import QThread
from PySide6.QtGui import QFont

from workers import DownloadWorker, InfoWorker
from dialogs import VideoInfoDialog
from command import CommandBuilder
from theme import apply_theme


class YtDlpGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("yt-dlp GUI")
        self.setGeometry(100, 100, 900, 700)
        
        # Worker threads
        self.download_thread = None
        self.download_worker = None
        self.info_thread = None
        self.info_worker = None
        
        # State
        self.is_downloading = False
        
        # Command builder
        self.command_builder = CommandBuilder()
        
        self.setup_ui()
        self.setup_styling()
        self.check_ytdlp_installation()
    
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Setup tabs
        self.setup_download_tab()
        self.setup_advanced_tab()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def setup_download_tab(self):
        """Setup the main download tab"""
        download_widget = QWidget()
        layout = QVBoxLayout()
        download_widget.setLayout(layout)
        
        # URL input group
        url_group = QGroupBox("Video URL")
        url_layout = QVBoxLayout()
        url_group.setLayout(url_layout)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter video URL here...")
        url_layout.addWidget(self.url_input)
        
        layout.addWidget(url_group)
        
        # Options group
        options_group = QGroupBox("Download Options")
        options_layout = QVBoxLayout()
        options_group.setLayout(options_layout)
        
        # Download path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Download Path:"))
        
        self.path_input = QLineEdit()
        self.path_input.setText(str(Path.home() / "Downloads"))
        path_layout.addWidget(self.path_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_download_path)
        path_layout.addWidget(browse_btn)
        
        options_layout.addLayout(path_layout)
        
        # Format and quality
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["best", "worst", "mp4", "webm", "mkv", "avi", "mp3", "m4a", "opus"])
        format_layout.addWidget(self.format_combo)
        
        format_layout.addWidget(QLabel("Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["best", "worst", "1080p", "720p", "480p", "360p", "240p"])
        format_layout.addWidget(self.quality_combo)
        
        format_layout.addStretch()
        options_layout.addLayout(format_layout)
        
        # Checkboxes
        checkbox_layout = QHBoxLayout()
        
        self.audio_only_cb = QCheckBox("Audio Only")
        checkbox_layout.addWidget(self.audio_only_cb)
        
        self.subtitle_cb = QCheckBox("Download Subtitles")
        checkbox_layout.addWidget(self.subtitle_cb)
        
        self.playlist_cb = QCheckBox("Download Playlist")
        checkbox_layout.addWidget(self.playlist_cb)
        
        checkbox_layout.addStretch()
        options_layout.addLayout(checkbox_layout)
        
        layout.addWidget(options_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.download_btn = QPushButton("Download")
        self.download_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        self.download_btn.clicked.connect(self.start_download)
        button_layout.addWidget(self.download_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; }")
        self.stop_btn.clicked.connect(self.stop_download)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        self.info_btn = QPushButton("Get Info")
        self.info_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; }")
        self.info_btn.clicked.connect(self.get_video_info)
        button_layout.addWidget(self.info_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Output log
        log_group = QGroupBox("Output Log")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 9))
        self.log_output.setMaximumHeight(200)
        log_layout.addWidget(self.log_output)
        
        layout.addWidget(log_group)
        
        self.tab_widget.addTab(download_widget, "Download")
    
    def setup_advanced_tab(self):
        """Setup the advanced options tab"""
        advanced_widget = QWidget()
        layout = QVBoxLayout()
        advanced_widget.setLayout(layout)
        
        # Custom arguments group
        args_group = QGroupBox("Custom Arguments")
        args_layout = QVBoxLayout()
        args_group.setLayout(args_layout)
        
        args_layout.addWidget(QLabel("Additional yt-dlp arguments:"))
        self.custom_args_input = QLineEdit()
        self.custom_args_input.setPlaceholderText("e.g., --write-thumbnail --embed-metadata")
        args_layout.addWidget(self.custom_args_input)
        
        layout.addWidget(args_group)
        
        # Audio options group
        audio_group = QGroupBox("Audio Options")
        audio_layout = QGridLayout()
        audio_group.setLayout(audio_layout)
        
        audio_layout.addWidget(QLabel("Audio Format:"), 0, 0)
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["best", "mp3", "m4a", "opus", "vorbis", "aac", "flac", "wav"])
        audio_layout.addWidget(self.audio_format_combo, 0, 1)
        
        audio_layout.addWidget(QLabel("Audio Quality:"), 1, 0)
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["best", "320", "256", "192", "128", "96", "64"])
        audio_layout.addWidget(self.audio_quality_combo, 1, 1)
        
        layout.addWidget(audio_group)
        
        # Video options group
        video_group = QGroupBox("Video Options")
        video_layout = QGridLayout()
        video_group.setLayout(video_layout)
        
        video_layout.addWidget(QLabel("Video Codec:"), 0, 0)
        self.video_codec_combo = QComboBox()
        self.video_codec_combo.addItems(["best", "h264", "h265", "vp9", "av01"])
        video_layout.addWidget(self.video_codec_combo, 0, 1)
        
        self.embed_subs_cb = QCheckBox("Embed Subtitles")
        video_layout.addWidget(self.embed_subs_cb, 1, 0)
        
        self.write_thumbnail_cb = QCheckBox("Save Thumbnail")
        video_layout.addWidget(self.write_thumbnail_cb, 1, 1)
        
        layout.addWidget(video_group)
        
        # SponsorBlock options (imported from sponsorblock module)
        from sponsorblock import create_sponsorblock_group
        sponsor_group = create_sponsorblock_group()
        
        # Get the widgets we need to access later
        self.sponsorblock_cb = sponsor_group.findChild(QCheckBox, "sponsorblock_cb")
        self.sponsor_categories_input = sponsor_group.findChild(QLineEdit, "sponsor_categories_input")
        
        layout.addWidget(sponsor_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(advanced_widget, "Advanced")
    
    def setup_styling(self):
        """Apply application styling"""
        apply_theme(self)
    
    def check_ytdlp_installation(self):
        """Check if yt-dlp is installed"""
        if self.command_builder.check_installation():
            version = self.command_builder.get_version()
            self.log(f"yt-dlp version: {version}")
            self.statusBar().showMessage("yt-dlp ready")
        else:
            QMessageBox.critical(self, "Error", 
                               "yt-dlp is not installed or not found in PATH.\n"
                               "Please install it using:\npip install yt-dlp")
            self.download_btn.setEnabled(False)
            self.info_btn.setEnabled(False)
            self.statusBar().showMessage("yt-dlp not found!")
    
    def get_ui_options(self) -> Dict[str, Any]:
        """Get current UI options as dictionary"""
        return {
            'url': self.url_input.text().strip(),
            'output_path': self.path_input.text(),
            'format': self.format_combo.currentText(),
            'quality': self.quality_combo.currentText(),
            'audio_only': self.audio_only_cb.isChecked(),
            'subtitle': self.subtitle_cb.isChecked(),
            'playlist': self.playlist_cb.isChecked(),
            'audio_format': self.audio_format_combo.currentText(),
            'audio_quality': self.audio_quality_combo.currentText(),
            'embed_subs': self.embed_subs_cb.isChecked(),
            'write_thumbnail': self.write_thumbnail_cb.isChecked(),
            'sponsorblock': self.sponsorblock_cb.isChecked(),
            'sponsor_categories': self.sponsor_categories_input.text(),
            'custom_args': self.custom_args_input.text().strip()
        }
    
    def browse_download_path(self):
        """Browse for download directory"""
        folder = QFileDialog.getExistingDirectory(self, "Select Download Directory", 
                                                 self.path_input.text())
        if folder:
            self.path_input.setText(folder)
    
    def log(self, message: str):
        """Add message to log"""
        self.log_output.append(message)
        
        # Auto-scroll to bottom
        from PySide6.QtGui import QTextCursor
        cursor = self.log_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_output.setTextCursor(cursor)
    
    def start_download(self):
        """Start download process"""
        try:
            if self.is_downloading:
                return
            
            options = self.get_ui_options()
            cmd = self.command_builder.build_download_command(options)
            self.log(f"Starting download: {' '.join(cmd)}")
            
            # Setup worker and thread
            self.download_worker = DownloadWorker()
            self.download_thread = QThread()
            
            self.download_worker.moveToThread(self.download_thread)
            
            # Connect signals
            self.download_worker.output_received.connect(self.log)
            self.download_worker.progress_updated.connect(self.progress_bar.setValue)
            self.download_worker.download_finished.connect(self.download_finished)
            
            # Start download when thread starts
            self.download_thread.started.connect(lambda: self.download_worker.start_download(cmd))
            
            # UI state
            self.is_downloading = True
            self.download_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            self.statusBar().showMessage("Downloading...")
            
            # Start thread
            self.download_thread.start()
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.log(f"Error starting download: {e}")
    
    def stop_download(self):
        """Stop current download"""
        if self.download_worker:
            self.download_worker.stop_download()
            self.log("Stopping download...")
    
    def download_finished(self, success: bool, message: str):
        """Handle download completion"""
        self.log(message)
        
        # Clean up thread
        if self.download_thread:
            self.download_thread.quit()
            self.download_thread.wait()
            self.download_thread = None
        self.download_worker = None
        
        # UI state
        self.is_downloading = False
        self.download_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if success:
            self.statusBar().showMessage("Download completed!")
        else:
            self.statusBar().showMessage("Download failed!")
    
    def get_video_info(self):
        """Get video information"""
        try:
            options = self.get_ui_options()
            cmd = self.command_builder.build_info_command(options)
            self.log("Getting video information...")
            self.statusBar().showMessage("Getting video info...")
            
            # Setup worker and thread
            self.info_worker = InfoWorker()
            self.info_thread = QThread()
            
            self.info_worker.moveToThread(self.info_thread)
            
            # Connect signals
            self.info_worker.info_received.connect(self.show_video_info)
            self.info_worker.error_occurred.connect(self.info_error)
            
            # Start info retrieval when thread starts
            self.info_thread.started.connect(lambda: self.info_worker.get_info(cmd))
            
            # Start thread
            self.info_thread.start()
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            self.log(f"Error getting video info: {e}")
    
    def show_video_info(self, info: Dict[str, Any]):
        """Show video information dialog"""
        self.log("Video information retrieved successfully")
        self.statusBar().showMessage("Ready")
        
        # Clean up thread
        if self.info_thread:
            self.info_thread.quit()
            self.info_thread.wait()
            self.info_thread = None
        self.info_worker = None
        
        # Show info dialog
        dialog = VideoInfoDialog(info, self)
        dialog.show()
    
    def info_error(self, error: str):
        """Handle info retrieval error"""
        self.log(f"Error getting video info: {error}")
        self.statusBar().showMessage("Ready")
        
        # Clean up thread
        if self.info_thread:
            self.info_thread.quit()
            self.info_thread.wait()
            self.info_thread = None
        self.info_worker = None
    
    def closeEvent(self, event):
        """Handle application closing"""
        if self.is_downloading:
            reply = QMessageBox.question(self, "Quit Application",
                                       "Download in progress. Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                if self.download_worker:
                    self.download_worker.stop_download()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()