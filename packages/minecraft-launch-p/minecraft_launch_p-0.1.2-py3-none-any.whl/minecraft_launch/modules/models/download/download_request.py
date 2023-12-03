class DownloadRequest():
    def __init__(self, dir: str, url: str, file_name: str, file_size: int) -> None:
        self.dir: str = dir
        self.url: str = url
        self.file_name: str = file_name
        self.file_size: int = file_size

