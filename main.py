from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivy.uix.image import Image
from random import randint

Window.size = (900, 700)

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    MDToolbar:
        id: toolbar
        title: 'Карточная игра "Дурак"'
        right_action_items: [['cogs', lambda x: app.setting()]]
    NavigationLayout:
        ScreenManager:
            id: scrm
            Screen:
                name: 'main'
                Image:
                    source: app.title_image
                MDFloatLayout:
                    padding: 10
                    spacing: 0
                    size_hint: [1, 1] 
                    AnchorLayout:
                        anchor_x: 'center'
                        anchor_y: 'bottom' 
                        padding: 0, 0, 0, 10                   
                        MDRaisedButton:
                            text: 'Играть'
                            on_press: app.begin_new_game()
                    AnchorLayout:
                        anchor_x: 'left'
                        anchor_y: 'bottom'
                        size_hint: .7, None
                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint: 1, None
                            padding: 10, 0, 0, 0
                            MDLabel:
                                size_hint: 1, 1
                                text: 'Общий счёт: '
                                halign: 'left'
                                valign: 'bottom'
                                
                            MDLabel:
                                id: player_wins_info
                                size_hint: 1, 1
                                text: 'Игрок - '
                                halign: 'left'
                                valign: 'bottom'
                            MDLabel:
                                id: comp_wins_info
                                size_hint: 1, 1
                                text: 'Компьютер - '
                                halign: 'left'
                                valign: 'bottom'                      
                      
            MDScreen:
                name: 'game'   
                FitImage:
                    source: app.fon           
                MDFloatLayout:
                    orientation: 'vertical'
                    size_hint: [1, 1]
                    spacing: 5
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: 10, 10, 10, 100 
                        size_hint: [1, 1]
                        MDBoxLayout:
                            orientation: 'vertical'
                            padding: 0, 0, 0, 0
                            ScrollView:
                                do_scroll_x: True
                                do_scroll_y: False
                                GridLayout:
                                    id: comp_karti
                                    size_hint: [1, .6]
                                    rows: 1
                                    padding: 0, 0, 0, 0
                                    
                            MDBoxLayout:
                                orientation: 'horizontal'
                                size_hint: [1, 1]         
                                padding: 0, -15, 0, 0                   
                                AnchorLayout:
                                    spacing: 3
                                    anchor_x: 'left'
                                    anchor_y: 'center'
                                    MDBoxLayout:
                                        orientation: 'vertical'
                                        padding: 0, -50, 0, 0
                                        GridLayout:
                                            id: table_comp
                                            padding: 0, 0, 0, 0
                                            size_hint: [.98, 1]
                                            pos_hint: {'left': 1}
                                            cols: 6
                                        GridLayout:
                                            id: table_player
                                            padding: 0, 0, 0, 0
                                            size_hint: [.98, 1]
                                            cols: 6
                                AnchorLayout:
                                    spacing: 3
                                    anchor_x: 'right' 
                                    anchor_y: 'center'  
                                    size_hint: [1, 1]                         
                                    MDBoxLayout:
                                        orientation: 'vertical'
                                        spacing: 5
                                        padding: 0, 0, 0, 0
                                        size_hint: [None, 1]
                                        AnchorLayout:
                                            id: koloda 
                                            size_hint: [None,1]   
                                            anchor_x: 'left' 
                                            anchor_y: 'top'
                                            MDBoxLayout:
                                                orientation: 'vertical'
                                                id: kosir
                                                size_hint: [None,None] 
                                            MDBoxLayout:
                                                orientation: 'vertical'
                                                id: koloda_image    
                            
                            ScrollView:
                                id: scroll_igrok
                                do_scroll_y: False                                
                                GridLayout:
                                    id: igrok_karti
                                    size_hint: [1, .85]
                                    padding: 0, 10, 0, 0
                                    rows: 1
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        AnchorLayout:
                            spacing: 3
                            anchor_x: 'left'
                            anchor_y: 'top'
                            size_hint: [1, None]
                            padding: 3
                            MDRaisedButton:
                                id: button_otboi
                                text: 'Отбой'
                                disabled: True
                                on_press: app.otboi_button()
                        AnchorLayout:
                            spacing: 3
                            anchor_x: 'center'
                            anchor_y: 'top'
                            size_hint: [1, None]
                            padding: 3
                            MDRaisedButton:
                                id: ok_button
                                text: 'Ок'
                                disabled: True
                                on_press: app.ok_button()
                        AnchorLayout:
                            spacing: 3
                            anchor_x: 'right'
                            anchor_y: 'top'
                            size_hint: [1, None]
                            padding: 3
                            MDRaisedButton:
                                id: vzyat_button
                                text: 'Беру'
                                disabled: True
                                on_press: 
                                    app.play_sound('vzyat')
                                    app.player_take_table_cards()
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        AnchorLayout:
                            spacing: 3
                            anchor_x: 'left'
                            anchor_y: 'bottom'
                            size_hint: [1, None]
                            padding: 10, 10, 10, -50 
                            
                            MDLabel:
                                id: info
                                text: 'info'
                                valign: 'bottom'
                                theme_text_color: 'Custom'
                                text_color: 1, 1, 1, 1
                            
                        AnchorLayout:
                            spacing: 3
                            anchor_x: 'right'
                            anchor_y: 'bottom'
                            size_hint: [1, None]
                            padding: 3
                            MDRaisedButton:
                                size_hint: [None, None]
                                id: button_razdacha
                                text: 'Раздать карты'
                                on_press: app.razdat_karti()        
                        
                    
            Screen:
                name: 'settings'
                MDBoxLayout:
                    size_hint: [1, 1]
                    orientation: 'vertical'
                    padding: 10
                    spacing: 10    
                    MDGridLayout:
                        size_hint: [1, None]
                        adaptive_height: True
                        cols: 3
                        MDLabel:
                            text: 'Громкость звуков'
                        MDSlider:
                            min: 0
                            max: 100
                            value: 70
                            step: 1
                            hint: False
                            show_off: False
                            on_value: 
                                app.set_sound_volume(int(self.value))
                                sound_volume_value.text = str(int(self.value))                                
                        MDLabel:
                            id: sound_volume_value
                            text: '70'  
                        MDLabel:
                            text: 'Громкость музыки'
                        MDSlider:
                            min: 0
                            max: 100
                            value: 30
                            step: 1
                            hint: False
                            show_off: False
                            on_value: 
                                app.set_music_volume(int(self.value))
                                music_volume_value.text = str(int(self.value))                                
                        MDLabel:
                            id: music_volume_value
                            text: '50' 
                    
                    MDGridLayout:
                        cols: 3
                        MDLabel:
                            text: 'Цветовая схема'                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            MDSlider:
                                min: 1
                                max: 18
                                value: 1
                                step: 1
                                hint: False
                                show_off: False
                                on_value: app.set_primary_palette(self.value)
                        MDLabel:
                            id: lbl_primary_palette 
                            text: 'Синий'
                    
                        MDLabel:
                            text: 'Насыщенность цвета'
                            
                        MDBoxLayout:
                            orientation: 'horizontal'
                            MDSlider:
                                min: 0
                                max: 13
                                value: 12
                                step: 1
                                hint: False
                                show_off: False
                                on_value: app.set_primary_hue(self.value)
                        MDLabel:
                            id: lbl_primary_hue 
                            text: '800'
                        MDRaisedButton:
                            size_hint: [None, None]
                            text: 'Сбросить счётчик побед'
                            on_press: app.reset_wins()
                        
                        MDRaisedButton:
                            size_hint: [None, None]
                            text: 'Правила игры'
                            on_press: app.pravila()
                        
                    MDRectangleFlatButton:
                        text: 'Ок'   
                        on_press: app.quit_setting()
                        
            Screen:
                name: 'pravila'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: 10
                    ScrollView:
                        padding: 30
                        MDLabel:
                            id: pravila
                            text_size: self.width, None
                            size_hint: 1, None
                            height: self.texture_size[1]
                MDBoxLayout:
                    size_hint: [1, 1]
                    orientation: 'horizontal'
                    padding: 10
                    spacing: 10                
                    MDRectangleFlatButton:
                        text: 'Ок'   
                        on_press: 
                            app.play_sound('ok')
                            scrm.current = 'settings'
