import datetime
import sounddevice as sd
from kivy.uix.checkbox import CheckBox
from kivymd.uix.bottomsheet import MDListBottomSheet
import shutil
from scipy.io.wavfile import write
import pandas as pd
import numpy as np
import pytz
import requests
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivymd.icon_definitions import md_icons
from kivy.clock import Clock
from kivy.graphics.opengl import *
from kivy.graphics import *
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivymd.uix.button import MDFlatButton
from kivy.uix.textinput import TextInput
import threading
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
import os,threading,time
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.behaviors import ButtonBehavior

class ImageButton(ButtonBehavior, Image):
    pass

class MainWindow(BoxLayout):
    pass
class HelpWindow(BoxLayout):
    pass
class PopupWarning(BoxLayout):
    label_of_emergency = ObjectProperty(None)
class AudioRecWindow(BoxLayout):
    micbutton = ObjectProperty(None)
class ContentNavigationDrawer(BoxLayout):
    pass
class InternalStorageWindow(BoxLayout):
    pass
class TeamWindow(BoxLayout):
    pass
class FileLoader(BoxLayout):
    filechooser = ObjectProperty(None)
class uiApp(MDApp):
    dialog = None
    def build(self):
        self.theme_cls.primary_palette = "Pink"

        self.theme_cls.theme_style = "Dark"  # "Light"


        self.screen_manager = ScreenManager()
        self.mainscreen = MainWindow()
        screen = Screen(name='mainscreen')
        screen.add_widget(self.mainscreen)
        self.screen_manager.add_widget(screen)

        self.recscreen = AudioRecWindow()
        screen = Screen(name='recscreen')
        screen.add_widget(self.recscreen)
        self.screen_manager.add_widget(screen)

        self.internalstoragescreen = InternalStorageWindow()
        screen = Screen(name='internalstoragescreen')
        screen.add_widget(self.internalstoragescreen)
        self.screen_manager.add_widget(screen)

        self.helpscreen = HelpWindow()
        screen = Screen(name='helpscreen')
        screen.add_widget(self.helpscreen)
        self.screen_manager.add_widget(screen)

        self.fileloaderscreen = FileLoader()
        screen = Screen(name='fileloaderscreen')
        screen.add_widget(self.fileloaderscreen)
        self.screen_manager.add_widget(screen)

        self.teamscreen = TeamWindow()
        screen = Screen(name='teamscreen')
        screen.add_widget(self.teamscreen)
        self.screen_manager.add_widget(screen)

        self.popupwarningscreen = PopupWarning()
        screen = Screen(name='popupwarningscreen')
        screen.add_widget(self.popupwarningscreen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager
    def thread_for_rec(self):
        if self.recscreen.micbutton.source == "resources/icons/micon.png":
            fs = 44100  # Sample rate
            seconds = 10  # Duration of recording
            print('rec started')
            self.myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)

            sd.wait()  # Wait until recording is finished
            if self.externally_stopped == True:
                pass
            else:
                write('recorded.wav', fs, self.myrecording)  # Save as WAV file in 16-bit format
                toast("Finished")
                self.filename = "recorded.wav"
                #self.recscreen.micbutton.source = "resources/icons/micoff.png"

    def show_popup(self,text):
        show = PopupWarning()
        show.label_of_emergency.text = text
        self.popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(400, 400))

        self.popupWindow.open()
    def close_popup(self):
        self.popupWindow.dismiss()
    def process_the_sound(self):
        from modelloader import process_file
        from svm_based_model.model_loader_and_predict import svm_process

        output1 = svm_process(self.filename)  # it will process file in svm-model

        print("model 1")
        print(output1)
        

        output2 = process_file(self.filename)               # it will process file in multilayer perceptron model

        print("model 2")
        print(output2)
        if output1== True and output2 == True:
            pass
            # call emergency funtion with higher risk currently we haven;t implemented emergency function
            text = "[size=30]Risk is [color=#FF0000]high[/color] calling \nemergency function[/size]"
            self.show_popup(text)
        elif output1 == True or output2 == True:
            # call emergency function
            text = "[size=30]Risk is [color=#008000]Medium[/color] calling \nemergency function[/size]"
            self.show_popup(text)
            pass
        else:
            toast("you are safe")

    def mic_clicked(self):
        if self.recscreen.micbutton.source == "resources/icons/micoff.png":     #Turn mic on
            self.recscreen.micbutton.source = "resources/icons/micon.png"

            self.externally_stopped = False
            toast("started")
            th = threading.Thread(target=self.thread_for_rec())
            th.start()

        else:
            try:
                sd.stop()
                self.externally_stopped = True
                fs = 44100  # Sample rate
                write('recorded.wav', fs, self.myrecording)  # Save as WAV file in 16-bit format
                self.filename = "recorded.wav"
                toast("stopped")
            except:
                print("hello")
            self.recscreen.micbutton.source = "resources/icons/micoff.png"
    def loadfile(self,path,selection):

        #print(selection)
        self.filename = str(selection[0])
        self.fileloaderscreen_to_internalstoragescreen()
    def internalstoragescreen_to_mainscreen(self):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'mainscreen'
    def mainscreen_to_internalstoragescreen(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'internalstoragescreen'
    def mainscreen_to_recscreen(self):
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'recscreen'
    def recscreen_to_mainscreen(self):
        self.screen_manager.transition.direction = 'right'
        self.screen_manager.current = 'mainscreen'
    def internalstoragescreen_to_fileloader(self):
        self.screen_manager.transition.direction = 'up'
        self.screen_manager.current = 'fileloaderscreen'
    def fileloaderscreen_to_internalstoragescreen(self):
        self.screen_manager.transition.direction = 'down'
        self.screen_manager.current = 'internalstoragescreen'
    def mainscreen_to_helpscreen(self):
        self.screen_manager.transition.direction = 'down'
        self.screen_manager.current = 'helpscreen'
    def mainscreen_to_teamscreen(self):
        self.screen_manager.transition.direction = 'down'
        self.screen_manager.current = 'teamscreen'
    def backforcommonscreens(self):
        self.screen_manager.transition.direction = 'up'
        self.screen_manager.current = 'mainscreen'
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Engine is currently Running!!",
                buttons=[
                    MDFlatButton(
                        text="Ok", text_color=self.theme_cls.primary_color,on_press= lambda x: self.dialog.dismiss(),
                    )
                ],

            )
        self.dialog.open()
if __name__ == '__main__':
    LabelBase.register(name='second',fn_regular='FFF_Tusj.ttf')
    LabelBase.register(name='first',fn_regular='Pacifico.ttf')


    uiApp().run()