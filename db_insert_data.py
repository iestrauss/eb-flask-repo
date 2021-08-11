import sqlite3
from sqlite3 import Error

# Python code to insert some basic data into the tables for apehouse.db

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

def insert_permission(conn, permission):
    """
    Create a new permission into the permission table
    :param conn:
    :param permission:
    :return: permission id
    """
    sql = ''' INSERT INTO permission(permission)
              VALUES(?) '''
    cur = conn.cursor()
    print(permission)

    cur.execute(sql, permission)
    conn.commit()
    return cur.lastrowid
    
def insert_user(conn, user):
    """
    Create a new user into the user table
    :param conn:
    :param user:
    :return: usser id
    """
    sql = ''' INSERT INTO user(name,permission_id)
              VALUES(?,?) '''
    print(user)

    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid  

def insert_choice(conn, choice):
    """
    Create a new user into the user table
    :param conn:
    :param user:
    :return: choice id
    """
    sql = ''' INSERT INTO vote_choice(choice, color, status)
              VALUES(?,?,?) '''
    print(choice)

    cur = conn.cursor()
    cur.execute(sql, choice)
    conn.commit()
    return cur.lastrowid  

def insert_article(conn, article):
    """
    Create a new article into the user table
    :param conn:
    :param user:
    :return: choice id
    """
    sql = ''' INSERT INTO article(title, url, image_url, snippet)
              VALUES(?,?,?,?) '''
    print(article)

    cur = conn.cursor()
    cur.execute(sql, article)
    conn.commit()
    return cur.lastrowid  

def main():
    database = r"/usr/local/var/apehouse.db"
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        admin_id     = insert_permission(conn, ('admin',))
        developer_id = insert_permission(conn, ('developer',))
        level_a_id   = insert_permission(conn, ('level-a-voter',))
        level_b_id   = insert_permission(conn, ('level-b_voter',))
        level_c_id   = insert_permission(conn, ('level-c-voter',))

        insert_user(conn, ('Ilana.e.s', admin_id))
        insert_user(conn, ('Hob.m', developer_id))
        insert_user(conn, ('TestA', level_a_id))
        insert_user(conn, ('TestB', level_b_id))
        insert_user(conn, ('TestC', level_c_id))

        insert_choice(conn, ('True', 'C8FBCE', 1))
        insert_choice(conn, ('Exaggerated', 'FEF9AA', 1))
        insert_choice(conn, ('No source', 'FEBFBF', 1))
        insert_choice(conn, ('Bad source', 'FEBFBF', 1))
        insert_choice(conn, ("Can't find source", 'FEBFBF', 1))
        insert_choice(conn, ('Not news', 'C8F3FB', 1))

        insert_article(conn, ('Lottery dumping',
            'https://worldnewsdailyreport.com/lottery-winner-arrested-for-dumping-200000-of-manure-on-ex-boss-lawn/',
            'https://worldnewsdailyreport.com/wp-content/uploads/2018/05/manurevilla2.jpg',
            "A man from Illinois was arrested for getting 224,000 worth of manure dumped on "
            "his former employer's property, only "
            "two weeks after he won 125 million at the "
            "lottery and quit his job."))
        insert_article(conn, ('Trump Bans Schools',
            'https://yewnorker.com/2018/12/07/president-trump-to-ban-schools-in-order-to-stop-school-shootings/',
            'https://i0.wp.com/yewnorker.com/wp-content/uploads/2018/12/School-2.jpg?resize=300%2C169&ssl=1',
            "President Trump has rejected statements made by Senator Dianne Feinstein (D-CA) that the easy access to high-powered assault-style weapons is directly related to the rising number of school shootings and deaths in the United States."))

        print("Closing connection to " + database)
        conn.close()
    else:
        print("Error! cannot create the database connection.")
 

 
if __name__ == '__main__':
    main()


