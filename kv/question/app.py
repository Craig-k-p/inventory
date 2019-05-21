from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


class AccountWindow(Screen):
    pass


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)


class kvApp(App):
    def build(self):
        # self.sm allows access to sm from any kv file using app.sm
        self.sm = sm
        return sm


if __name__ == '__main__':
    Builder.load_file("kv.kv")

    sm = WindowManager()
    # db = DataBase('users.txt')

    screens = [AccountWindow()]

    # Make sure sm knows how to handle changes to sm.current
    for screen in screens:
        sm.add_widget(screen)

    # Set the current screen to login window
    sm.current = 'account window'

    kvApp().run()
