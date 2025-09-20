import subprocess
import json
from typing import List

from PySide6.QtCore import QObject, Signal


class DownloadWorker(QObject):
    """Worker class for handling yt-dlp downloads in a separate thread"""
    
    output_received = Signal(str)
    progress_updated = Signal(int)
    download_finished = Signal(bool, str)  # success, message
    
    def __init__(self):
        super().__init__()
        self.process = None
        self.should_stop = False
    
    def start_download(self, command: List[str]):
        """Start the download process"""
        try:
            self.should_stop = False
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output line by line
            while True:
                if self.should_stop:
                    self.process.terminate()
                    break
                
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                
                if output:
                    self.output_received.emit(output.strip())
                    
                    # Try to parse progress
                    if '[download]' in output and '%' in output:
                        try:
                            # Extract percentage from output like "[download] 45.2% of 123MB"
                            import re
                            match = re.search(r'(\d+\.?\d*)%', output)
                            if match:
                                progress = int(float(match.group(1)))
                                self.progress_updated.emit(progress)
                        except:
                            pass
            
            # Get return code
            return_code = self.process.poll()
            success = return_code == 0 and not self.should_stop
            
            if self.should_stop:
                self.download_finished.emit(False, "Download cancelled by user")
            elif success:
                self.download_finished.emit(True, "Download completed successfully!")
            else:
                self.download_finished.emit(False, f"Download failed with exit code: {return_code}")
                
        except Exception as e:
            self.download_finished.emit(False, f"Error during download: {str(e)}")
        finally:
            self.process = None
    
    def stop_download(self):
        """Stop the current download"""
        self.should_stop = True
        if self.process:
            try:
                self.process.terminate()
            except:
                pass


class InfoWorker(QObject):
    """Worker class for getting video information"""
    
    info_received = Signal(dict)
    error_occurred = Signal(str)
    
    def get_info(self, command: List[str]):
        """Get video information"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                try:
                    info = json.loads(result.stdout)
                    self.info_received.emit(info)
                except json.JSONDecodeError as e:
                    self.error_occurred.emit(f"Error parsing video information: {str(e)}")
            else:
                self.error_occurred.emit(f"Error getting video info: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.error_occurred.emit("Timeout while getting video information")
        except Exception as e:
            self.error_occurred.emit(f"Error getting video info: {str(e)}")