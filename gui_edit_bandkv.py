from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import bandcl
import gui_collection_pagekv
import gui_select
# import print_pdf

Builder.load_file('kv_files/kvEditBand.kv')


class EditBand(GridLayout):
    def __init__(self, band, capa_list, collection, **kwargs):
        super(EditBand, self).__init__(**kwargs)
        self.padding = [10, 10, 10, 10]
        self.ids.grid_lay.padding = [0, 10, 0, 20]
        self.band = band
        self.model_lay = gui_collection_pagekv.MyCollectionPage(self.band, capa_list)
        self.add_widget(self.model_lay)
        self.model_lay.bind(on_band_change=self.update_display_band)
        # click button action
        self.register_event_type('on_ok_clicked')
        self.ids.but_ok.bind(on_press=self.ok_button_clicked)
        # import button
        self.ids.but_import.bind(on_press=self.add_imported_model)
        # on name change
        self.ids.inp_name.bind(text=self.change_name)
        self.update_display_band()
        # create event for imported model selection
        self.sel_layout = gui_select.SelectPopup(collection.model_list, title="Select a model to add...")
        self.register_event_type('on_add_from_collec_clicked')
        self.ids.but_import.bind(on_press=self.add_imported_model)
        self.sel_layout.bind(on_item_selected=self.on_popup_return)
        self.sel_layout.bind(on_cancel_clicked=self.cancel_import)
        # print
        # self.ids.but_print.bind(on_press=self.print_band)

    def update_display_band(self, *args):
        self.ids.inp_name.text = self.band.name.encode('utf-8')
        self.ids.lbl_total_cost.text = str(self.band.total_cost) + " pts"
        self.ids.lbl_pers_cost.text = "Perso.: " + str(self.band.personalities_cost) + " pts"
        self.ids.lbl_nb_model.text = str(len(self.band.model_list)) + " models:"
        list_of_models = ""
        for model in self.band.model_list:
            text_added = model.name.encode('utf-8')
            list_of_models += text_added + " ; "
        self.ids.lbl_list_models.text = list_of_models

    def change_name(self, *args):
        self.band.name = self.ids.inp_name.text

    def load_band(self, band):
        self.band = band
        self.model_lay.load_band(band)
        self.update_display_band(band)

    def ok_button_clicked(self, *args):
        self.dispatch('on_ok_clicked')

    def on_ok_clicked(self, *args):
        pass

    def add_imported_model(self, *args):
        self.sel_layout.open()

    def on_popup_return(self, popup, *args):
        self.sel_layout.dismiss()
        new_model = bandcl.Model()
        new_model.copy_model(popup.item_selected)
        self.model_lay.add_model(new_model)
        self.update_display_band(self.band)

    def cancel_import(self, instance):
        self.sel_layout.dismiss()

    def on_add_from_collec_clicked(self):
        pass

    # def print_band(self, instance):
        # print_pdf.print_pdf_band_list(self.band)


class BandEditApp(App):
    def build(self):
        capa_list = bandcl.load_capacities_from_file("data/list_capa.txt")
        band = bandcl.Band("Les Zinzins")
        model1 = bandcl.Model("Burgh")
        model2 = bandcl.Model("Zerbigh")
        model1.set_combat(4)
        model1.add_capacity(capa_list[3])
        model2.set_quality(2)
        model2.add_capacity(capa_list[38])
        band.add_model(model1)
        band.add_model(model2)
        band.add_model(model2)
        page = EditBand(band, capa_list)
        return page


if __name__ == '__main__':
    BandEditApp().run()
