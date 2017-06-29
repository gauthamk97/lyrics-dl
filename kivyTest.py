import kivy
#kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Username'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
    
    def on_touch_down(self, touch):
        print touch


class MyApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
