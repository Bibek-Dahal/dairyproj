import datetime
from dairyapp.models import MilkRecord
import pytz

def getShift():
    desired_timezone = pytz.timezone('Asia/Kathmandu')
    current_time = datetime.datetime.now(desired_timezone)
    print(current_time)


    # Extract the hour component from the current time
    current_hour = current_time.hour

    print("current_hour======",current_hour)

    # Determine whether it's AM or PM
    if current_hour < 12:

        return MilkRecord.shift_choices[0][1]
    else:
         return MilkRecord.shift_choices[1][1]
    