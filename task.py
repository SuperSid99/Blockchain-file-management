import watchdog.events
import watchdog.observers
import time
from blockchain_main import execute_process


class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        # Set the patterns for PatternMatchingEventHandler
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg', '*.jpeg', '*.txt'],
                                                             ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        # print("Watchdog received created event - % s." % event.src_path)
        sttime=time.time()
        print(f"image added to folder at {sttime}\n")
        execute_process(event.src_path)
        endtime=time.time()
        print(f"excitution ended at {endtime}\n")
        print(f"total time taken = {endtime-sttime}\n")

    # Event is created, you can process it now

    def on_modified(self, event):
        print(f"Watchdog received modified event - {event.src_path}.")
        # execute_process(event.src_path)

    # Event is modified, you can process it now


if __name__ == "__main__":
    # add the source path to your folder
    src_path = r'path to/Blockchain_file_management'
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=src_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
