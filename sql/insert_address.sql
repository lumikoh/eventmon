INSERT INTO address (a_id, name, full_address, location_link,
                    country_code, country_code_3, latitude, 
                    longitude, state, city, country, postal_code) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT DO NOTHING;