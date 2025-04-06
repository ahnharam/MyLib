import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import hashlib

# 파일 내용을 해시로 변환하는 함수
def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

# SmartBotReloader 클래스 정의
class SmartBotReloader(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.file_hashes = self.calculate_initial_hashes()
        self.process = subprocess.Popen(['python', self.script])

    # 최초 실행 시 모든 .py 파일의 해시 저장
    def calculate_initial_hashes(self):
        hashes = {}
        for root, _, files in os.walk("."):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.abspath(os.path.join(root, file))
                    hashes[path] = hash_file(path)
        return hashes

    # 파일이 수정될 때마다 호출
    def on_modified(self, event):
        if not event.src_path.endswith(".py"):
            return

        abs_path = os.path.abspath(event.src_path)
        old_hash = self.file_hashes.get(abs_path)
        new_hash = hash_file(abs_path)

        if old_hash != new_hash:
            print(f"🔄 내용 변경 감지: {event.src_path} → 봇 재시작")
            self.process.kill()
            self.process = subprocess.Popen(['python', self.script])
            self.file_hashes[abs_path] = new_hash


if __name__ == "__main__":
    path = "."
    event_handler = SmartBotReloader("bot.py")
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print("👀 스마트 변경 감지 중 (내용 변경 시에만 재시작)...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.process.kill()
    observer.join()
