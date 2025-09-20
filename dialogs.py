from typing import Dict, Any

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QTabWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class VideoInfoDialog(QWidget):
    """Dialog for displaying detailed video information"""
    
    def __init__(self, info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video Information")
        self.setGeometry(200, 200, 800, 600)
        self.info = info
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout()
        
        # Create tab widget for organized info display
        tab_widget = QTabWidget()
        
        # General info tab
        general_tab = self.create_general_tab()
        tab_widget.addTab(general_tab, "General")
        
        # Formats tab
        formats_tab = self.create_formats_tab()
        tab_widget.addTab(formats_tab, "Formats")
        
        # Raw data tab
        raw_tab = self.create_raw_tab()
        tab_widget.addTab(raw_tab, "Raw Data")
        
        layout.addWidget(tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_general_tab(self) -> QWidget:
        """Create general information tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setFont(QFont("Segoe UI", 10))
        
        # Format basic information
        info_str = self.format_general_info()
        info_text.setPlainText(info_str)
        
        layout.addWidget(info_text)
        widget.setLayout(layout)
        
        return widget
    
    def create_formats_tab(self) -> QWidget:
        """Create formats information tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        if 'formats' in self.info:
            tree = QTreeWidget()
            tree.setHeaderLabels(['Format ID', 'Extension', 'Resolution', 'FPS', 'Codec', 'Size', 'Note'])
            
            for fmt in self.info['formats']:
                item = QTreeWidgetItem([
                    fmt.get('format_id', 'N/A'),
                    fmt.get('ext', 'N/A'), 
                    fmt.get('resolution', 'N/A'),
                    str(fmt.get('fps', 'N/A')),
                    fmt.get('vcodec', 'N/A') if fmt.get('vcodec') != 'none' else fmt.get('acodec', 'N/A'),
                    self.format_filesize(fmt.get('filesize')),
                    fmt.get('format_note', 'N/A')
                ])
                tree.addTopLevelItem(item)
            
            # Auto-resize columns
            for i in range(tree.columnCount()):
                tree.resizeColumnToContents(i)
            
            layout.addWidget(tree)
        else:
            info_text = QTextEdit()
            info_text.setReadOnly(True)
            info_text.setPlainText("No format information available")
            layout.addWidget(info_text)
        
        widget.setLayout(layout)
        return widget
    
    def create_raw_tab(self) -> QWidget:
        """Create raw data tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        raw_text = QTextEdit()
        raw_text.setReadOnly(True)
        raw_text.setFont(QFont("Consolas", 9))
        
        # Pretty print the raw JSON data
        import json
        try:
            raw_str = json.dumps(self.info, indent=2, ensure_ascii=False)
            raw_text.setPlainText(raw_str)
        except Exception as e:
            raw_text.setPlainText(f"Error formatting raw data: {e}")
        
        layout.addWidget(raw_text)
        widget.setLayout(layout)
        
        return widget
    
    def format_general_info(self) -> str:
        """Format general video information"""
        info_lines = []
        
        # Basic info
        info_lines.append("=== BASIC INFORMATION ===")
        info_lines.append(f"Title: {self.info.get('title', 'N/A')}")
        info_lines.append(f"Uploader: {self.info.get('uploader', 'N/A')}")
        info_lines.append(f"Channel: {self.info.get('channel', 'N/A')}")
        info_lines.append(f"Upload Date: {self.format_date(self.info.get('upload_date'))}")
        info_lines.append(f"Duration: {self.format_duration(self.info.get('duration'))}")
        info_lines.append(f"View Count: {self.format_number(self.info.get('view_count'))}")
        info_lines.append(f"Like Count: {self.format_number(self.info.get('like_count'))}")
        info_lines.append("")
        
        # Technical info
        info_lines.append("=== TECHNICAL INFORMATION ===")
        info_lines.append(f"Video ID: {self.info.get('id', 'N/A')}")
        info_lines.append(f"Webpage URL: {self.info.get('webpage_url', 'N/A')}")
        info_lines.append(f"Extractor: {self.info.get('extractor', 'N/A')}")
        info_lines.append(f"File Size (approx): {self.format_filesize(self.info.get('filesize_approx'))}")
        info_lines.append("")
        
        # Quality info
        info_lines.append("=== QUALITY INFORMATION ===")
        info_lines.append(f"Width: {self.info.get('width', 'N/A')}")
        info_lines.append(f"Height: {self.info.get('height', 'N/A')}")
        info_lines.append(f"FPS: {self.info.get('fps', 'N/A')}")
        info_lines.append(f"Video Codec: {self.info.get('vcodec', 'N/A')}")
        info_lines.append(f"Audio Codec: {self.info.get('acodec', 'N/A')}")
        info_lines.append(f"Format: {self.info.get('format', 'N/A')}")
        info_lines.append("")
        
        # Description
        description = self.info.get('description', '')
        if description:
            info_lines.append("=== DESCRIPTION ===")
            # Limit description length for readability
            if len(description) > 1000:
                description = description[:1000] + "..."
            info_lines.append(description)
        
        return '\n'.join(info_lines)
    
    def format_duration(self, duration) -> str:
        """Format duration in seconds to HH:MM:SS"""
        if not duration:
            return "N/A"
        
        try:
            duration = int(duration)
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes:02d}:{seconds:02d}"
        except:
            return str(duration)
    
    def format_filesize(self, size) -> str:
        """Format file size in bytes to human readable format"""
        if not size:
            return "N/A"
        
        try:
            size = int(size)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except:
            return str(size)
    
    def format_number(self, number) -> str:
        """Format large numbers with commas"""
        if not number:
            return "N/A"
        
        try:
            return f"{int(number):,}"
        except:
            return str(number)
    
    def format_date(self, date_str) -> str:
        """Format date string to readable format"""
        if not date_str:
            return "N/A"
        
        try:
            # Assuming format is YYYYMMDD
            if len(date_str) == 8:
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                return f"{year}-{month}-{day}"
            return date_str
        except:
            return str(date_str)


class AboutDialog(QWidget):
    """About dialog for the application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About yt-dlp GUI")
        self.setGeometry(300, 300, 400, 300)
        self.setWindowFlags(Qt.Dialog)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the about dialog UI"""
        layout = QVBoxLayout()
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
        <h2>yt-dlp GUI</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Description:</b> A modern Qt-based GUI wrapper for yt-dlp</p>
        
        <h3>Features:</h3>
        <ul>
            <li>Easy video downloads from hundreds of sites</li>
            <li>Audio-only extraction</li>
            <li>Subtitle downloads</li>
            <li>SponsorBlock integration</li>
            <li>Custom format selection</li>
            <li>Batch playlist downloads</li>
        </ul>
        
        <h3>Built with:</h3>
        <ul>
            <li>Python 3</li>
            <li>PySide6 (Qt for Python)</li>
            <li>yt-dlp</li>
        </ul>
        
        <p><b>License:</b> MIT</p>
        """)
        
        layout.addWidget(about_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)