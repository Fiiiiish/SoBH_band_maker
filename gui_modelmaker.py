from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import gui_modelkv
import gui_capacitieskv
import bandcl


class ModelEditor(GridLayout):
    def __init__(self, model, capacities_list, **kwargs):
        super(ModelEditor, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 20
        self.padding = [0, 10, 0, 0]
        self.model = model
        self.selected_capacities = []
        self.ok_button = Button(text='OK', size_hint=[1, None], height='40dp')
        self.model_lay = gui_modelkv.EditModelLayout(model)
        self.scroll = ScrollView()
        self.capa_lay = gui_capacitieskv.CapacityGrid(capacities_list)
        self.scroll.add_widget(self.capa_lay)
        self.add_widget(self.ok_button)
        self.add_widget(self.model_lay)
        self.add_widget(self.scroll)

        # check boxes of capacities already in models
        self.capa_lay.check_capacity(self.model.capacities_list)

        # on capacity selection
        self.capa_lay.bind(on_capacity_clicked=self.update_capacity_list)

        # click button action
        self.register_event_type('on_ok_clicked')
        self.ok_button.bind(on_press=self.ok_button_clicked)

    def update_capacity_list(self, instance, clist):
        self.model.clean_capacity()
        for capa in clist:
            self.model.add_capacity(capa)
        self.model_lay.update_display()

    def load_model(self, model):
        self.model = model
        self.capa_lay.check_capacity(self.model.capacities_list)
        self.model_lay.load_model(self.model)

    def ok_button_clicked(self, *args):
        self.dispatch('on_ok_clicked')

    def on_ok_clicked(self, *args):
        pass


class ModelEditorApp(App):
    def build(self):
        model = bandcl.Model("Burgh")
        capa_list = bandcl.load_capacities_from_file("data/list_capa.txt")
        model.set_combat(4)
        model.add_capacity(capa_list[3])
        model.add_capacity(capa_list[38])
        return ModelEditor(model, capa_list)


if __name__ == '__main__':
    ModelEditorApp().run()
