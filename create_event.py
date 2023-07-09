import json
import smtplib
from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def create_event(summary, description, start, end):
    service = get_calendar_service()

    # d = datetime.now().date()
    # tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    start = start.isoformat()
    end = end.isoformat()
    # end = (tomorrow + timedelta(hours=1)).isoformat()

    config = json.load(open('config.json'))

    c_id = config["calendar_id"]
    email = config["email"]
    password = config["password"]
    date_string = str(start).replace("T", " ")[:-3]

    event_result = service.events().insert(calendarId=c_id,
        body={
            "summary": summary,
            "description": description,
            "start": {"dateTime": start, "timeZone": 'Europe/Helsinki'},
            "end": {"dateTime": end, "timeZone": 'Europe/Helsinki'},
        }
    ).execute()

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg=f"Subject:Event created: {date_string} {summary}\n\n{summary}\n{date_string}\n{description}".replace("\u00e9", "e").replace("ä", "a").replace("ö", "o").replace("Ö", "O").replace("Ä", "A").encode().decode('ascii', errors='ignore')
        )

    #print("created event")
    #print("id: ", event_result['id'])
    #print("summary: ", event_result['summary'])
    #print("starts at: ", event_result['start']['dateTime'])
    #print("ends at: ", event_result['end']['dateTime'])