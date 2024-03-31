import psycopg2
import psycopg2.extras
import configparser
import requests
import json
from termcolor import colored

configFilePath = './config.ini'

def getFromLocation(url):
    response_API = requests.get(url)
    data = response_API.text
    return json.loads(data)
    

def getScriptsFromFile(path):
    file = open(path, 'r')
    commands = file.read().strip('\n').split(';')
    file.close()
    del commands[-1]
    return commands

def main():
    config = configparser.RawConfigParser()
    config.read_file(open(configFilePath))

    username = config.get('db', 'username')
    password = config.get('db', 'password')
    hostname = config.get('db', 'hostname')
    database = config.get('db', 'database')
    port     = config.get('db', 'port'    )

    conn = None
    cur  = None

    try:
        print(colored('Connecting... ≽^•⩊•^≼\n', 'light_magenta'))

        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = password,
            port = port
        )

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute('SELECT version();')
        record = cur.fetchone()
        print(colored(record[0], 'yellow'), '\n')

        dsn_p = conn.get_dsn_parameters()

        print(colored('  user:', 'light_blue'), dsn_p['user'])
        print(colored('    db:', 'light_blue'), dsn_p['dbname'])
        print(colored('  host:', 'light_blue'), dsn_p['host'])
        print(colored('  port:', 'light_blue'), dsn_p['port'])
        print('')

        scripts = getScriptsFromFile('./sql/create_tables.sql')

        for s in scripts:
            cur.execute(s)

        print(colored('Fetching data...\n', 'light_magenta'))

        data = getFromLocation(config.get('url','test'))

        insert_address = getScriptsFromFile('./sql/insert_address.sql')[0]
        insert_event   = getScriptsFromFile('./sql/insert_event.sql')[0]

        for d in data['activities']:
            cur.execute(insert_address, (d['address'].get('guid'), 
                                         d['address'].get('name'),
                                         d['address'].get('full_address'),
                                         d['address'].get('location_map_link'),
                                         d['address'].get('country_code'),
                                         d['address'].get('country_code_alpha_3'),
                                         d['address'].get('latitude'),
                                         d['address'].get('longitude'),
                                         d['address'].get('state'),
                                         d['address'].get('city'),
                                         d['address'].get('country'),
                                         d['address'].get('postal_code')))
            
            cur.execute(insert_event, (d.get('guid'),
                                       d['address'].get('guid'),
                                       d['contact_information'].get('contact_phone'),
                                       d['contact_information'].get('contact_email'),
                                       d['contact_information'].get('contact_website'),
                                       d['metadata'].get('update_key'),
                                       d.get('name'),
                                       d.get('payment_options'),
                                       d.get('start_datetime'),
                                       d.get('activity_type'),
                                       d.get('large_event_guid'),
                                       d.get('has_registration_options'),
                                       d.get('has_registration_skus'),
                                       d.get('league_guid'),
                                       d.get('activity_format'),
                                       d.get('status'),
                                       d.get('tags'),
                                       False,
                                       d.get('pokemon_url')

            ))

        conn.commit()

    except Exception as error:
        print(error)
    
    finally:
        if conn != None:
            conn.close()
        if cur != None:
            cur.close()

if __name__ == '__main__':
    main()