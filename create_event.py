import json
from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def create_event(summary, description, start, end):
    service = get_calendar_service()

    # d = datetime.now().date()
    # tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    start = start.isoformat()
    end = end.isoformat()
    # end = (tomorrow + timedelta(hours=1)).isoformat()

    c_id = json.load(open('config.json'))["calendar_id"]

    event_result = service.events().insert(calendarId=c_id,
        body={
            "summary": summary,
            "description": description,
            "start": {"dateTime": start, "timeZone": 'Europe/Helsinki'},
            "end": {"dateTime": end, "timeZone": 'Europe/Helsinki'},
        }
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])