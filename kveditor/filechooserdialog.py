# -*- coding: utf-8 -*-

__all__ = [r'FileChooserDialog']

import kivy
kivy.require(r'1.9.1')
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.factory import Factory


class FileChooserDialog(Factory.ModalView):

    filepath = StringProperty()

    def on_button_cancel(self):
        self.dismiss()

    def on_button_ok(self):
        selection = self.ids.filechooser.selection
        if len(selection) > 0:
            self.filepath = selection[0]
        self.dismiss()


Builder.load_string(r'''
<FileChooserDialog>:
    BoxLayout:
        size_hint: 1, 1
        orientation: r'vertical'
        FileChooserListView:
            id: filechooser
        BoxLayout:
            orientation: r'horizontal'
            size_hint_y: None
            height: 30
            Button:
                text: r'Cancel'
                on_release: root.on_button_cancel()
            Button:
                text: r'OK'
                on_release: root.on_button_ok()
''')


def _test():
    from kivy.base import runTouchApp

    root = Builder.load_string(r'''
BoxLayout:
    orientation: r'vertical'
    Label:
        id: id_label
    Button:
        text: r'click to choose file'
        id: id_button''')
    dialog = FileChooserDialog()
    dialog.bind(filepath=root.ids.id_label.setter(r'text'))
    root.ids.id_button.bind(on_press=dialog.open)
    runTouchApp(root)


if __name__ == r'__main__':
    _test()
