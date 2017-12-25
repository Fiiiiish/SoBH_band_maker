from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
import bandcl
import gui_modelkv
import gui_modelmaker

Builder.load_file('kv_files/kvCollectionPage.kv')


class MyCollectionPage(GridLayout):
    def __init__(self, band, capa_list, **kwargs):
        super(MyCollectionPage, self).__init__(**kwargs)
        self.padding =  [10, 0, 10, 10]
        self.band = band
        self.fill_collection_layout()
        self.ids.but_add_model.bind(on_press=self.create_model)

        self.model_editor_view = gui_modelmaker.ModelEditor(bandcl.Model("New Model"), capa_list)
        self.popup_model_editor = Popup(title='Edit Model')
        self.popup_model_editor.add_widget(self.model_editor_view)

        self.model_editor_view.bind(on_ok_clicked=self.close_popup_model_editor)

        # create event for external
        self.register_event_type('on_band_change')

    def create_model(self, instance):
        new_model = bandcl.Model("New Model")
        self.add_model(new_model)
        self.edit_model(instance, new_model)
        self.dispatch('on_band_change')

    def fill_collection_layout(self):
        self.ids.lay_list_model.clear_widgets()
        for model in self.band.model_list:
            mod_lay = gui_modelkv.DisplayModelLayout(model)
            self.ids.lay_list_model.add_widget(mod_lay)
            mod_lay.bind(on_delete_clicked=self.delete_model)
            mod_lay.bind(on_copy_clicked=self.copy_model)
            mod_lay.bind(on_edit_clicked=self.edit_model)

    def add_model(self, model):
        self.band.add_model(model)
        mod_lay = gui_modelkv.DisplayModelLayout(model)
        self.ids.lay_list_model.add_widget(mod_lay)
        mod_lay.bind(on_delete_clicked=self.delete_model)
        mod_lay.bind(on_copy_clicked=self.copy_model)
        mod_lay.bind(on_edit_clicked=self.edit_model)

    def copy_model(self, instance, model_src):
        new_model = bandcl.Model("")
        new_model.copy_model(model_src)
        self.add_model(new_model)
        self.dispatch('on_band_change')

    def delete_model(self, instance, model):
        self.band.remove_model(model)
        for child_lay in self.ids.lay_list_model.children:
            if child_lay.model is model:
                self.ids.lay_list_model.remove_widget(child_lay)
        self.dispatch('on_band_change')

    def edit_model(self, instance, model):
        self.model_editor_view.model = model
        self.model_editor_view.load_model(model)
        self.popup_model_editor.open()

    def close_popup_model_editor(self, model):
        self.band.update_cost()
        self.update_model_display(model)
        self.popup_model_editor.dismiss()
        self.dispatch('on_band_change')

    def update_model_display(self, instance):
        for child_lay in self.ids.lay_list_model.children:
            if child_lay.model is instance.model:
                child_lay.update_display()

    def on_band_change(self):
        pass

    def load_band(self, band):
        self.band = band
        self.fill_collection_layout()


class MyCollectionApp(App):
    def build(self):
        capa_list = bandcl.load_capacities_from_file("data/list_capa.txt")
        model1 = bandcl.Model("Burgh")
        model2 = bandcl.Model("Zerbigh")
        model1.set_combat(4)
        model1.add_capacity(capa_list[3])
        model2.set_quality(2)
        model2.add_capacity(capa_list[38])
        band = bandcl.Band("My Band")
        band.add_model(model1)
        band.add_model(model2)
        page = MyCollectionPage(band, capa_list)
        return page


if __name__ == '__main__':
    MyCollectionApp().run()
