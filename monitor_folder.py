import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import django
from django.core.mail import EmailMessage

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

class Watcher:
    DIRECTORY_TO_WATCH = "C:\\Users\\Admin\\Desktop\\send_pdf"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            if event.src_path.endswith('.pdf'):
                Handler.send_email(event.src_path)

    @staticmethod
    def send_email(file_path):
        email = EmailMessage(
            'Subject here',
            'Here is the message.',
            'mubeenjutt9757@gmail.com',  # Sender
            ['naveedilyas321@gmail.com'],  # Receiver
        )
        email.attach_file(file_path)
        email.send()

if __name__ == '__main__':
    w = Watcher()
    w.run()
