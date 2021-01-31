from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
import os
import sqlite3

class Main(Screen):
    data_items = ListProperty()
    cursor = ObjectProperty()
    connection = ObjectProperty()

    def get_users(self):

        if not os.path.exists('demo.db'):
            self.connection = sqlite3.connect("demo.db", isolation_level=None)
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS Callbacks(cName TEXT, cID INT, cbTime INT, cbRems TEXT)")
            self.cursor.execute("INSERT INTO Callbacks VALUES ('Client1','1','1500','Test1')")
            self.cursor.execute("INSERT INTO Callbacks VALUES ('Client2','2','1600','Test2')")
            for i in list(range(35)):
              self.cursor.execute(f"INSERT INTO Callbacks VALUES ('Client{i}','{i}','1700','Test{i}')")
            self.connection.commit()
            self.cursor.execute("SELECT * FROM Callbacks ORDER BY ROWID DESC")
        else:
            self.connection = sqlite3.connect("demo.db", isolation_level=None)
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT * FROM Callbacks ORDER BY ROWID DESC")

        rows = self.cursor.fetchall()

        # create data_items
        for row in rows:
            for col in row:
                self.data_items.append(col)

        for row in rows:
            pass

    def update_db(self, newvalue, i_d, idx):
        update = newvalue, i_d
        if idx in (0, 4, 8):
            self.cursor.execute('UPDATE Callbacks SET cName = ? WHERE cID = ?', update)
        elif idx in (2, 6, 10):
            self.cursor.execute('UPDATE Callbacks SET cbTime = ? WHERE cID = ?', update)
        elif idx in (3, 7, 11):
            self.cursor.execute('UPDATE Callbacks SET cbRems = ? WHERE cID = ?', update)
        self.connection.commit()

