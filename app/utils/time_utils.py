import time


def calculate_uptime(start_time):
    current_time = time.time()

    uptime_seconds = round(current_time - start_time, 2)

    return uptime_seconds
