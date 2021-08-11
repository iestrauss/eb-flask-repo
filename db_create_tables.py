import sqlite3
from sqlite3 import Error

# Python code to create database and tables for apehouse.db
# Program will not overwrite or modify existing tables
# To startover delete database, modify definitions, run the script
# See db_insert_data for seeding tables
# use prompt> sqlite3 /usr/local/var/apehouse.db
#     sqlite3> .help
#     sqlite3> .tables
#     sqlite3> select * from permission;

# Version:
#     0.0.1 Initial table setup

create_table_commands = []

permission_table = """CREATE TABLE IF NOT EXISTS permission (
    id INTEGER PRIMARY KEY,
    permission TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);"""

create_table_commands.append(permission_table)

user_table = """CREATE TABLE IF NOT EXISTS user (
    id integer PRIMARY KEY,
    name text NOT NULL,
    permission_id INTEGER NOT NULL, 
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (permission_id) REFERENCES permission(id)
);"""

create_table_commands.append(user_table)

article_table = """CREATE TABLE IF NOT EXISTS article (
    id          INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    url         TEXT NOT NULL,
    image_url   TEXT NOT NULL,
    snippet     TEXT NOT NULL,
    date_upload TEXT DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT article_unq UNIQUE (url)
);"""

create_table_commands.append(article_table)

# select id, title, url, datetime(created_at, 'localtime') as created_at from article

vote_choice_table = """CREATE TABLE IF NOT EXISTS vote_choice (
    id INTEGER PRIMARY KEY,
    choice TEXT NOT NULL,
    color  TEXT NOT NULL,
    status INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);"""

create_table_commands.append(vote_choice_table)

article_vote_table = """CREATE TABLE IF NOT EXISTS article_vote (
    id integer  PRIMARY KEY,
    user_id     INTEGER NOT NULL, 
    article_id  INTEGER NOT NULL, 
    vote_choice_id INTEGER NOT NULL,
    comment     TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id)    REFERENCES user(id),
        FOREIGN KEY (article_id) REFERENCES article(id),
        FOREIGN KEY (vote_choice_id) REFERENCES vote_choices(id),
        CONSTRAINT article_vote_unq UNIQUE (user_id, article_id)
);"""

create_table_commands.append(article_vote_table)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"/usr/local/var/apehouse.db"
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        for command in create_table_commands:
            print(command)
            create_table(conn, command)
        print("Closing connection to " + database)
        conn.close()

    else:
        print("Error! cannot create the database connection.")
 
 
if __name__ == '__main__':
    main()


