from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from gui_top_menu import TopMenu
import gui_collection_pagekv
import gui_ruleskv
import gui_band_pagekv
import bandcl
import pickle
from kivy.config import Config

Config.read("kv_files/config.ini")


class SoBHBandMaker(App):
    def build(self):
        self.icon = "data/iconApp.png"
        self.title = "Battlefield in Pocket - SoBH"
        # get list of capacities
        capa_list = bandcl.load_capacities_from_file("data/list_capa.txt")
        # get saved bands
        try:
            personal_record = open("data/MyBands", 'rb')
            self.band_list = pickle.load(personal_record)
            personal_record.close()
            if len(self.band_list) == 0:
                self.band_list = []
        except:
            self.band_list = []

        # get saved collection
        try:
            personal_record = open("data/MyCollection", 'rb')
            self.band_collection = pickle.load(personal_record)
            personal_record.close()
        except:
            self.band_collection = bandcl.Band("")

        # Build menu
        self.menu = TopMenu()
        # bind to menu
        self.menu.bind(on_rules_page_selected=self.show_rules_page)
        self.menu.bind(on_collection_page_selected=self.show_collection_page)
        self.menu.bind(on_band_page_selected=self.show_band_page)

        # build pages
        self.band_page = gui_band_pagekv.BandPage(self.band_list, capa_list, self.band_collection)
        self.rules_page = gui_ruleskv.RulePage(capa_list)
        self.collection_page = gui_collection_pagekv.MyCollectionPage(self.band_collection, capa_list)

        # build main windows
        main_win = GridLayout(cols=1, spacing=10, size_hint=[1, None], size=(Window.width, Window.height))
        main_win.add_widget(self.menu)
        self.central_layout = ScrollView(bar_width=5)
        self.central_layout.add_widget(self.band_page)
        main_win.add_widget(self.central_layout)

        return main_win

    def show_rules_page(self, instance):
        self.central_layout.clear_widgets()
        self.central_layout.add_widget(self.rules_page)
        personal_record = open("data/MyCollection", 'wb')
        pickle.dump(self.band_collection, personal_record)
        personal_record.close()

    def show_collection_page(self, instance):
        self.central_layout.clear_widgets()
        self.central_layout.add_widget(self.collection_page)

    def show_band_page(self, instance):
        self.central_layout.clear_widgets()
        self.central_layout.add_widget(self.band_page)
        personal_record = open("data/MyCollection", 'wb')
        pickle.dump(self.band_collection, personal_record)
        personal_record.close()

    def save_bands(self):
        # save bands
        personal_record = open("data/MyBands", 'wb')
        pickle.dump(self.band_list, personal_record)
        personal_record.close()

    def on_stop(self):
        self.save_bands()
        # save collection
        personal_record = open("data/MyCollection", 'wb')
        pickle.dump(self.band_collection, personal_record)
        personal_record.close()


if __name__ == '__main__':
    SoBHBandMaker().run()
