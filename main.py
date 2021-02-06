#!/usr/bin/env python3
#
# from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
# from kivy.uix.label import Label
# from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout

from kivymd.icon_definitions import md_icons
from kivy.metrics import dp
from kivymd.app import MDApp

import os
import sqlite3
from kivy.utils import platform
import datetime,time


# from fmn_main import Main, RecycleViewRow

class MainWindow(Screen):
  pass

class SettingsWindow(Screen):
  pass

class RecycleViewRow(BoxLayout,RecycleDataViewBehavior):

  def do_up(self):
    print(f"UP {self.text}")

  def do_down(self):
    print(f"DOWN {self.text}")

class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
  pass

class WindowManager(ScreenManager):
  pass

colors = {
    "Teal": {
        "50": "e4f8f9",
        "100": "bdedf0",
        "200": "97e2e8",
        "300": "79d5de",
        "400": "6dcbd6",
        "500": "6ac2cf",
        "600": "63b2bc",
        "700": "5b9ca3",
        "800": "54888c",
        "900": "486363",
        "A100": "bdedf0",
        "A200": "97e2e8",
        "A400": "6dcbd6",
        "A700": "5b9ca3",
    },
    "Blue": {
        "50": "e3f3f8",
        "100": "b9e1ee",
        "200": "91cee3",
        "300": "72bad6",
        "400": "62acce",
        "500": "589fc6",
        "600": "5191b8",
        "700": "487fa5",
        "800": "426f91",
        "900": "35506d",
        "A100": "b9e1ee",
        "A200": "91cee3",
        "A400": "62acce",
        "A700": "487fa5",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "F5F5F5",
        "Background": "FAFAFA",
        "CardsDialogs": "FFFFFF",
        "FlatButtonDown": "cccccc",
    },
    "Dark": {
        "StatusBar": "000000",
        "AppBar": "212121",
        "Background": "303030",
        "CardsDialogs": "424242",
        "FlatButtonDown": "999999",
    }
}

class Main(Screen):
  data_items = ListProperty()
  cursor = ObjectProperty()
  connection = ObjectProperty()

# int id # идентификатор, primary key, uniq
# int parent # идентификатор родителя (0 для корневого)
# string title # подпись
# int x,y,w,h # описание рамки на родительском фото
# int photo # номер фотографии (0, если фото нет)
# int weight # порядковый номер в родительском списке
# int deleted # признак удаления
# timedate created # время и дата создания
# timedate updated # время и дата последнего изменения/удале

  def init_db(self):
    x = self.cursor.execute(\
        "CREATE TABLE IF NOT EXISTS Items(ID INTEGER PRIMARY KEY, TITLE TEXT, "\
        "PARENT INTEGER, X INTEGER DEFAULT 0, Y INTEGER DEFAULT 0, "\
        "W INTEGER DEFAULT 0, H INTEGER DEFAULT 0, "\
        "PHOTO INTEGER DEFAULT 0, WEIGHT INTEGER DEFAULT 0, IS_DEL INTEGER DEFAULT 0, "\
        "CREATED INTEGER DEFAULT 0, UPDATED INTEGER DEFAULT 0)"\
        )
    self.connection.commit()

  def get_users(self):

    # self.connection = sqlite3.connect("fmn.db", isolation_level=None)
    # app_path = os.path.dirname(__file__)
    store_path = '.' #app_storage_path()

    self.connection = sqlite3.connect(os.path.join(store_path, 'my.db'))
    self.cursor = self.connection.cursor()
    

    # Check if table is present and seed it
    # TODO: delete this code in production
    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Items'")
    table = self.cursor.fetchall()
    if len(table) < 1:
        self.init_db()
        for i in list(range(3)):
          t = time.time()
          self.cursor.execute(f"INSERT INTO Items (TITLE, PARENT, WEIGHT, CREATED, UPDATED) VALUES ('Item{i}', 0, {3-i}, {t}, {t})")

    # TODO: uncomment in production
    # self.init_db()
    self.cursor.execute("SELECT * FROM Items ORDER BY ID ASC")
    # id, title, parent, x,y,w,h, photo, weight, is_del, created, updated
    rows = self.cursor.fetchall()

    ml = self.ids['main_list']
    # create data_items
    data = [{'myid': row[8], 'text': f"{row[1]} @{row[2]} {row[3]}:{row[4]} {row[5]}x{row[6]}"} for row in rows]
    ml.data = sorted(data, key=lambda x: x['myid'])
    ml.refresh_from_data()

    im = self.ids['item_image']
    im.source = 'photo.jpeg'


  # def update_db(self, newvalue, idx):
  #   names = ['TITLE','cbTime','cbRems']
  #   row = 1+ idx // 4
  #   pos = 1+ idx % 4
  #   update = newvalue, row
  #   print(f"row: {row}; pos: {pos}; idx: {idx}; val: {newvalue};")
  #   print(f"UPDATE Items SET {names[pos]} = {update[0]} WHERE ID = {update[1]}")
  #   self.cursor.execute(f'UPDATE Items SET {names[pos]} = ? WHERE ID = ?', update)

  #   self.connection.commit()






kv = Builder.load_file('fmn.kv')

class ForgetMeNotApp(MDApp):
    title = "Forget Me Not"

    def build(self):
        #self.root = WindowManager() #RV()
        #self.root = RV()
        sm = ScreenManager()
        self.main = Main()
        sm.add_widget(self.main)
        sm.add_widget(SettingsWindow())

        # self.theme_cls.theme_style = "Dark"  # "Light"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        return sm

    def on_start(self):
        self.main.get_users()


if __name__ == "__main__":
    app = ForgetMeNotApp()
    app.run()
