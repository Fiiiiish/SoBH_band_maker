from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
import bandcl

Builder.load_file('kv_files/kvModel.kv')


class CapacityDisplayLabel(Label):
    pass


class EditModelLayout(GridLayout):
    def __init__(self, model, **kwargs):
        super(EditModelLayout, self).__init__(**kwargs)
        self.padding = [10, 0, 10, 0]
        self.model = model
        self.update_display()
        # bindings
        self.ids.but_combat_plus.bind(on_press=self.up_combat)
        self.ids.but_combat_minus.bind(on_press=self.down_combat)
        self.ids.but_quality_plus.bind(on_press=self.up_quality)
        self.ids.but_quality_minus.bind(on_press=self.down_quality)
        self.ids.inp_name.bind(text=self.change_name)

    def update_display(self):
        self.ids.inp_name.text = self.model.name
        if self.model.personality:
            self.ids.lbl_cost.text = "(Personality)    " + str(self.model.cost) + " pts"
        else:
            self.ids.lbl_cost.text = str(self.model.cost) + " pts"
        self.ids.lbl_quality.text = str(self.model.quality) + "+"
        self.ids.lbl_combat.text = str(self.model.combat)
        capa_str = "Capacitites: "
        for capa in self.model.capacities_list:
            capa_str += str(capa.name) + " ; "
            self.ids.list_capacities.text = capa_str

    def change_name(self, instance, value):
        self.model.name = self.ids.inp_name.text

    def up_combat(self, instance):
        if int(self.ids.lbl_combat.text) in range(5):
            new_value = int(self.ids.lbl_combat.text) + 1
            self.model.set_combat(new_value)
            self.update_display()

    def down_combat(self, instance):
        if int(self.ids.lbl_combat.text) in range(1, 6):
            new_value = int(self.ids.lbl_combat.text) - 1
            self.model.set_combat(new_value)
            self.update_display()

    def up_quality(self, instance):
        old_value = int(self.ids.lbl_quality.text.split("+", 1)[0])
        if old_value in range(3, 7):
            new_value = old_value - 1
            self.model.set_quality(new_value)
            self.update_display()

    def down_quality(self, instance):
        old_value = int(self.ids.lbl_quality.text.split("+", 1)[0])
        if old_value in range(6):
            new_value = old_value + 1
            self.model.set_quality(new_value)
            self.update_display()

    def load_model(self, model):
        self.model = model
        self.update_display()


class DisplayModelLayout(GridLayout):
    def __init__(self, model, **kwargs):
        self.padding = ['5dp', '5dp', '5dp', '5dp']
        self.register_event_type('on_delete_clicked')
        self.register_event_type('on_copy_clicked')
        self.register_event_type('on_edit_clicked')
        super(DisplayModelLayout, self).__init__(**kwargs)
        self.model = model
        self.update_display()
        # bindings
        self.ids.but_copy.bind(on_press=self.copy_clicked)
        self.ids.but_edit.bind(on_press=self.edit_clicked)
        self.ids.but_delete.bind(on_press=self.delete_clicked)

    def update_display(self):
        self.ids.lbl_name.text = self.model.name
        if self.model.personality:
            self.ids.lbl_cost.text = "(P) " + str(self.model.cost) + " pts"
        else:
            self.ids.lbl_cost.text = str(self.model.cost) + " pts"
        self.ids.lbl_quality.text = str(self.model.quality) + "+"
        self.ids.lbl_combat.text = str(self.model.combat)
        capa_str = "Capacitites: "
        for capa in self.model.capacities_list:
            capa_str += str(capa.name) + " ; "
        self.ids.list_capacities.text = capa_str

    def delete_clicked(self, instance):
        self.dispatch('on_delete_clicked', self.model)

    def copy_clicked(self, instance):
        self.dispatch('on_copy_clicked', self.model)

    def edit_clicked(self, instance):
        self.dispatch('on_edit_clicked', self.model)

    def on_delete_clicked(self, model, *args):
        pass

    def on_copy_clicked(self, model, *args):
        pass

    def on_edit_clicked(self, model, *args):
        pass

    def load_model(self, model):
        self.model = model
        self.update_display()


class GuiModelApp(App):
    models_wid = GridLayout(cols=1, spacing=10, padding=[0, 10, 0, 10], size_hint=[1, None])
    my_mod = bandcl.Model("Barbare")
    ind = 0
    listc = bandcl.load_capacities_from_file("data/list_capa.txt")

    # FONCTION DE TEST
    def add_mdl(self, instance):
        self.my_mod.add_capacity(self.listc[self.ind])
        self.ind += 1
        self.models_wid.add_widget(
            EditModelLayout(self.my_mod))
        self.models_wid.height = self.models_wid.height + 120

    def build(self):
        main_win = ScrollView()
        add_mdl_but = Button(text="Add model...", height=50, size_hint=[1, None], on_press=self.add_mdl)
        self.models_wid.add_widget(add_mdl_but)
        self.models_wid.height = 70
        main_win.add_widget(self.models_wid)
        return main_win


if __name__ == '__main__':
    GuiModelApp().run()
