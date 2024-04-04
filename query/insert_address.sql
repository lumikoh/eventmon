INSERT INTO address (a_id, name, full_address, location_link,
                    country_code, country_code_3, latitude, 
                    longitude, state, city, country, postal_code) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT (a_id) 
    DO UPDATE
    SET
        name = EXCLUDED.name,
        full_address = EXCLUDED.full_address,
        location_link = EXCLUDED.location_link,
        latitude = EXCLUDED.latitude,
        longitude = EXCLUDED.longitude,
        state = EXCLUDED.state,
        city = EXCLUDED.city,
        postal_code = EXCLUDED.postal_code;