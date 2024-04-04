import psycopg2
import psycopg2.extras
import configparser
from termcolor import colored

from src.util import getScriptsFromFile

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

        get_by_country = getScriptsFromFile('./query/get_by_country.sql')[0]

        cur.execute(get_by_country, "FI")

    except Exception as error:
        print(error)
    
    finally:
        if conn != None:
            conn.close()
        if cur != None:
            cur.close()

if __name__ == '__main__':
    main()