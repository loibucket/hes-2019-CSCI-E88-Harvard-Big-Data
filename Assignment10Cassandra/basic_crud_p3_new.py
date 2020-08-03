from datetime import datetime, timedelta
from cassandra.cluster import Cluster
from cassandra import util
import pandas as pd
import numpy as np
import uuid
import random

# Initialize the connection and session with Cassandra on localhost
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('hw10')

def generate_data(num_rows):

    #generate uuid
    uuid_list = []
    for _ in range(num_rows):
        uuid_list.append(uuid.uuid4())

    df = pd.DataFrame(uuid_list)

    #generate incremental time
    time_list = [pd.Timestamp('2019-11-17T01Z')]
    for i in range(1,len(df)):
        time_list.append( time_list[-1] + pd.Timedelta(seconds=random.randint(1,50)) )
    df[1] = time_list

    #generate url
    new_url_list = ['http://example.com/?url=091','http://example.com/?url=095','http://example.com/?url=099']
    df[2] = np.random.choice(new_url_list, size=len(df))

    #generate user
    df[3] = np.random.choice(['user-028','user-039','user-052','user-065','user-099',], size=len(df))

    #generate country
    df[4] = np.random.choice(['ER','SJ','MA','GD','ZW'], size=len(df))

    #generate browser
    new_browser_list = ['Chrome','Firefox','Edge','IE']
    df[5]  = np.random.choice(new_browser_list, size=len(df))

    #generate OS
    df[6] = np.random.choice(['Mac','Linux','iPhone','Windows'], size=len(df))

    #generate Response
    df[7] = np.random.choice([501,307,510,208], size=len(df))

    #generate TTFB
    df[8] = np.random.uniform(size=len(df))
    df[8] = df[8].round(3)

    #extract hour
    df[9] = df[1].astype(str).apply(lambda x: x[:13]+':00:00Z')

    return df

def insert_cassandra(df):
    """
    Table Reference
    CREATE TABLE IF NOT EXISTS hw10.hw10_p2 (
    id UUID,
    time timestamp,
    url text,
    userId text,
    country text,
    ua_browser text,
    ua_os text,
    response_status int,
    TTFB float,
    hour timestamp,
    PRIMARY KEY ((url, country, hour), time, id)
    );
    """

    #clean the table for homework purposes
    session.execute(
    """
    TRUNCATE hw10.hw10_p2
    """
    )

    #run insertions
    for i in range(len(df)):

        #format each entry for insertion
        #proper format example
        #event_string = "8e66dea6-2a91-4ba6-9e48-c534c705574e, '2019-09-14 03:56:26Z', 'http://example.com/?url=078', 'user-079', 'SN', 'Firefox', 'Mac', 201, 0.2186, '2019-09-14 03:00:00Z'"
        event_string = str(list(df.iloc[i]))[1:-1]
        event_string = event_string.replace("'","",2)
        event_string = event_string.replace("UUID(","",)
        event_string = event_string.replace("Timestamp(","",)
        event_string = event_string.replace(", tz='UTC'","",)
        event_string = event_string.replace("+0000","Z",)
        event_string = event_string.replace(")","",)
        print("event", event_string  )
    
        session.execute(
            """
            INSERT INTO hw10.hw10_p2
            (id, time, url, userId, country, ua_browser, ua_os, response_status, TTFB, hour)
            VALUES ( %s )
            """ 
            %event_string
        )

        
        print ("inserted")

def read_cassandra():
        
        row = session.execute(
            """
            SELECT url, country, count(*), AVG(TTFB) FROM hw10.hw10_p2
            WHERE hour = '2019-11-17 01:00:00Z' and 
            country = 'GD' and 
            url = 'http://example.com/?url=095' and 
            time >= '2019-11-17 01:00:00Z' and time <= '2019-11-17 01:40:00Z'
            """ 
        )

        for items in row:
            print(items)

        row = session.execute(
            """
            SELECT url, country, count(*), AVG(TTFB) FROM hw10.hw10_p2
            WHERE hour = '2019-11-17 03:00:00Z' and 
            country = 'ZW' and 
            url = 'http://example.com/?url=099' and 
            time >= '2019-11-17 03:10:00Z' and time <= '2019-11-17 03:50:00Z'
            """ 
        )

        for items in row:
            print(items)

def main():

    df = generate_data(500)

    insert_cassandra(df)

    read_cassandra()

    print("Job Completed")

if __name__ == "__main__":
    main()
