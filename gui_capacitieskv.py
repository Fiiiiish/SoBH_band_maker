from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
import bandcl

Builder.load_file('kv_files/kvCapacitiesSelector.kv')


class CapacityGrid(StackLayout):
    def __init__(self, capacities_list, **kwargs):
        self.register_event_type('on_capacity_clicked')
        super(CapacityGrid, self).__init__(**kwargs)
        for capacity in capacities_list:
            cwid = CapacityWidget(capacity=capacity)
            cwid.ids.chckbox.bind(active=self.get_checked_boxes)
            self.add_widget(cwid)
        self.selected_capacities = []

    def get_checked_boxes(self, instance, value):
        if value:
            self.selected_capacities.append(instance.parent.parent.capacity)
        else:
            self.selected_capacities.remove(instance.parent.parent.capacity)
        self.dispatch('on_capacity_clicked', self.selected_capacities)

    def check_capacity(self, capacity_list):
        for capawid in self.children:
            capawid.ids.chckbox.active = False
            for capa_model in capacity_list:
                if capawid.capacity.name == capa_model.name:
                    capawid.ids.chckbox.active = True
                    break

    def on_capacity_clicked(self, value, *args):
        pass


class CapacityWidget(GridLayout):
    def __init__(self, capacity, **kwargs):
        super(CapacityWidget, self).__init__(**kwargs)
        self.capacity = capacity
        self.ids.lbl_name.text = capacity.name
        self.ids.lbl_cost.text = str(capacity.cost)
        if capacity.personality is True:
            self.ids.lbl_name.bold = True
        self.ids.chckbox.active = False


class CapacitiesApp(App):
    def build(self):
        scroll = ScrollView(size_hint=[1, 1])
        mainwid = CapacityGrid(bandcl.load_capacities_from_file("data/list_capa.txt"))
        scroll.add_widget(mainwid)
        return scroll


if __name__ == '__main__':
    CapacitiesApp().run()
