from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class ThingView(GridLayout):
    name = ObjectProperty(None)
    weight = ObjectProperty(None)
    val = ObjectProperty(None)
    tags = ObjectProperty(None)
