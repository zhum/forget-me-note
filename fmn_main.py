from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

import os
import sqlite3
#from android.storage import app_storage_path

import datetime

class MainWindow(Screen):
  pass

# class RecycleViewRow(RecycleDataViewBehavior, BoxLayout):
#   index = None

#   def __init__(txt):
#     text = txt
#     super()

# class SelectableButton(RecycleDataViewBehavior, Button):
#   ''' Add selection support to the Button '''
#   index = None
#   selected = BooleanProperty(False)
#   selectable = BooleanProperty(True)

#   def refresh_view_attrs(self, rv, index, data):
#     ''' Catch and handle the view changes '''
#     self.index = index
#     return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

#   def on_touch_down(self, touch):
#     ''' Add selection on touch down '''
#     if super(SelectableButton, self).on_touch_down(touch):
#         return True
#     if self.collide_point(*touch.pos) and self.selectable:
#         return self.parent.select_with_touch(self.index, touch)

#   def apply_selection(self, rv, index, is_selected):
#     ''' Respond to the selection of items in the view. '''
#     self.selected = is_selected

#   def on_press(self):
#     popup = TextInputPopup(self)
#     popup.open()

#   def update_changes(self, txt):
#     # if self.index < 4:
#     #     i_d = 3
#     # elif self.index > 3 and self.index < 8:
#     #     i_d = 2
#     # else:
#     #     i_d = 1
#     self.text = txt
#     app.main.update_db(txt, self.index)


# class Main(Screen):
#   data_items = ListProperty()
#   cursor = ObjectProperty()
#   connection = ObjectProperty()

#   def init_db(self):
#     x = self.cursor.execute("CREATE TABLE IF NOT EXISTS Callbacks(cID INTEGER PRIMARY KEY, cName TEXT, cbTime INT, cbRems TEXT)")
#     for i in list(range(3)):
#       t = datetime.datetime.now().minute
#       self.cursor.execute(f"INSERT INTO Callbacks (cName, cbTime, cbRems) VALUES ('Client{i}', {1700+t},'Test{i}')")
#     self.connection.commit()

#   def get_users(self):

#     # self.connection = sqlite3.connect("fmn.db", isolation_level=None)
#     # app_path = os.path.dirname(__file__)
#     store_path = '.' #app_storage_path()

#     self.connection = sqlite3.connect(os.path.join(store_path, 'my.db'))
#     self.cursor = self.connection.cursor()
#     self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Callbacks'")
#     table = self.cursor.fetchall()
#     if len(table) < 1:
#       self.init_db()

#     self.cursor.execute("SELECT * FROM Callbacks ORDER BY ROWID ASC")

#     rows = self.cursor.fetchall()

#     ml = self.ids['main_list']
#     # create data_items
#     # for row in rows:
#     #   print(f"--> {row[0]}")
#     #   w = RecycleViewRow()
#     #   w.text=f"{row[0]} - {row[1]} - {row[2]} - {row[3]}"
#     #   ml.data.append(w)

#     # for row in rows:
#     #   pass

#   def update_db(self, newvalue, idx):
#     names = ['cName','cbTime','cbRems']
#     row = 1+ idx // 4
#     pos = 1+ idx % 4
#     update = newvalue, row
#     print(f"row: {row}; pos: {pos}; idx: {idx}; val: {newvalue};")
#     print(f"UPDATE Callbacks SET {names[pos]} = {update[0]} WHERE cID = {update[1]}")
#     self.cursor.execute(f'UPDATE Callbacks SET {names[pos]} = ? WHERE cID = ?', update)

#     self.connection.commit()

