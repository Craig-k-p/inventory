from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty


class ScreenOne(Screen):

    box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)

        a = Widgets()
        self.box.add_widget(a)


class Widgets(GridLayout):

    lab1 = ObjectProperty()
    lab2 = ObjectProperty()

    def change_text(self):
        self.lab1.sub_lab.text = 'Changed!'
        self.lab2.sub_lab.text = 'OK'


Builder.load_file('test.kv')

sm = ScreenManager()
sm.add_widget(ScreenOne(name='screen one'))

Builder.unload_file('test.kv')


class test(App):
    def build(self):
        return sm


test().run()
