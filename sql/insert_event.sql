INSERT INTO event (e_id, a_id, phone, email, website, update_key, name,
                   payment_options, start_time, activity_type, large_event_id,
                   reg_options, reg_skus, l_id, format, status, tags, in_calendar,
                   pokemon_url) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT(e_id) 
    DO UPDATE SET
        phone = EXCLUDED.phone,
        email = EXCLUDED.email,
        website = EXCLUDED.website,
        start_time = EXCLUDED.start_time,
        format = EXCLUDED.format;