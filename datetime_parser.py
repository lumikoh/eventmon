import datetime

MONTHS=['january','february','march','april','may','june','july','august',
        'september','october','november','december']

def string_to_datetime(datestring):
    try:
        parts = datestring.split(' ')

        month = 0
        for i in range(len(MONTHS)):
            if MONTHS[i] == parts[0].lower():
                month = i+1
                break


        year = int(parts[2])
        day = int(parts[1].strip(','))
        hour = 0
        minute = 0

        if parts[3][:2] == '12' and parts[3][-2:] == "PM":
            hour = 12
        else:
            hour = int(parts[3].split(":")[0])
            if parts[3][-2:] == "PM":
                hour += 12
        minute = int(parts[3][-4:-2])


        date = datetime.datetime(year, month, day, hour, minute)
        return date
    except:
        print("Datetime conversion error")
    return None