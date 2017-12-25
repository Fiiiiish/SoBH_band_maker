from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
import bandcl

Builder.load_file('kv_files/kvSelection.kv')


class SelectPopup(Popup):
    def __init__(self, item_list, **kwargs):
        self.register_event_type('on_item_selected')
        self.register_event_type('on_cancel_clicked')
        super(SelectPopup, self).__init__(**kwargs)
        self.item_list = item_list
        self.ids.but_cancel.bind(on_press=self.on_cancel_click)
        self.item_selected = None
        for item in self.item_list:
            but = ButtonItem(item)
            but.bind(on_press=self.item_clicked)
            self.ids.lay_list.add_widget(but)

    def on_open(self):
        self.ids.lay_list.clear_widgets()
        for item in self.item_list:
            but = ButtonItem(item)
            but.bind(on_press=self.item_clicked)
            self.ids.lay_list.add_widget(but)

    def on_cancel_click(self, instance):
        self.item_selected = None
        self.dispatch('on_cancel_clicked')

    def item_clicked(self, instance):
        self.item_selected = instance.item
        self.dispatch('on_item_selected')

    def on_item_selected(self):
        pass

    def on_cancel_clicked(self):
        pass


class ButtonItem(Button):
    def __init__(self, item, **kwargs):
        super(ButtonItem, self).__init__(**kwargs)
        self.item = item
        self.text = item.display()
        self.size_hint = [1, None]
        self.height = '40dp'


class SelectApp(App):
    def build(self):
        capa_list = bandcl.load_capacities_from_file("data/list_capa.txt")
        model1 = bandcl.Model("Burgh")
        model2 = bandcl.Model("Zerbigh")
        model1.set_combat(4)
        model1.add_capacity(capa_list[3])
        model2.set_quality(2)
        model2.add_capacity(capa_list[38])
        liste = []
        mainwin = SelectPopup(capa_list)
        return mainwin


if __name__ == '__main__':
    SelectApp().run()
