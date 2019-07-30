# Project Summary

### Background
This project is to help a startup called <strong>Sparkify</strong> to understand what songs users are listening to. Sparkify has been collecting on songs and user activity on their new music streaming app. 
As their use base and song database grow, they decide to move their processes and data onto cloud with two Amazon Web Services <strong>S3</strong> (simple storage service) and <strong>Redshift</strong> (Internet hosting service and data warehouse product). 


### Datasets
Two datasets that reside in S3:

<ol>
    <li><strong>Song Dataset</strong></li>
    > Each file is in JSON format and contains metadata about a song and the artist of that song. <br>
    > File names are like 'song_data/A/B/C/TRABCEI128F424C983.json' etc. <br>
    > In each file, data are like: {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
    <li><strong>Log Dataset</strong></li>
    > Each file is in JSON format and contains logs on user activity on the app <br>
    > File names are like 'log_data/2018/11/2018-11-12-events.json' etc. <br>
    > below is an example of what the data in a log file, 2018-11-12-events.json, looks like.
</ol>

![](https://r766469c826419xjupyterlr5tapor7.udacity-student-workspaces.com/files/img/log-data-examples.png)
    

### Tasks
<ol>
    <li><strong>Redshift cluster setup<strong></li>
    > launch a readshift database dc2.large cluster with 4 nodes<br>
    > create an IAM role that has read access to S3<br>
        <li><strong>Designing tables in <em>sql_queries.py</em></strong></li>
    > design fact and dimension tables for a star schema<br>
         fact table: songplays<br>
         dimension tables: users, songs, artists, time<br>
    > design staging tables: staging_events, staging_songs<br>
    > write a CREATE statement for each of these tables<br>
    > write a DROP statements to drop tables if the tables already exist<br>
    <li><strong>Creating tables in <em>create_tables.py</em></li>
    > connect to the database<br>
    > create fact, dimension, staging tabels
    <li><strong>Buidling ETL pipeline in <em>etl.py</em></strong></li>
    > implement the logic to load data from S3 to staging tables on Redshift<br>
    > implement the logic to load data from staging tables to analytics tables on Redshift<br>
    <li><strong>Cluster cleanup</strong></li>
    > remember to delete the Redshift cluster when finish
        
</ol>

---
# To run the Python scripts
<ol>
    <li>Get <em>[Cluster]</em> and <em>[IAM_ROLE]</em> from Redshift to fill dwh.cfg file
    <li>Click <em>File -> New -> Console</em> at top menu bar</li>
    <li>Select kernel <em>Python3</em></li>
    <li>Type <code>'%run create_tables.py'<\code> in the console cell</li>
    <li>Click <em>Run -> Run selected cell</em> at top menu bar</li>
    <li>Type <code>'%run etl.py'<\code> in the console cell</li>
    <li>Click <em>Run -> Run selected cell</em> at top menu bar</li>
</ol>

        
---
# Files in the repository
The project workspace includes five files:
<ul>
    <li><strong><em>create_tables.py</em></strong> creates the fact and dimension tables for the star schema in Redshift.</li>
    <li><strong><em>etl.py</em></strong> loads data from S3 into staging tables on Redshift and then process that data into the fact and dimension tables on Redshift.</li>
    <li><strong><em>sql_queries.py</em></strong> contains all sql queries, which are imported into the last two files above.</li>
    <li><strong><em>dwh.cfg</em></strong> stores cluster, IAM role, S3 file path information, which are imported into the last three files above.</li>
    <li><strong><em>README.md</em></strong> this file provides discussion on the project.</li>
</ul>
        

---
# Results

<strong>Analysis on songplay table</strong><br>
<ul>
    <li><strong>The most popular song</strong> is 'You're The One'<br>
        query:<br>
        
![](https://r766469c826419xjupyterlr5tapor7.udacity-student-workspaces.com/files/img/query1_song_code.png)        
        result:<br>
![](https://r766469c826419xjupyterlr5tapor7.udacity-student-workspaces.com/files/img/query1_song_result.png)
        <br>
        <br>
        
 <li><strong>The most popular artist</strong> is 'Dwight Yoakam'<br>
        query:<br>
        
![](https://r766469c826419xjupyterlr5tapor7.udacity-student-workspaces.com/files/img/query2_artist_code.png)        
        result:<br>
![](https://r766469c826419xjupyterlr5tapor7.udacity-student-workspaces.com/files/img/query2_artist_result.png)