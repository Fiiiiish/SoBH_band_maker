from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class TopMenu(GridLayout):
    def __init__(self, **kwargs):
        super(TopMenu, self).__init__(**kwargs)
        self.cols = 5
        self.rows = 1
        self.size_hint = [1, None]
        self.height = '30dp'
        self.padding = [5, 5, 5, 0]

        my_bands_button = ToggleButton(text="My Bands", group="menu", on_press=self.click_my_bands, state='down')
        self.add_widget(my_bands_button)
        my_collection_button = ToggleButton(text="My Collection", group="menu", on_press=self.click_my_collection)
        self.add_widget(my_collection_button)
        rules_button = ToggleButton(text="Rules", group="menu", on_press=self.click_rules)
        self.add_widget(rules_button)
        info_button = Button(text="?", size_hint=[None, 1], width=self.height, on_press=self.click_info)
        self.add_widget(info_button)
        # creating events
        self.register_event_type('on_band_page_selected')
        self.register_event_type('on_collection_page_selected')
        self.register_event_type('on_rules_page_selected')

    def click_my_bands(self, instance):
        self.dispatch('on_band_page_selected')

    def click_my_collection(self, instance):
        self.dispatch('on_collection_page_selected')

    def click_rules(self, instance):
        self.dispatch('on_rules_page_selected')

    def click_info(self, instance):
        popup = Popup(title="About...",
                      content=Label(text="Battlefield in Pocket\nfor\nSong of Blades and Heroes\n\n\n\n\nv0.1\n(c) Christophe Fischer, "
                                         "2017", halign="center"),
                      size_hint=(0.9, 0.5))
        popup.open()

    def on_rules_page_selected(self):
        pass

    def on_collection_page_selected(self):
        pass

    def on_band_page_selected(self):
        pass


class TopMenuTest(App):
    def build(self):
        return TopMenu()

if __name__ == '__main__':
    TopMenuTest().run()
