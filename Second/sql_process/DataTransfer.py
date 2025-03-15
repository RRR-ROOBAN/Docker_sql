import requests
import mysql.connector
import os
import time


DB_HOST=os.getenv("DB_HOST","db")
DB_NAME=os.getenv("DB_NAME","isidata")
DB_USER=os.getenv("DB_USER","roobanuser")
DB_PASSWORD=os.getenv("DB_PASSWORD","rootroot")
DB_PORT=os.getenv("DB_PORT","3306") 

def fetch_data():
    re=requests.get("http://api.open-notify.org/iss-now.json")
    if re.status_code==200:
        data=re.json()
        return {"timestamp": data["timestamp"],"latitude":float(data["iss_position"]["latitude"]),
                                  "longitude":float(data["iss_position"]["longitude"])
                                  
                                  }
    return None
    


def store_data(D1):
    conn=mysql.connector.connect(host=DB_HOST,database=DB_NAME,user=DB_USER,password=DB_PASSWORD,port=DB_PORT)
    cur=conn.cursor()
    cur.execute("""
                create table if not exists location(id int auto_increment primary key,
                timestamp bigint,latitude double,longitude double 
                );""")
    cur.execute(""" 
                insert into location (timestamp,latitude,longitude) values (%s,%s,%s);
                """,(D1["timestamp"],D1["latitude"],D1["longitude"]))
    conn.commit()
    cur.close()
    conn.close()
    
    print("success")
    

if __name__ == "__main__":
    while True:
        D1=fetch_data()
        if D1:
            store_data(D1)
        time.sleep(10)
