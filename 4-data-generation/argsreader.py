#encoding: utf-8

def getargs():
    import argparse
    parser = argparse.ArgumentParser(description='Populate Avia database TABLE with N rows')
    parser.add_argument('table',
                        metavar='TABLE',
                        help='the name of a table to be populated')
    parser.add_argument('-a', '--append', action='store_true',
                        help='try to add N rows to already inserted rows')
    parser.add_argument('--clear', action='store_true', help='clear table')
    parser.add_argument('-n', '--number', type=int,
                        metavar='N',
                        help='the total N of rows that have to be in the table')
    parser.add_argument('--dbname', default='avia',
                        help='the database name')
    parser.add_argument('--user', default='postgres',
                        help='PostgreSQL user name to connect as')
    parser.add_argument('--password', default='',
                        help='password to be used for authentication')
    parser.add_argument('--host', default='localhost',
                        help='name of host to connect to')
    return parser.parse_args()
