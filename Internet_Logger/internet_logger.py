import subprocess
import time
from datetime import datetime
import pytz
import os

class InternetLogger:
    def __init__(self, timezone='US/Pacific', check_interval=20):
        self.timezone = timezone
        self.check_interval = check_interval
        self.log_file_path = "log.txt"
        self.ensure_log_file_exists()
        self.disconnect_start_time = None

    def ensure_log_file_exists(self):
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w") as log_file:
                log_file.write("Internet Logger Log\n")

    def get_current_timestamp(self):
        tz = pytz.timezone(self.timezone)
        return datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    def check_wifi_connection(self):
        try:
            # Ping Google's DNS server
            output = subprocess.check_output(["ping", "-n", "1", "8.8.8.8"])
            output_str = output.decode('utf-8')
            if "Destination host unreachable" in output_str:
                print(output_str)
                print("Destination host unreachable")
                return False
            return True
        except subprocess.CalledProcessError:
            print("Ping Failed")
            return False

    def log_internet_status(self):
        print("Internet Logging... (disconnects only)")
        while True:
            timestamp = self.get_current_timestamp()
            if not self.check_wifi_connection():
                if self.disconnect_start_time is None:
                    self.disconnect_start_time = datetime.now(pytz.timezone(self.timezone))
                message = "Internet Down ... " + timestamp
                print(message)
                with open(self.log_file_path, "a") as log_file:
                    log_file.write(message + "\n")
            else:
                if self.disconnect_start_time is not None:
                    disconnect_end_time = datetime.now(pytz.timezone(self.timezone))
                    duration = disconnect_end_time - self.disconnect_start_time
                    message = (f"Internet reconnected at {timestamp}. "
                               f"Disconnect duration: {duration}. "
                               f"Disconnected from {self.disconnect_start_time.strftime('%Y-%m-%d %H:%M:%S')} "
                               f"to {disconnect_end_time.strftime('%Y-%m-%d %H:%M:%S')}.")
                    print(message)
                    with open(self.log_file_path, "a") as log_file:
                        log_file.write(message + "\n")
                    self.disconnect_start_time = None
            time.sleep(self.check_interval)

if __name__ == "__main__":
    logger = InternetLogger()
    logger.log_internet_status()