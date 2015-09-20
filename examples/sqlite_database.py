#!/usr/bin/env python

import time
import sys
import Adafruit_DHT
import sqlite3 as lite
from daemon import Daemon

class SqliteDatabase(Daemon):
    sensor = Adafruit_DHT.DHT11
    pin = 4
    wait_time = 30
    database = "/home/pi/database/weather.sqlite"

    def run(self):
        self.create()
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
            if humidity is not None and temperature is not None:
                self.save(temperature, humidity)
            time.sleep(self.wait_time)

    def create(self):
        self.execute("CREATE TABLE IF NOT EXISTS 'Weather' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'datetime' DATETIME DEFAULT CURRENT_TIMESTAMP, 'temperature' REAL, 'humidity' REAL)")

    def save(self, temperature, humidity):
        self.execute("INSERT INTO 'Weather' ('id','temperature','humidity') VALUES (NULL,'{0}','{1}')".format(temperature,humidity))

    def execute(self, sql):
        con = lite.connect(self.database)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

if __name__ == "__main__":
    daemon = SqliteDatabase('/tmp/sqlite_database.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
