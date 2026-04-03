import os
import requests
import hashlib
import threading
from pathlib import Path

class ISODownloader:
    def __init__(self, download_dir=None):
        if download_dir is None:
            # Default to Downloads folder
            self.download_dir = os.path.join(Path.home(), "Downloads")
        else:
            self.download_dir = download_dir
            
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download(self, url, filename, progress_callback=None):
        file_path = os.path.join(self.download_dir, filename)
        
        def run_download():
            try:
                response = requests.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                
                downloaded = 0
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback:
                                progress_callback(downloaded, total_size)
                
                if progress_callback:
                    progress_callback(total_size, total_size, finished=True, path=file_path)
            except Exception as e:
                if progress_callback:
                    progress_callback(0, 0, error=str(e))

        thread = threading.Thread(target=run_download)
        thread.start()
        return thread

    @staticmethod
    def verify_checksum(file_path, expected_hash, algorithm="sha256"):
        if not os.path.exists(file_path):
            return False
            
        hash_func = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest().lower() == expected_hash.lower()
