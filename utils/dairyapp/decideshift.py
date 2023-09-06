import datetime
from dairyapp.models import MilkRecord
def getShift():
    # Get the current time
    current_time = datetime.datetime.now().time()

    # Define the morning and night time ranges
    morning_start = datetime.time(0, 0)  # Midnight
    morning_end = datetime.time(11, 59, 59)  # 11:59:59 AM

    night_start = datetime.time(12, 0)  # Noon
    night_end = datetime.time(23, 59, 59)  # 11:59:59 PM

    # Check if it's morning or night
    if morning_start <= current_time <= morning_end:
        # print("It's morning.========")
        # print(MilkRecord.shift_choices[0][1])
        return MilkRecord.shift_choices[0][1]
    elif night_start <= current_time <= night_end:
        return MilkRecord.shift_choices[1][1]
    else:
        return MilkRecord.shift_choices[0][1]