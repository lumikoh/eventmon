import json
import smtplib
from cal_setup import get_calendar_service
import datetime


def create_event(summary, description, start, end):
    service = get_calendar_service()

    config = json.load(open('config.json'))

    c_id = config["calendar_id"]
    email = config["email"]
    password = config["password"]

    time_change = datetime.timedelta(minutes=180)
    change = start - time_change

    start = start.isoformat()
    end = end.isoformat()

    events_list = service.events().list(calendarId=c_id, 
                                        timeMin=change.isoformat()+"Z").execute()

    date_string = str(start).replace("T", " ")[:-3]

    for event in events_list["items"]:
        if(event["summary"] == summary):
            return

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

    print("-----------------------------------------------------------------")
    print("  Created event:")
    print("    id: ", event_result['id'])
    print("    summary: ", event_result['summary'])
    print("-----------------------------------------------------------------\n")