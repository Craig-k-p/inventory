from kivy.app import App
from kivy.uix.label import Label


class TestApp(App):

    def build(self):
        return Label(
            text='Testing 1 2 3',
            font_size=20
            )


if __name__ == "__main__":
    TestApp().run()
