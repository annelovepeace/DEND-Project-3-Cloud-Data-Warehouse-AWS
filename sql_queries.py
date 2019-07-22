import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events (
                                se_eventid  INT  IDENTITY(0,1) PRIMARY KEY,
                                se_artist  VARCHAR(255),
                                se_auth  VARCHAR(255),
                                se_firstname VARCHAR(255),
                                se_gender  VARCHAR(1),
                                se_iteminsession  INT,
                                se_lastname  VARCHAR(255),
                                se_length  NUMERIC,
                                se_level  VARCHAR(255),
                                se_location  VARCHAR(255),
                                se_method  VARCHAR(255),
                                se_page  VARCHAR(255),
                                se_registration  VARCHAR(255),
                                se_sessionid  INT,
                                se_song  VARCHAR(255),
                                se_status  INT,
                                se_ts BIGINT,
                                se_useragent VARCHAR(255),
                                se_userid  INT
                                );
                            """)

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
                                song_id  VARCHAR(255) PRIMARY KEY,
                                num_songs  INT,
                                title  VARCHAR(255),
                                artist_name  VARCHAR(255),
                                artist_latitude  NUMERIC,
                                year  INT,
                                duration  NUMERIC,
                                artist_id  VARCHAR(255),
                                artist_longitude  NUMERIC,
                                artist_location  VARCHAR(255)
                                );
                            """)

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay (
                            sp_songplayid  INT  IDENTITY(0,1) PRIMARY KEY,
                            sp_starttime  TIMESTAMP NOT NULL,
                            sp_userid  INT NOT NULL,
                            sp_level  VARCHAR(255),
                            sp_songid  VARCHAR(255) NOT NULL,
                            sp_artistid  VARCHAR(255) NOT NULL,
                            sp_sessionid  INT,
                            sp_location  VARCHAR(255),
                            sp_useragent VARCHAR(255)
                            );
                        """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                        u_userid  int  PRIMARY KEY,
                        u_firstname  VARCHAR(255),
                        u_lastname  VARCHAR(255),
                        u_gender  VARCHAR(255),
                        u_level  VARCHAR(255)
                        );
                    """)

song_table_create = ("""CREATE TABLE IF NOT EXISTS song (
                        s_songid  VARCHAR(255)  PRIMARY KEY,
                        s_title  VARCHAR(255),
                        s_artistid  VARCHAR(255) NOT NULL,
                        s_year  INT,
                        s_duration  NUMERIC
                        );
                    """)

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist (
                            a_artistid  VARCHAR(255)  PRIMARY KEY,
                            a_name  VARCHAR(255),
                            a_location  VARCHAR(255),
                            a_latitude  NUMERIC,
                            a_longitude  NUMERIC
                            );
                        """)

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                        t_starttime  TIMESTAMP  PRIMARY KEY,
                        t_hour  INT,
                        t_day  INT,
                        t_week  INT,
                        t_month  INT,
                        t_year  INT,
                        t_weekday  INT
                        );
                    """)

# STAGING TABLES

staging_events_copy = ("""
                        copy staging_events from '{}'
                        credentials 'aws_iam_role={}'
                        region 'us-west-2'
                        compupdate off
                        JSON '{}'
                        """).format(config.get('S3', 'LOG_DATA'),
                                    config.get('IAM_ROLE', 'ARN'),
                                    config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""
                    copy staging_songs from '{}'
                    credentials 'aws_iam_role={}'
                    region 'us-west-2'
                    compupdate off
                    JSON 'auto'
                    """).format(config.get('S3', 'SONG_DATA'),
                                config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplay (sp_starttime, sp_userid,
                                                sp_level, sp_songid,
                                                sp_artistid, sp_sessionid,
                                                sp_location, sp_useragent)
                            SELECT DISTINCT
                                timestamp 'epoch' + se_ts/1000 *
                                    interval '1 second' AS sp_starttime,
                                se_userid,
                                se_level,
                                song_id,
                                artist_id,
                                se_sessionid,
                                se_location,
                                se_useragent
                            FROM staging_events se, staging_songs ss
                            WHERE se.se_page='NextSong'
                                and se.se_song=ss.title
                        """)

user_table_insert = ("""INSERT INTO users (u_userid, u_firstname, u_lastname, u_gender, u_level)
                        SELECT DISTINCT
                            se_userid,
                            se_firstname,
                            se_lastname,
                            se_gender,
                            se_level
                        FROM staging_events
                        WHERE se_page='NextSong'
                    """)

song_table_insert = ("""INSERT INTO song (s_songid, s_title, s_artistid, s_year, s_duration)
                        SELECT DISTINCT
                            song_id,
                            title,
                            artist_id,
                            year,
                            duration
                        FROM staging_songs
                    """)

artist_table_insert = ("""INSERT INTO artist (a_artistid, a_name, a_location, a_latitude, a_longitude)
                            SELECT DISTINCT
                                artist_id,
                                artist_name,
                                artist_location,
                                artist_latitude,
                                artist_longitude
                            FROM staging_songs
                        """)

time_table_insert = ("""INSERT INTO time (t_starttime, t_hour, t_day, t_week,
                                            t_month, t_year, t_weekday)
                        SELECT DISTINCT
                            t_starttime,
                            EXTRACT(h from t_starttime) AS t_hour,
                            EXTRACT(d from t_starttime) AS t_day,
                            EXTRACT(w from t_starttime) AS t_week,
                            EXTRACT(mon from t_starttime) AS t_month,
                            EXTRACT(y from t_starttime) AS t_year,
                            EXTRACT(dw from t_starttime) AS t_weekday
                        FROM (SELECT distinct timestamp 'epoch' +
                                    se_ts/1000 * interval '1 second'
                                    AS t_starttime
                                FROM staging_events)
                    """)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]