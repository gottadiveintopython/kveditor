# -*- coding: utf-8 -*-

import sys
import io
import os.path
from functools import cached_property

import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.window import Window


def check_if_xpopup_is_installed() -> bool:
    try:
        import kivy.garden.xpopup
    except (ImportError, KeyError):
        print("You don't have 'kivy.garden.xpopup' installed. You cannot perform I/O operations.", file=sys.stderr)
        return False
    return True


def tab2spaces(text):
    return text.replace('\t', '    ')


class KvEditorApp(App):
    def on_start(self):
        self.root.kve_start()


class KvEditor(Factory.FloatLayout):

    @cached_property
    def _kv_filename(self):
        return 'KvEditor_internal.' + str(self.uid)

    def on_keyboard(self, instance, key, scancode, codepoint, modifiers):
        '''Keyboard入力があった時に呼ばれるMethod

        以下のShortcutKeyを実現している
            Ctrl + P => Preview
            Ctrl + S => Save
            Ctrl + L => Load
        '''
        if len(modifiers) == 1 and modifiers[0] == 'ctrl':
            if codepoint == 'p':
                self.kve_preview()
            elif codepoint == 's':
                self.kve_save()
            elif codepoint == 'l':
                self.kve_load()

    def kve_start(self):
        '''アプリケーション開始時に行いたい処理を書いておくMethod'''

        Window.bind(on_keyboard=self.on_keyboard)

    def kve_choosefile(self):
        if not check_if_xpopup_is_installed():
            return
        from kivy.garden.xpopup.file import XFileOpen
            
        def on_dismiss(popup):
            if popup.is_canceled():
                return
            filepath = popup.selection[0]
            self.ids.ti_filepath.text = filepath
            self.last_opened_dir = os.path.dirname(filepath)
        last_opened_dir = getattr(self, 'last_opened_dir', os.path.curdir)
        XFileOpen(on_dismiss=on_dismiss, multiselect=False, path=last_opened_dir)

    def kve_load(self):
        '''Fileの中身をEditorに読み込む'''
        if not check_if_xpopup_is_installed():
            return
        from kivy.garden.xpopup.notification import XMessage

        editor = self.ids.editor
        filepath = self.ids.ti_filepath.text
        try:
            with io.open(filepath, 'rt', encoding='utf-8') as reader:
                editor.text = tab2spaces(reader.read())
        except (OSError, IOError) as e:
            XMessage(title='Error', text='Failed to load from the file : {}\n{}'.format(filepath, e.strerror))

    def kve_save(self):
        '''EditorのtextをFileに書き込む'''
        if not check_if_xpopup_is_installed():
            return
        from kivy.garden.xpopup.notification import XMessage

        editor = self.ids.editor
        editor.text = tab2spaces(editor.text)
        filepath = self.ids.ti_filepath.text
        try:
            with io.open(filepath, 'wt', encoding='utf-8') as writer:
                writer.write(editor.text)
        except (OSError, IOError) as e:
            XMessage(title='Error', text='Failed to write to the file : {}\n{}'.format(filepath, e.strerror))

    def kve_preview(self):
        '''EditorのtextからWidgetを作って左側にPreview

        Builder.load_stringは
        1. 与えられたKvコードに問題があると例外を投げる
        2. 与えられたKvコードにroot ruleが無い時はNoneを返す
        ようなので、その場合はそれがユーザーに分かるようエラーメッセージの書かれた
        Labelを作って貼り付けている
        '''

        editor = self.ids.editor  # Editor部分のWidget(CodeInput)
        preview = self.ids.preview  # Preview貼り付け先のWidget
        editor.text = tab2spaces(editor.text)
        preview.clear_widgets()  # 以前のPreviewを破棄
        Builder.unload_file(self._kv_filename)  # 以前のKvコードを無効化

        widget = None
        try:
            widget = Builder.load_string(
                editor.text,
                filename=self._kv_filename
            )
        except Exception as e:
            temp = [str(e.__class__)]
            temp.extend([str(arg) for arg in e.args])
            error_msg = '\n'.join(temp)
        else:
            if widget is None:
                error_msg = 'No root rule.'
        if widget is None:
            # Widgetの作成に失敗した時は、代わりにエラーメッセージの書かれたLabel
            # を貼り付ける
            preview.add_widget(Factory.Label(text=error_msg))
        else:
            preview.add_widget(widget)


class Preview(Factory.RelativeLayout):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_up(touch)


if __name__ == r'__main__':
    KvEditorApp().run()
