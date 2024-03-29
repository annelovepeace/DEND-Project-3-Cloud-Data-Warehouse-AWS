import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    To read and load JSON files from S3 into staging_events and staging_songs tables.

    Parameters:
        cur: cursor.
        conn: connection.

    Returns:
        staging_events and staging_songs tables with filled data.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    To load data from staging_events and staging_songs tables into songplay, song, users, artist, time tables.

    Parameters:
        cur: cursor.
        conn: connection.

    Returns:
        songplay, song, users, artist, time tables with filled data.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()