'''


class ImageButton(ButtonBehavior, Image):
    def __init__(self, karta, **kwargs):
        super().__init__(**kwargs)
        self.karta = karta


new_koloda = []
masti = ['piki', 'kresti', 'bubi', 'chervi']
masti_rus = ['Пики', 'Трефы', 'Буби', 'Червы']
rangi = [6, 7, 8, 9, 10, 11, 12, 13, 14]
PLAYER = 'player'
COMP = 'comp'


class Karta:
    def __init__(self, mast, rang, image):
        self.mast = mast
        self.rang = rang
        self.image = image
        self.bita = False

def open_new_koloda():
    new_koloda.clear()
    for mast in masti:
        for rang in rangi:
            image = 'source/' + mast[0] + str(rang) + '.png'
            karta = Karta(mast, rang, image)
            new_koloda.append(karta)


class DurakApp(MDApp):
    fon = 'source/bg1.jpg'
    title_image = 'source/title.png'
    player_wins = 0
    comp_wins = 0
    sounds = []
    koloda = []
    igrok_karti = []
    comp_karti = []
    igrok_table = []
    comp_table = []
    otboi_count = 0
    kosir = ''
    turn = ''
    comp_take = False
    comp_otboi = False
    comp_ok = False
    player_take = False
    game = False
    otboi = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_wins()
        self.load_music()
        self.set_music_volume(30)
        self.play_music()
        self.load_sounds()
        self.set_sound_volume(70)
        self.screen = Builder.load_string(KV)

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '800'
        self.title = 'Карточная игра "Дурак"'
        self.update_wins_info()
        return self.screen

    def pravila(self):
        self.play_sound('pravila')
        try:
            file = open('pravila.txt', 'r')
            self.screen.ids.pravila.text = ''
            for line in file:
                #self.screen.ids.rules_lbl.text += line
                self.screen.ids.pravila.text += line
            file.close()
            self.screen.ids.scrm.current = 'pravila'
        except:
            Snackbar(text='Ошибка чтения файла').show()

    def load_music(self):
        try:
            self.music = SoundLoader.load('sounds/music.mp3')
            self.music.loop = True
        except:
            Snackbar(text='Ошибка загрузки музыки').show()

    def play_music(self):
        try:
            self.music.play()
        except:
            Snackbar(text='Ошибка загрузки музыки').show()

    def load_sounds(self):
        try:
            sound_start = SoundLoader.load('sounds/start.mp3')
            self.sounds.append(sound_start)
            sound_otboi = SoundLoader.load('sounds/otboi.mp3')
            self.sounds.append(sound_otboi)
            sound_vzyat = SoundLoader.load('sounds/vzyat.mp3')
            self.sounds.append(sound_vzyat)
            sound_ok = SoundLoader.load('sounds/ok.mp3')
            self.sounds.append(sound_ok)
            sound_test = SoundLoader.load('sounds/test_volume.mp3')
            self.sounds.append(sound_test)
            sound_razdacha = SoundLoader.load('sounds/razdacha.mp3')
            self.sounds.append(sound_razdacha)
            sound_pravila = SoundLoader.load('sounds/pravila.mp3')
            self.sounds.append(sound_pravila)
            sound_reset = SoundLoader.load('sounds/reset.mp3')
            self.sounds.append(sound_reset)
            sound_smeh = SoundLoader.load('sounds/smeh.mp3')
            self.sounds.append(sound_smeh)
            sound_settings = SoundLoader.load('sounds/settings.mp3')
            self.sounds.append(sound_settings)
            sound_draw = SoundLoader.load('sounds/draw.mp3')
            self.sounds.append(sound_draw)
            sound_koloda = SoundLoader.load('sounds/koloda.mp3')
            self.sounds.append(sound_koloda)
            sound_pluh = SoundLoader.load('sounds/pluh.mp3')
            self.sounds.append(sound_pluh)
            sound_worng = SoundLoader.load('sounds/wrong.mp3')
            self.sounds.append(sound_worng)
            sound_win = SoundLoader.load('sounds/win.mp3')
            self.sounds.append(sound_win)
            sound_pup = SoundLoader.load('sounds/pup.mp3')
            self.sounds.append(sound_pup)
            sound_sh = SoundLoader.load('sounds/sh.mp3')
            self.sounds.append(sound_sh)
            sound_pup2 = SoundLoader.load('sounds/pup2.mp3')
            self.sounds.append(sound_pup2)
        except:
            Snackbar(text='Ошибка загрузки звуков!').show()

    def play_sound(self, sound):
        try:
            if sound == 'start':
                self.sounds[0].play()
            elif sound == 'otboi':
                self.sounds[1].play()
            elif sound == 'vzyat':
                self.sounds[2].play()
            elif sound == 'ok':
                self.sounds[3].play()
            elif sound == 'test':
                self.sounds[4].play()
            elif sound == 'razdacha':
                self.sounds[5].play()
            elif sound == 'pravila':
                self.sounds[6].play()
            elif sound == 'reset':
                self.sounds[7].play()
            elif sound == 'smeh':
                self.sounds[8].play()
            elif sound == 'settings':
                self.sounds[9].play()
            elif sound == 'draw':
                self.sounds[10].play()
            elif sound == 'koloda':
                self.sounds[11].play()
            elif sound == 'pluh':
                self.sounds[12].play()
            elif sound == 'wrong':
                self.sounds[13].play()
            elif sound == 'win':
                self.sounds[14].play()
            elif sound == 'pup':
                self.sounds[15].play()
            elif sound == 'sh':
                self.sounds[16].play()
            elif sound == 'pup2':
                self.sounds[17].play()
        except:
            pass

    def set_primary_palette(self, value):
        self.play_sound('pup2')
        if value == 1:
            self.theme_cls.primary_palette = 'Blue'
            self.screen.ids.lbl_primary_palette.text = 'Синий'
        elif value == 2:
            self.theme_cls.primary_palette = 'Pink'
            self.screen.ids.lbl_primary_palette.text = 'Розовый'
        elif value == 3:
            self.theme_cls.primary_palette = 'Purple'
            self.screen.ids.lbl_primary_palette.text = 'Фиолетовый'
        elif value == 4:
            self.theme_cls.primary_palette = 'DeepPurple'
            self.screen.ids.lbl_primary_palette.text = 'Темно-фиолетовый'
        elif value == 5:
            self.theme_cls.primary_palette = 'Indigo'
            self.screen.ids.lbl_primary_palette.text = 'Индиго'
        elif value == 6:
            self.theme_cls.primary_palette = 'Red'
            self.screen.ids.lbl_primary_palette.text = 'Красный'
        elif value == 7:
            self.theme_cls.primary_palette = 'LightBlue'
            self.screen.ids.lbl_primary_palette.text = 'Светло-синий'
        elif value == 8:
            self.theme_cls.primary_palette = 'Cyan'
            self.screen.ids.lbl_primary_palette.text = 'Голубой'
        elif value == 9:
            self.theme_cls.primary_palette = 'Teal'
            self.screen.ids.lbl_primary_palette.text = 'Бирюзовый'
        elif value == 10:
            self.theme_cls.primary_palette = 'Green'
            self.screen.ids.lbl_primary_palette.text = 'Зеленый'
        elif value == 1:
            self.theme_cls.primary_palette = 'LightGreen'
            self.screen.ids.lbl_primary_palette.text = 'Светло-зеленый'
        elif value == 12:
            self.theme_cls.primary_palette = 'Yellow'
            self.screen.ids.lbl_primary_palette.text = 'Желтый'
        elif value == 13:
            self.theme_cls.primary_palette = 'Amber'
            self.screen.ids.lbl_primary_palette.text = 'Янтарный'
        elif value == 14:
            self.theme_cls.primary_palette = 'Orange'
            self.screen.ids.lbl_primary_palette.text = 'Оранжевый'
        elif value == 15:
            self.theme_cls.primary_palette = 'DeepOrange'
            self.screen.ids.lbl_primary_palette.text = 'Темно-оранжевый'
        elif value == 16:
            self.theme_cls.primary_palette = 'Brown'
            self.screen.ids.lbl_primary_palette.text = 'Коричневый'
        elif value == 17:
            self.theme_cls.primary_palette = 'Gray'
            self.screen.ids.lbl_primary_palette.text = 'Серый'
        elif value == 18:
            self.theme_cls.primary_palette = 'BlueGray'
            self.screen.ids.lbl_primary_palette.text = 'Серо-голубой'

    def set_primary_hue(self, value):
        self.play_sound('pup2')
        if value == 1:
            self.theme_cls.primary_hue = '50'
            self.screen.ids.lbl_primary_hue.text = '50'
        elif value == 2:
            self.theme_cls.primary_hue = '100'
            self.screen.ids.lbl_primary_hue.text = '100'
        elif value == 3:
            self.theme_cls.primary_hue = 'A100'
            self.screen.ids.lbl_primary_hue.text = 'A100'
        elif value == 4:
            self.theme_cls.primary_hue = '200'
            self.screen.ids.lbl_primary_hue.text = '200'
        elif value == 5:
            self.theme_cls.primary_hue = 'A200'
            self.screen.ids.lbl_primary_hue.text = 'A200'
        elif value == 6:
            self.theme_cls.primary_hue = '300'
            self.screen.ids.lbl_primary_hue.text = '300'
        elif value == 7:
            self.theme_cls.primary_hue = '400'
            self.screen.ids.lbl_primary_hue.text = '400'
        elif value == 8:
            self.theme_cls.primary_hue = 'A400'
            self.screen.ids.lbl_primary_hue.text = 'A400'
        elif value == 9:
            self.theme_cls.primary_hue = '500'
            self.screen.ids.lbl_primary_hue.text = '500'
        elif value == 10:
            self.theme_cls.primary_hue = '600'
            self.screen.ids.lbl_primary_hue.text = '600'
        elif value == 11:
            self.theme_cls.primary_hue = '700'
            self.screen.ids.lbl_primary_hue.text = '700'
        elif value == 12:
            self.theme_cls.primary_hue = '800'
            self.screen.ids.lbl_primary_hue.text = '800'
        elif value == 13:
            self.theme_cls.primary_hue = '900'
            self.screen.ids.lbl_primary_hue.text = '900'

    def set_sound_volume(self, value):
        try:
            for sound in self.sounds:
                sound.volume = float(value) / 100
            self.play_sound('test')
        except:
            pass

    def set_music_volume(self, value):
        try:
            self.music.volume = float(value) / 100
        except:
            pass

    def reset_wins(self):
        self.play_sound('reset')
        self.comp_wins = 0
        self.player_wins = 0
        self.write_file()
        self.update_wins_info()
        Snackbar(text='Счётчик побед сброшен').show()

    def get_wins(self):
        try:
            file = open('wins.txt', 'r')
            wins = []
            for line in file:
                wins.append(int(line))

            self.player_wins = wins[0]
            self.comp_wins = wins[1]
            file.close()
        except:
            Snackbar(text='Ошибка чтения файла').show()

    def begin_new_game(self):
        self.play_sound('start')
        open_new_koloda()
        self.clear_all_table()
        self.igrok_karti.clear()
        self.comp_karti.clear()
        self.peremeshat_kolodu()
        self.otboi_count = 0
        self.comp_take = False
        self.comp_otboi = False
        self.comp_ok = False
        self.player_take = False
        self.screen.ids.scrm.current = 'game'
        self.screen.ids.info.text = 'Начало игры'
        self.game = True
        self.otboi.clear()

    def clear_all_table(self):
        self.screen.ids.table_comp.clear_widgets()
        self.screen.ids.table_player.clear_widgets()
        self.screen.ids.koloda_image.clear_widgets()
        self.screen.ids.kosir.clear_widgets()
        self.screen.ids.comp_karti.clear_widgets()
        self.screen.ids.igrok_karti.clear_widgets()

    def begin_game(self):
        player = []
        comp = []
        for karta in self.comp_karti:
            if karta.mast == self.kosir:
                comp.append(karta)
        for karta in self.igrok_karti:
            if karta.mast == self.kosir:
                player.append(karta)
        if len(player) > 0 and len(comp) == 0:
            self.turn = PLAYER
        elif len(comp) > 0 and len(player) == 0:
            self.turn = COMP
        elif len(player) == 0 and len(comp) == 0:
            self.turn = PLAYER
        else:
            player.sort(key=lambda x: x.rang)
            comp.sort(key=lambda x: x.rang)
            if player[0].rang < comp[0].rang:
                self.turn = PLAYER
            else:
                self.turn = COMP

        self.clear_table()

        if self.turn == COMP:
            self.screen.ids.info.text = f'Ход компа'
            self.comp_turn()
        else:
            self.screen.ids.info.text = f'Ваш ход'
            self.player_turn()

    def peremeshat_kolodu(self):
        self.koloda.clear()
        temp = new_koloda.copy()
        for i in range(36):
            index = randint(0, len(temp) - 1)
            random_karta = temp[index]
            self.koloda.append(random_karta)
            temp.pop(index)

    def comp_turn(self):
        if not self.player_take:
            self.screen.ids.info.text = 'Ход компа'
        Clock.schedule_once(self.comp_action, .8)

    def comp_action(self, dt):
        if self.turn == PLAYER:
            for karta in self.igrok_table:
                if karta.bita:
                    continue
                if not self.comp_answer(karta):
                    self.comp_take_table_cards()
                    break
                else:
                    self.player_turn()
        else:
            self.comp_karti.sort(key=lambda x: x.rang)
            index = -1
            if self.check_to_win():
                return
            if self.player_take:

                if not len(self.comp_karti) == 0:
                    index = self.comp_podkid()

                while index >= 0:
                    self.comp_karti.pop(index)
                    index = self.comp_podkid()
                    self.comp_turn()
                    self.comp_ok = True

                if not self.comp_ok:
                    self.comp_ok = True
                    self.player_take_table_cards()
                    return
                else:
                    self.comp_ok = True
                    self.screen.ids.info.text = 'Комп подкинул еще карты. Нажмите "Беру"'
                    self.player_turn()
                    return
            elif len(self.comp_table) == 0:
                for i in range(len(self.comp_karti)):
                    if not self.comp_karti[i].mast == self.kosir:
                        index = i
                        self.screen.ids.table_comp.add_widget(Image(source=self.comp_karti[i].image))
                        self.play_sound('pluh')
                        self.screen.ids.table_player.add_widget(Image(source='source/nemo.png', opacity=0))
                        self.comp_table.append(self.comp_karti[i])
                        for widget in self.screen.ids.comp_karti.children:
                            #if widget.source == self.comp_karti[i].image:
                            if widget.source == 'source/s.png':
                                self.screen.ids.comp_karti.remove_widget(widget)
                                break
                        break
                    else:
                        continue
                if index == -1 and len(self.comp_karti) > 0:
                    index = 0
                    self.screen.ids.table_comp.add_widget(Image(source=self.comp_karti[0].image))
                    self.play_sound('pluh')
                    self.screen.ids.table_player.add_widget(Image(source='source/nemo.png', opacity=0))
                    self.comp_table.append(self.comp_karti[0])
                    for widget in self.screen.ids.comp_karti.children:
                        #if widget.source == self.comp_karti[0].image:
                        if widget.source == 'source/s.png':
                            self.screen.ids.comp_karti.remove_widget(widget)
                            break
            elif len(self.comp_table) > 0:
                if len(self.comp_karti) == 0:
                    self.screen.ids.info.text = 'У компа нет карт. Нажмите "Отбой"'
                    self.comp_otboi = True
                    self.player_turn()
                    return

                if len(self.igrok_karti) == 0:
                    self.screen.ids.info.text = 'Нажмите "Отбой"'
                    self.comp_otboi = True
                    self.player_turn()
                    return

                if len(self.comp_table) == 5 and self.otboi_count == 0:
                    self.screen.ids.info.text = 'Первый отбой 5 карт. Нажмите "Отбой"'
                    self.comp_otboi = True
                    self.player_turn()
                    return
                elif len(self.comp_table) == 6 and self.otboi_count > 0:
                    self.screen.ids.info.text = 'Вы успешно отбились. Нажмите "Отбой"'
                    self.comp_otboi = True
                    self.player_turn()
                    return

                index = self.comp_podkid()

            if not index == -1:
                self.comp_karti.pop(index)
            else:
                self.screen.ids.info.text = 'Нажмите "Отбой"'
                self.comp_otboi = True

            self.player_turn()

    def comp_give_kosir(self):
        index = -1
        for i in range(len(self.comp_karti)):
            karta = self.comp_karti[i]
            if karta.mast == self.kosir and self.check_comp_turn(karta):
                index = i
                self.screen.ids.table_comp.add_widget(Image(source=self.comp_karti[i].image))
                self.play_sound('pluh')
                self.screen.ids.table_player.add_widget(Image(source='source/nemo.png', opacity=0))
                self.comp_table.append(self.comp_karti[i])
                for widget in self.screen.ids.comp_karti.children:
                    #if widget.source == self.comp_karti[i].image:
                    if widget.source == 'source/s.png':
                        self.screen.ids.comp_karti.remove_widget(widget)
                        break
                break
        return index

    def comp_podkid(self):
        index = -1
        if len(self.koloda) < 12:
            index = self.comp_give_kosir()

        if index >= 0:
            return index

        for i in range(len(self.comp_karti)):
            karta = self.comp_karti[i]
            if not karta.mast == self.kosir and self.check_comp_turn(karta):
                index = i
                self.screen.ids.table_comp.add_widget(Image(source=self.comp_karti[i].image))
                self.play_sound('pluh')
                self.screen.ids.table_player.add_widget(Image(source='source/nemo.png', opacity=0))
                self.comp_table.append(self.comp_karti[i])
                for widget in self.screen.ids.comp_karti.children:
                    #if widget.source == self.comp_karti[i].image:
                    if widget.source == 'source/s.png':
                        self.screen.ids.comp_karti.remove_widget(widget)
                        break
                break
        return index

    def comp_answer(self, karta):
        bita = False
        comp_karta = None
        self.comp_karti.sort(key=lambda x: x.rang)
        for curr_karta in self.comp_karti:
            if curr_karta.mast == karta.mast and curr_karta.rang > karta.rang:
                bita = True
                comp_karta = curr_karta
                break

        if not bita and not karta.mast == self.kosir:
            for curr_karta in self.comp_karti:
                if not curr_karta.mast == self.kosir:
                    continue
                bita = True
                comp_karta = curr_karta
                break

        karta.bita = bita
        if not comp_karta == None:
            # self.screen.ids.table_comp.add_widget(Image(source=comp_karta.image))
            for widget in self.screen.ids.table_comp.children:
                if widget.source == 'source/nemo.png':
                    widget.source = comp_karta.image
                    self.play_sound('pluh')
                    widget.opacity = 1
                    break

            for widget in self.screen.ids.comp_karti.children:
                #if widget.source == comp_karta.image:
                if widget.source == 'source/s.png':
                    self.screen.ids.comp_karti.remove_widget(widget)
                    break
            index = -1
            for i in range(len(self.comp_karti)):
                if self.comp_karti[i].image == comp_karta.image:
                    index = i
                    break
            if index == -1:
                return
            self.comp_karti.pop(index)
            self.comp_table.append(comp_karta)
        return bita

    def comp_take_table_cards(self):
        self.screen.ids.info.text = 'Комп берёт карты. Подбросьте и(или) нажмите "Ок".'
        self.screen.ids.ok_button.disabled = False
        self.screen.ids.button_otboi.disabled = True
        self.comp_take = True
        self.player_turn()

    def player_take_card_from_table(self, dt):
        if len(self.comp_table) == 0 and len(self.igrok_table) == 0:
            Clock.unschedule(self.player_take_card_from_table)
            self.turn = COMP
            self.take_cards_in_game()
            # self.comp_turn()
        else:
            if not len(self.comp_table) == 0:
                karta = self.comp_table[0]
                self.igrok_karti.append(karta)
                button = ImageButton(karta, source=karta.image, disabled=True)
                button.bind(on_press=self.player_action)
                self.play_sound('pup')
                self.screen.ids.igrok_karti.add_widget(button)
                for widget in self.screen.ids.table_comp.children:
                    if widget.source == karta.image:
                        self.screen.ids.table_comp.remove_widget(widget)
                        break
                self.comp_table.pop(0)
            elif not len(self.igrok_table) == 0:
                karta = self.igrok_table[0]
                self.igrok_karti.append(karta)
                button = ImageButton(karta, source=karta.image, disabled=True)
                button.bind(on_press=self.player_action)
                self.play_sound('pup')
                self.screen.ids.igrok_karti.add_widget(button)
                for widget in self.screen.ids.table_player.children:
                    if widget.source == karta.image:
                        self.screen.ids.table_player.remove_widget(widget)
                        break
                self.igrok_table.pop(0)

    def comp_take_card_from_table(self, dt):
        if len(self.comp_table) == 0 and len(self.igrok_table) == 0:
            self.turn = PLAYER
            self.take_cards_in_game()
            #self.player_turn()
            Clock.unschedule(self.comp_take_card_from_table)
        else:
            if not len(self.comp_table) == 0:
                karta = self.comp_table[0]
                self.comp_karti.append(karta)
                self.play_sound('pup')
                self.screen.ids.comp_karti.add_widget(Image(source='source/s.png'))
                #self.screen.ids.comp_karti.add_widget(Image(source=karta.image))
                for widget in self.screen.ids.table_comp.children:
                    if widget.source == karta.image:
                        self.screen.ids.table_comp.remove_widget(widget)
                        break
                self.comp_table.pop(0)
            elif not len(self.igrok_table) == 0:
                karta = self.igrok_table[0]
                self.comp_karti.append(karta)
                self.play_sound('pup')
                self.screen.ids.comp_karti.add_widget(Image(source='source/s.png'))
                #self.screen.ids.comp_karti.add_widget(Image(source=karta.image))
                for widget in self.screen.ids.table_player.children:
                    if widget.source == karta.image:
                        self.screen.ids.table_player.remove_widget(widget)
                        break
                self.igrok_table.pop(0)

    def player_take_table_cards(self):
        #self.play_sound('vzyat')
        self.player_take = True
        self.screen.ids.vzyat_button.disabled = True
        if self.comp_ok:
            self.comp_ok = False
            Clock.schedule_interval(self.player_take_card_from_table, .7)
        else:
            self.screen.ids.info.text = 'Вы берете карты'
            self.comp_turn()

    def razdat_karti(self):
        self.play_sound('razdacha')
        if self.screen.ids.button_razdacha.text == 'На главную':
            self.screen.ids.scrm.current = 'main'
            self.screen.ids.button_razdacha.text = 'Раздать карты'
            return
        self.count = 0
        self.screen.ids.button_razdacha.disabled = True
        self.screen.ids.info.text = 'Раздача карт'
        Clock.schedule_interval(self.give_kart, .7)

    def give_kart(self, dt):
        if self.count < 12:
            self.play_sound('pup')
            index = len(self.koloda) - 1
            karta = self.koloda[index]

            if self.count % 2 == 0:
                self.comp_karti.append(karta)
                self.screen.ids.comp_karti.add_widget(Image(source='source/s.png'))
                #self.screen.ids.comp_karti.add_widget(Image(source=karta.image))
            else:
                self.igrok_karti.append(karta)
                button = ImageButton(karta, source=karta.image, disabled=True)
                button.bind(on_press=self.player_action)
                self.screen.ids.igrok_karti.add_widget(button)
            self.koloda.pop(index)
            self.count += 1
        else:
            self.kosir = self.koloda[0].mast
            for i in range(len(masti)):
                if masti[i] == self.kosir:
                    self.kosir_rus = masti_rus[i]
            self.play_sound('sh')
            self.play_sound('pup')
            self.screen.ids.kosir.add_widget(Image(source=self.koloda[0].image, size_hint=[None, 1]))
            # self.screen.ids.koloda.add_widget(Image(source='source/s2.png', size_hint=[None, 1]))

            button = ImageButton(None, source='source/s2.png', size_hint=[None, 1])
            button.bind(on_press=self.koloda_count_info)
            self.screen.ids.koloda_image.add_widget(button)
            self.begin_game()
            Clock.unschedule(self.give_kart)

    def koloda_count_info(self, instance):
        self.play_sound('koloda')
        Snackbar(text=f'В колоде осталось {len(self.koloda)} карт. Козырь - {self.kosir_rus}').show()

    def setting(self):
        self.play_sound('settings')
        self.screen.ids.scrm.current = 'settings'

    def quit_setting(self):
        self.play_sound('ok')
        if self.game:
            self.screen.ids.scrm.current = 'game'
        else:
            self.screen.ids.scrm.current = 'main'

    def player_turn(self):
        if self.player_take and self.comp_ok:
            self.screen.ids.vzyat_button.disabled = False
            self.disable_player_cards(True)
            return
        self.disable_player_cards(False)
        if not self.comp_take and not self.comp_otboi:
            self.screen.ids.info.text = 'Ваш ход'

        if self.turn == PLAYER and self.comp_take:
            if self.check_to_win():
                return
            return

        if self.comp_otboi:
            self.screen.ids.button_otboi.disabled = False
            if self.check_to_win():
                return
            self.disable_player_cards(True)
        elif self.turn == PLAYER and self.otboi_count == 0 and len(self.igrok_table) == 5:
            self.screen.ids.button_otboi.disabled = False
            if self.check_to_win():
                return
            self.disable_player_cards(True)
            self.screen.ids.info.text = 'Первый отбой 5 карт. Нажмите "Отбой".'
            self.screen.ids.button_otboi.disabled = False
        elif self.turn == PLAYER and self.otboi_count > 0 and len(self.igrok_table) == 6:
            self.screen.ids.button_otboi.disabled = False
            if self.check_to_win():
                return
            self.disable_player_cards(True)
            self.screen.ids.info.text = 'Комп успешно отбился. Нажмите "Отбой".'
        elif self.turn == PLAYER and len(self.comp_karti) == 0:
            self.screen.ids.info.text = 'У компа нету карт что б отбиваться. Нажмите "Отбой"'
            self.disable_player_cards(True)
            self.screen.ids.button_otboi.disabled = False
        elif self.turn == PLAYER and len(self.igrok_table) > 0:
            if self.check_to_win():
                return
            self.screen.ids.button_otboi.disabled = False
            self.screen.ids.info.text = 'Комп отбился. Можете подкинуть или нажмите "Отбой"'
        elif self.turn == COMP and len(self.comp_table) > 1:
            self.screen.ids.info.text = 'Комп подкинул карту. Отбивайтесь'
            self.screen.ids.vzyat_button.disabled = False
        elif self.turn == COMP and len(self.comp_table) == 1:
            self.screen.ids.info.text = 'Комп походил. Отбивайтесь'
            self.screen.ids.vzyat_button.disabled = False

    def player_action(self, instance):
        if self.turn == PLAYER:
            if len(self.igrok_karti) == 0:
                self.screen.ids.info.text = 'Вы выиграли!'
                return
            if len(self.igrok_table) == 0:
                self.screen.ids.table_player.add_widget(Image(source=instance.karta.image))
                self.play_sound('pluh')
                self.screen.ids.table_comp.add_widget(Image(source='source/nemo.png', opacity=0))
                self.screen.ids.igrok_karti.remove_widget(instance)
                index = -1
                for i in range(len(self.igrok_karti)):
                    if self.igrok_karti[i].image == instance.karta.image:
                        index = i
                        break
                if index == -1:
                    return
                self.igrok_karti.pop(index)
                self.igrok_table.append(instance.karta)
                self.disable_player_cards(True)
                self.screen.ids.button_otboi.disabled = True
                self.comp_turn()
            else:
                if self.check_player_turn(instance.karta):
                    self.screen.ids.table_player.add_widget(Image(source=instance.karta.image))
                    self.play_sound('pluh')
                    self.screen.ids.table_comp.add_widget(Image(source='source/nemo.png', opacity=0))
                    self.screen.ids.igrok_karti.remove_widget(instance)
                    index = -1
                    for i in range(len(self.igrok_karti)):
                        if self.igrok_karti[i].image == instance.karta.image:
                            index = i
                            break
                    if index == -1:
                        return
                    self.igrok_karti.pop(index)
                    self.igrok_table.append(instance.karta)
                    if not self.comp_take:
                        self.disable_player_cards(True)
                        self.screen.ids.button_otboi.disabled = True
                        self.comp_turn()
                else:
                    self.play_sound('wrong')
                    Snackbar(text='Вы не можете подкинуть эту карту').show()
        elif self.turn == COMP:
            for karta in self.comp_table:
                if karta.bita:
                    continue
                if instance.karta.mast == self.kosir and not karta.mast == self.kosir:
                    self.player_answer(instance)
                    karta.bita = True
                    break
                elif instance.karta.mast == karta.mast and instance.karta.rang > karta.rang:
                    self.player_answer(instance)
                    karta.bita = True
                    break
                else:
                    self.play_sound('wrong')
                    Snackbar(text='Вы не можете отбиться этой картой').show()

    def player_answer(self, instance):
        for widget in self.screen.ids.table_player.children:
            if widget.source == 'source/nemo.png':
                self.play_sound('pluh')
                widget.source = instance.karta.image
                widget.opacity = 1
                break
        # self.screen.ids.table_player.add_widget(Image(source=instance.karta.image))
        self.screen.ids.igrok_karti.remove_widget(instance)
        index = -1
        for i in range(len(self.igrok_karti)):
            if self.igrok_karti[i].image == instance.karta.image:
                index = i
                break
        if index == -1:
            return
        self.igrok_karti.pop(index)
        self.igrok_table.append(instance.karta)
        self.disable_player_cards(True)
        self.screen.ids.vzyat_button.disabled = True
        self.screen.ids.button_otboi.disabled = True
        self.comp_turn()

    def disable_player_cards(self, value):
        for widget in self.screen.ids.igrok_karti.children:
            widget.disabled = value

    def check_comp_turn(self, karta):
        for karta_in_table in self.igrok_table:
            if karta_in_table.rang == karta.rang:
                return True

        for karta_in_table in self.comp_table:
            if karta_in_table.rang == karta.rang:
                return True

        return False

    def check_player_turn(self, karta):
        for karta_in_table in self.igrok_table:
            if karta_in_table.rang == karta.rang:
                return True

        for karta_in_table in self.comp_table:
            if karta_in_table.rang == karta.rang:
                return True
        self.play_sound('wrong')
        Snackbar(text='Вы не можете подкинуть эту карту').show()
        return False

    def razdacha_in_game(self, dt):
        if self.turn == PLAYER and len(self.igrok_karti) < 6:
            if len(self.koloda) == 0:
                self.end_of_razdacha()
                Clock.unschedule(self.razdacha_in_game)
                return
            index = len(self.koloda) - 1
            karta = self.koloda[index]
            self.igrok_karti.append(karta)
            button = ImageButton(karta, source=karta.image, disabled=True)
            button.bind(on_press=self.player_action)
            self.play_sound('pup')
            self.screen.ids.igrok_karti.add_widget(button)
            #self.play_sound('sh')
            self.koloda.pop(index)
        elif self.turn == COMP and len(self.comp_karti) < 6:
            if len(self.koloda) == 0:
                self.end_of_razdacha()
                Clock.unschedule(self.razdacha_in_game)
                return
            index = len(self.koloda) - 1
            karta = self.koloda[index]
            self.comp_karti.append(karta)
            self.play_sound('pup')
            self.screen.ids.comp_karti.add_widget(Image(source='source/s.png'))
            #self.screen.ids.comp_karti.add_widget(Image(source=karta.image))
            self.koloda.pop(index)
        else:
            if len(self.igrok_karti) < 6:
                if len(self.koloda) == 0:
                    self.end_of_razdacha()
                    Clock.unschedule(self.razdacha_in_game)
                    return
                index = len(self.koloda) - 1
                karta = self.koloda[index]
                self.igrok_karti.append(karta)
                button = ImageButton(karta, source=karta.image, disabled=True)
                button.bind(on_press=self.player_action)
                self.play_sound('pup')
                self.screen.ids.igrok_karti.add_widget(button)
                #self.play_sound('sh')
                self.koloda.pop(index)
            elif len(self.comp_karti) < 6:
                if len(self.koloda) == 0:
                    self.end_of_razdacha()
                    Clock.unschedule(self.razdacha_in_game)
                    return
                index = len(self.koloda) - 1
                karta = self.koloda[index]
                self.comp_karti.append(karta)
                self.play_sound('pup')
                self.screen.ids.comp_karti.add_widget(Image(source='source/s.png'))
                #self.screen.ids.comp_karti.add_widget(Image(source=karta.image))
                self.koloda.pop(index)
            else:
                self.end_of_razdacha()
                Clock.unschedule(self.razdacha_in_game)

    def end_of_razdacha(self):
        if len(self.koloda) == 1:
            for widget in self.screen.ids.koloda_image.children:
                if widget.source == 'source/s2.png':
                    widget.source = 'source/s3.png'
                    break
        elif len(self.koloda) == 0:
            self.screen.ids.kosir.clear_widgets()
            for widget in self.screen.ids.koloda_image.children:
                if widget.source == 'source/s2.png':
                    widget.source = 'source/s3.png'
                    break
        for karta in self.igrok_karti:
            karta.bita = False
        for karta in self.comp_karti:
            karta.bita = False
        self.comp_table.clear()
        self.igrok_table.clear()
        if self.player_take:
            self.turn = COMP
        elif self.comp_take:
            self.turn = PLAYER
        else:
            if self.turn == COMP:
                self.turn = PLAYER
            else:
                self.turn = COMP
        self.comp_take = False
        self.comp_otboi = False
        self.player_take = False
        self.clear_table()
        if self.turn == PLAYER:
            self.player_turn()
        else:
            self.comp_turn()

    def take_cards_in_game(self):
        self.screen.ids.info.text = 'Раздача недостающих карт'
        Clock.schedule_interval(self.razdacha_in_game, .7)

    def ok_button(self):
        self.play_sound('ok')
        self.screen.ids.info.text = 'Комп забирает карты.'
        self.screen.ids.ok_button.disabled = True
        self.disable_player_cards(True)
        Clock.schedule_interval(self.comp_take_card_from_table, .7)

    def otboi_button(self):
        self.play_sound('otboi')
        for card in self.comp_table:
            self.otboi.append(card)
        for card in self.igrok_table:
            self.otboi.append(card)
        self.otboi_count += len(self.comp_table) + len(self.igrok_table)
        self.clear_table()
        self.take_cards_in_game()

    def clear_table(self):
        self.screen.ids.table_player.clear_widgets()
        self.screen.ids.table_comp.clear_widgets()
        self.igrok_table.clear()
        self.comp_table.clear()
        self.screen.ids.button_otboi.disabled = True
        self.screen.ids.info.text = 'Отбой'

    def write_file(self):
        try:
            file = open('wins.txt', 'w')
            file.write(str(self.player_wins) + '\n' + str(self.comp_wins))
            file.close()
        except:
            Snackbar(text='Ошибка записи файла').show()

    def update_wins_info(self):
        self.screen.ids.player_wins_info.text = f'Игрок - {self.player_wins}'
        self.screen.ids.comp_wins_info.text = f'Компьютер - {self.comp_wins}'

    def check_to_win(self):
        if len(self.koloda) == 0:
            self.otboi.sort(key=lambda x: x.mast, reverse=False)
            self.otboi.sort(key=lambda x: x.rang, reverse=False)
            count = 0
            if len(self.igrok_karti) == 0 and len(self.comp_karti) == 0:
                self.play_sound('draw')
                self.screen.ids.info.text = 'Ничья!'
                self.screen.ids.ok_button.disabled = True
                self.screen.ids.vzyat_button.disabled = True
                self.screen.ids.button_otboi.disabled = True
                self.screen.ids.button_razdacha.disabled = False
                self.screen.ids.button_razdacha.text = 'На главную'
                self.game = False
                return True
            elif len(self.igrok_karti) == 0:
                self.screen.ids.info.text = 'Вы выиграли!'
                self.play_sound('win')
                self.player_wins += 1
                self.write_file()
                self.update_wins_info()
                self.screen.ids.ok_button.disabled = True
                self.screen.ids.vzyat_button.disabled = True
                self.screen.ids.button_otboi.disabled = True
                self.screen.ids.button_razdacha.disabled = False
                self.screen.ids.button_razdacha.text = 'На главную'
                self.game = False
                return True
            elif len(self.comp_karti) == 0:
                self.play_sound('smeh')
                self.screen.ids.info.text = 'Комп выиграл.'
                self.comp_wins += 1
                self.write_file()
                self.update_wins_info()
                self.screen.ids.ok_button.disabled = True
                self.screen.ids.vzyat_button.disabled = True
                self.screen.ids.button_otboi.disabled = True
                self.screen.ids.button_razdacha.disabled = False
                self.screen.ids.button_razdacha.text = 'На главную'
                self.game = False
                return True
        return False


DurakApp().run()
