from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
import bandcl
import gui_edit_bandkv
import pickle

Builder.load_file('kv_files/kvBandPage.kv')

class ValidPopup(Popup):
    def __init__(self, **kwargs):
        super(ValidPopup, self).__init__(**kwargs)
        self.ids.ok_but.bind(on_press=self.ok_pressed)
        self.ids.cancel_but.bind(on_press=self.cancel_pressed)
        self.register_event_type('on_ok_clicked')

    def cancel_pressed(self, *args):
        self.dismiss()

    def ok_pressed(self, *args):
        self.dispatch('on_ok_clicked')

    def on_ok_clicked(self, *args):
        pass


class BandPage(GridLayout):
    def __init__(self, band_list, capa_list, collection, **kwargs):
        super(BandPage, self).__init__(**kwargs)
        self.padding = [10, 0, 10, 10]
        self.band_list = band_list
        # create edit page
        self.popup_band_editor = Popup(title='Edit Band')
        ex_band = bandcl.Band("a")
        self.band_editor_view = gui_edit_bandkv.EditBand(ex_band, capa_list, collection)
        self.popup_band_editor.add_widget(self.band_editor_view)
        self.band_editor_view.bind(on_ok_clicked=self.close_popup_model_editor)
        # create bands items
        for band in self.band_list:
            band_layout = BandDisplay(band)
            self.ids.lay_list_band.add_widget(band_layout)
            band_layout.ids.but_copy.bind(on_press=self.copy_band)
            band_layout.ids.but_delete.bind(on_press=self.delete_band)
            band_layout.ids.but_edit.bind(on_press=self.edit_band)
        self.ids.but_create_band.bind(on_press=self.create_band)
        # are you sure popup
        self.band_to_delete = None
        self.valid_delete_popup = ValidPopup()
        self.valid_delete_popup.bind(on_ok_clicked=self.remove_band)

    def add_band(self, band, edit=True):
        self.band_list.append(band)
        band_layout = BandDisplay(band)
        self.ids.lay_list_band.add_widget(band_layout)
        band_layout.ids.but_copy.bind(on_press=self.copy_band)
        band_layout.ids.but_delete.bind(on_press=self.delete_band)
        band_layout.ids.but_edit.bind(on_press=self.edit_band)
        if edit:
            self.band_editor_view.load_band(band)
            self.popup_band_editor.open()

    def remove_band(self, *args):
        self.valid_delete_popup.dismiss()
        self.band_list.remove(self.band_to_delete)
        for band_lay in self.ids.lay_list_band.children:
            if band_lay.band is self.band_to_delete:
                self.ids.lay_list_band.remove_widget(band_lay)

    def create_band(self, instance):
        new_band = bandcl.Band("New Band")
        self.add_band(new_band)

    def copy_band(self, instance):
        src_band = instance.parent.parent.parent.parent.band
        new_band = bandcl.Band("")
        new_band.copy_band(src_band)
        self.add_band(new_band, False)

    def delete_band(self, instance):
        self.band_to_delete = instance.parent.parent.parent.parent.band
        self.valid_delete_popup.open()

    def on_popup_return(self):
        self.valid_delete_popup.dismiss()
        self.remove_band(self.band_to_delete)

    def edit_band(self, instance):
        band = instance.parent.parent.parent.parent.band
        self.band_editor_view.load_band(band)
        self.popup_band_editor.open()

    def close_popup_model_editor(self, instance):
        self.popup_band_editor.dismiss()
        # update display
        for band_lay in self.ids.lay_list_band.children:
            if band_lay.band is self.band_editor_view.band:
                band_lay.update_display()
        # save bands
        personal_record = open("MyBands", 'wb')
        pickle.dump(self.band_list, personal_record)
        personal_record.close()


class BandDisplay(GridLayout):
    def __init__(self, band, **kwargs):
        super(BandDisplay, self).__init__(**kwargs)
        self.spacing = 20
        self.ids.lay_grid.spacing = 15
        self.padding = ['5dp', '5dp', '9dp', '5dp']
        self.band = band
        self.update_display()

    def update_display(self):
        self.ids.lbl_band_name.text = self.band.name
        self.ids.lbl_total_cost.text = str(self.band.total_cost) + " pts"
        self.ids.lbl_personalities_cost.text = "Pers. : " + str(self.band.personalities_cost) + " pts"
        self.ids.lbl_nb_models.text = str(len(self.band.model_list)) + " models"
        str_model_list = ""
        for model in self.band.model_list:
            text_added = model.name.encode('utf-8')
            str_model_list += text_added + " ; "
        self.ids.lbl_model_list.text = str_model_list


class BandPageApp(App):
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
        band2 = bandcl.Band("hehe")
        band3 = bandcl.Band("Waaaaagh")
        band2.add_model(model1)
        band3.add_model(model2)
        band_list = [band, band2, band3, band, band2, band3, band, band2, band3]
        page = BandPage(band_list, capa_list)
        return page


if __name__ == '__main__':
    BandPageApp().run()
