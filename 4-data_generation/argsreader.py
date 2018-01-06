#encoding: utf-8

import argparse

class list_action(argparse.Action):
     def __init__(self, option_strings, dest=argparse.SUPPRESS,
                  default=argparse.SUPPRESS, help=None, nargs=None):
         if nargs is not None:
             raise ValueError("nargs not allowed")
         super(list_action, self).__init__(option_strings=option_strings,
               dest=dest, default=default, nargs=0, help=help)

     def __call__(self, parser, namespace, values, option_string=None):
         import generator
         db = generator.init_connection(namespace)
         all_tables = generator.select_all_tables(db)
         for name in sorted(all_tables):
             print name
         generator.close_connection_and_exit(0)

def getargs():
    parser = argparse.ArgumentParser(description='Populate Avia database TABLE with N rows')
    parser.add_argument('table', metavar='TABLE',
                        help='the name of a table to be modified')
    populate_group = parser.add_mutually_exclusive_group()
    populate_group.add_argument('--clear', action='store_true',
                                help='clear the specified table')
    populate_group.add_argument('-l', '--list', action=list_action,
                                help='list names of all tables')
    populate_group.add_argument('-n', '--number', type=int, metavar='N',
                                help='number of rows to be inserted in the specified table')
    db_group = parser.add_argument_group('PostgreSQL options')
    db_group.add_argument('--dbname', default='avia',
                          help='the database name (default is "avia")')
    db_group.add_argument('--user', default='postgres',
                          help='PostgreSQL user name to connect as (default is "postgres")')
    db_group.add_argument('--host', default='localhost',
                          help='name of a host to connect to (default is "localhost")')
    return parser.parse_args()
