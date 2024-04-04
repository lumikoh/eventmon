INSERT INTO calendar_status (e_id, in_calendar, country_code) 
    VALUES (%s, %s, %s) 
    ON CONFLICT DO NOTHING;