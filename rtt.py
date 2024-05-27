#!/usr/bin/env python3

import subprocess
import time
import os
import psutil


LOG_FILE = "/tmp/rtt_output.log"
DEVICE = "NRF52833_XXAA"
INTERFACE = "SWD"
SPEED = 4000
CHANNEL = 0
TIMEOUT = 5  # Timeout in seconds to detect inactivity

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w"):
        pass
else:
    with open(LOG_FILE, "w") as f:
        f.truncate(0)

def kill_existing_jlink_rtt_logger():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == 'JLinkRTTLoggerEx':
            proc.kill()

time.sleep(1)
def start_rtt_logger():
    command = [
        "JLinkRTTLogger",
        "-Device", DEVICE,
        "-If", INTERFACE,
        "-Speed", str(SPEED),
        "-RTTChannel", str(CHANNEL),
        LOG_FILE
    ]
    with open(os.devnull, 'w') as devnull:
        return subprocess.Popen(command, stdout=devnull, stderr=devnull), time.time()

def monitor_log_file(log_file, start_time, timeout):
    last_size = 0
    while True:
        if os.path.exists(log_file):
            current_size = os.path.getsize(log_file)
            if current_size != last_size:
                with open(log_file, "r") as f:
                    f.seek(last_size)
                    new_data = f.read()
                    if new_data:
                        # Filter out unwanted lines
                        filtered_data = "\n".join(
                            line for line in new_data.splitlines()
                            if "Booting Zephyr OS build" not in line
                        ) + "\n"
                        print(filtered_data, end="")
                last_size = current_size
                start_time = time.time()
            elif time.time() - start_time > timeout:
                break
        time.sleep(1)
    return False

if __name__ == "__main__":
    while True:
        # Start RTT Logger
        rtt_process, start_time = start_rtt_logger()

        try:
            # Monitor log file for timeout
            monitor_log_file(LOG_FILE, start_time, TIMEOUT)
        except KeyboardInterrupt:
            break
        finally:
            # Terminate RTT Logger process if running
            rtt_process.terminate()
            rtt_process.wait()
