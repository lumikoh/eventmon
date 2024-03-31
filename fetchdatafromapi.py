import psycopg2
import psycopg2.extras
import configparser
import requests
import json

configFilePath = './config.ini'

def getFromLocation(url):
    response_API = requests.get(url)
    data = response_API.text
    return json.loads(data)
    

def getScriptsFromFile(path):
    file = open(path, 'r')
    commands = file.read().strip("\n").split(';')
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
        print("Connecting... ≽^•⩊•^≼\n")

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
        print(record[0], '\n')

        dsn_p = conn.get_dsn_parameters()

        print('  user:', dsn_p['user'])
        print('    db:', dsn_p['dbname'])
        print('  host:', dsn_p['host'])
        print('  port:', dsn_p['port'])
        print('')

        scripts = getScriptsFromFile('./sql/create_tables.sql')

        for s in scripts:
            cur.execute(s)

        testcreate = ''' CREATE TABLE IF NOT EXISTS poksutesti (
                            id      int PRIMARY KEY,
                            name    varchar(40) NOT NULL,
                            salary  int,
                            dept_id varchar(30))'''
        
        cur.execute(testcreate)

        data = getFromLocation(config.get('url','test'))

        insert_script = 'INSERT INTO address (a_id, name, full_address, country_code, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'
        
        for d in data["activities"]:
            cur.execute(insert_script, (d["address"]["guid"], 
                                        d["address"]["name"],
                                        d["address"]["full_address"],
                                        d["address"]["country_code"],
                                        d["address"]["latitude"],
                                        d["address"]["longitude"],))

        conn.commit()

    except Exception as error:
        print(error)
    
    finally:
        if conn != None:
            conn.close()
        if cur != None:
            cur.close()

if __name__ == "__main__":
    main()