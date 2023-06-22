from datetime import datetime
import datetime as dt
import time

start_time = dt.datetime.now().time()
time.sleep(5)
end_time = dt.datetime.now().time()

delta_hour = end_time.hour - start_time.hour
delta_minute = end_time.minute - start_time.minute
delta_second = end_time.second - start_time.second
delta_us = end_time.microsecond - start_time.microsecond

# frmt = '%H:%M:%S.%s'
# delta = datetime.strptime(str(end_time), frmt) - datetime.strptime(str(start_time), frmt)

print(f"{delta_hour} hours, {delta_minute} minutes, {delta_second}.{delta_us} seconds")
