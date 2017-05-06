# -*- coding: utf-8 -*-

__all__ = [r'MessagePopup', r'show_message_popup']

import kivy
kivy.require(r'1.9.1')
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.factory import Factory


class MessagePopup(Factory.ModalView):

    text = StringProperty()


def show_message_popup(text):
    MessagePopup(text=text).open()


Builder.load_string(r'''
<MessagePopup>:
    size_hint: 0.9, 0.9
    on_touch_down: self.dismiss()  # ユーザーが画面をどこでもいいのでTouch(Click)したら閉じる
    Label:
        font_size: 30
        text: root.text
        size_hint: 0.96, 0.96
        pos_hint: {r'center_x': 0.5, r'center_y': 0.5}
''')


def _test():

    from kivy.base import runTouchApp

    root = Factory.Button(text=r'click to show message')
    # root.bind(on_press=(lambda *args: show_message_popup(r'show_message_popup test')))  # 使い方A
    root.bind(on_press=MessagePopup(text=r'MessagePopup test').open)  # 使い方B
    runTouchApp(root)


if __name__ == r'__main__':
    _test()
