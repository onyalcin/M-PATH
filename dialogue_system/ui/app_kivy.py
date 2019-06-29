#import os
#os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.config import Config
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class MainScreen(BoxLayout):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs, orientation='vertical')

        self._controller = controller

        self._text_input = TextInput(multiline=False)
        self._text_input.bind(on_text_validate=self._on_text_input_validate)

        self._talk_btn = Button(text='Hold to Talk')
        self._talk_btn.bind(on_press=self._on_talk_btn_pressed)
        self._talk_btn.bind(on_release=self._on_talk_btn_released)

        layout = BoxLayout(orientation='horizontal')
        layout.add_widget(Label(text='Text input'))
        layout.add_widget(self._text_input)
        self.add_widget(layout)

        self.add_widget(self._talk_btn)

    def _on_talk_btn_pressed(self, inst):
        self._controller.start_listening()

    def _on_talk_btn_released(self, inst):
        self._controller.stop_listening()

    def _on_text_input_validate(self, inst):
        self._controller.process_text_input(inst.text)


class App(App):

    def __init__(self, controller):
        super().__init__()
        self._controller = controller

    def build(self):
        return MainScreen(controller=self._controller)


def run(controller):
    Config.set('graphics', 'width', '250')
    Config.set('graphics', 'height', '100')
    App(controller=controller).run()
