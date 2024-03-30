import psycopg2
import psycopg2.extras
import configparser
from bs4 import BeautifulSoup

configFilePath = './config.ini'

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

        testcreate = ''' CREATE TABLE IF NOT EXISTS poksutesti (
                            id      int PRIMARY KEY,
                            name    varchar(40) NOT NULL,
                            salary  int,
                            dept_id varchar(30))'''
        
        cur.execute(testcreate)

        insert_script = 'INSERT INTO poksutesti (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'

        insert_value = (2, 'abd', 12000, 'D1')

        cur.execute(insert_script, insert_value)

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