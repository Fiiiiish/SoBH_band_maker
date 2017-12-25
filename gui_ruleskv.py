from kivy.app import App
import bandcl
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

Builder.load_file('kv_files/kvRulesPage.kv')


class RuleText(GridLayout):
    def __init__(self, capa, long_text, **kwargs):
        super(RuleText, self).__init__(**kwargs)
        if capa.personality:
            capa_title = capa.name + " (Personality, " + str(capa.cost) + "pts):"
        else:
            capa_title = capa.name + " (" + str(capa.cost) + "pts):"
        self.ids.lbl_title.text = capa_title
        if long_text:
            self.ids.lbl_text.text = capa.text
        else:
            self.ids.lbl_text.text = capa.help


class CapaList(GridLayout):
    pass


class RulePage(GridLayout):
    def __init__(self, capa_list, **kwargs):
        super(RulePage, self).__init__(**kwargs)
        self.capa_list = capa_list
        self.short_text = CapaList()
        self.long_text = CapaList()
        for capa in capa_list:
            self.short_text.add_widget(RuleText(capa, False))
            self.long_text.add_widget(RuleText(capa, True))
        self.ids.lay_rules_text.add_widget(self.short_text)
        self.ids.switch_text.bind(active=self.swith_text)
        self.ids.but_show_pdf.bind(on_press=self.show_pdf)

    def swith_text(self, instance, value):
        if value:
            self.ids.lay_rules_text.remove_widget(self.short_text)
            self.ids.lay_rules_text.add_widget(self.long_text)
        else:
            self.ids.lay_rules_text.remove_widget(self.long_text)
            self.ids.lay_rules_text.add_widget(self.short_text)

    def show_pdf(self, instance):
        print("pushed")

class RulesApp(App):
    def build(self):
        scroll = ScrollView()
        capacities_list = bandcl.load_capacities_from_file("data/list_capa.txt")
        scroll.add_widget(RulePage(capacities_list))
        return scroll

if __name__ == '__main__':
    RulesApp().run()
