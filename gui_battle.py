from kivy.app import App
import bandcl
import gui_ruleskv
from kivy.uix.carousel import Carousel
import pickle
import gui_band_pagekv
import gui_collection_pagekv
import gui_ruleskv


class BattleCarousel(Carousel):
    def __init__(self, **kwargs):
        super(BattleCarousel, self).__init__(**kwargs)


class BattleApp(App):
    def build(self):
        # get list of capacities
        capa_list = bandcl.load_capacities_from_file("data/list_capa.txt")
        # get saved bands
        try:
            personal_record = open("data/MyBands", 'rb')
            band_list = pickle.load(personal_record)
            personal_record.close()
            if len(band_list) == 0:
                band_list = []
        except:
            band_list = []

        # get saved collection
        try:
            personal_record = open("data/MyCollection", 'rb')
            band_collection = pickle.load(personal_record)
            personal_record.close()
        except:
            band_collection = bandcl.Band("")
        car = BattleCarousel()
        band_page = gui_band_pagekv.BandPage(band_list, capa_list, band_collection)
        rules_page = gui_ruleskv.RulePage(capa_list)
        collection_page = gui_collection_pagekv.MyCollectionPage(band_collection, capa_list)
        car.add_widget(band_page)
        car.add_widget(rules_page)
        car.add_widget(collection_page)

        return car

if __name__ == '__main__':
    BattleApp().run()
