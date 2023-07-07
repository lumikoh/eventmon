from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def create_event(summary, description, start, end):
    service = get_calendar_service()

    # d = datetime.now().date()
    # tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
    start = start.isoformat()
    end = end.isoformat()
    # end = (tomorrow + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='25f27666ccf3e36f503d346826b32c4ce2a7d06c675732b98b83198989911c22@group.calendar.google.com',
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