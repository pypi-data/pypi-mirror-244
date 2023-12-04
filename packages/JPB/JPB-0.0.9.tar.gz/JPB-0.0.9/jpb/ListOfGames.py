import logging
import os
import time
import asyncio

from pyautogui import press
from jpb.settings import fipath
from jpb.search import process
# from dPresence import pack3v, pack4v, pack5v, pack6v, pack7v, pack8v, pack9v, pack10v

process = process()

dictation = {'св': 'Это Смертельная Вечеринка',  # Создаём словарь для названий игр
             'св2': 'Смертельная Вечеринка 2',
             'сх2': 'Смехлыст 2',
             'сх3': 'Смехлыст 3',
             'работа': 'За Работой',
             'колесо': 'Колесо Невероятных Масштабов',
             'бред3': 'Бредовуха 3',
             'дьявол': 'Дьяволы В деталях',
             'шпион': 'Нашшпионаж',
             'инт': 'Выжить в Интернете',
             'грхолст': 'Гражданский Холст',
             'голова': 'А Голову Ты Не Забыл? (5 пак)',
             'жмикн': 'Жми на Кнопку',
             'монстр': 'Монстр Ищет Монстра',
             'гладАРТ': 'ГладиАРТоры',
             'футКО': 'Футбол K.O.',
             'чемп': 'Панччемпионат',
             'подзем': 'Подземнения',
             'прерис': 'Преступление и Рисование',
             'рифмы': 'Город Злых Рифм',
             'FT': 'FixyText (10 пак)',
             'DDRM': 'DoDo Re Mi (10 пак)',
             'mp3': 'MP3-бред'
             }


class game:
    def __init__(self):
        self.св = None
        self.св2 = None
        self.сх2 = None
        self.сх3 = None
        self.работа = None
        self.колесо = None
        self.бред3 = None
        self.дьявол = None
        self.шпион = None
        self.инт = None
        self.грхолст = None
        self.голова = None
        self.жмикн = None
        self.монстр = None
        self.гладАРТ = None
        self.футКО = None
        self.чемп = None
        self.подзем = None
        self.прерис = None
        self.рифмы = None
        self.FT = None
        self.DDRM = None
        self.mp3 = None

    def info(self, gpath: str, paths: list[callable], name: str) -> tuple[str | None, str | None]:
        if gpath is None:
            logging.error('Missing argument for game path')
        elif paths is None:
            logging.error('Missing argument for image paths')
        elif name is None:
            logging.error('Missing argument for game name')
        elif name:
            print('db started')
        elif paths:
            pass
        return name, gpath

    def path(self, path: str, name: str | None) -> None:
        if path.endswith('Click_ListGames.png'):
            process.first(fipath + path)
        elif path.endswith('StartThis.png'):
            process.click(fipath + path)
        elif path.endswith('Play.png'):
            process.click(fipath + path)
        elif path.endswith('StartGame.png'):
            process.start(fipath + path)
        elif path.endswith('\\settings\\settings.png'):
            process.click(fipath + path)
        elif path.endswith('\\settings\\gameplay.png'):
            process.click(fipath + path)
        elif path.endswith(('\\settings\\controller.png', 'closeSettings.png')):
            process.clickf(fipath + path)
        elif path.endswith('turnController.png'):
            process.clickf(fipath + path)
        elif path.endswith('preEnd.png'):
            process.clickf(fipath + path)
            time.sleep(3)
            press('esc')
            time.sleep(2)
            press('esc')
            time.sleep(0.5)
            press('down')
            time.sleep(0.5)
            press('enter')
            time.sleep(0.2)
            press('enter')
        elif path.endswith('endGame.png'):
            time.sleep(2)
            process.off(fipath + path, name)
        elif path.endswith('endsGame.png'):
            process.waitfor(fipath + path)
            process.off(fipath + path, name)
        elif path.endswith('settings\\musics.png'):
            process.waitform(fipath + path)
            process.click(fipath + path)
        elif path.endswith('settings\\topics.png'):
            process.waitform(fipath + path)
            process.click(fipath + path)

    def get(self, name):
        if name == 'св':
            gpath = r'The Jackbox\\Party Pack 3'
            name = 'The Jackbox Party Pack 3'
            self.св = self.info(name='The Jackbox Party Pack 3',
                                gpath=r'The Jackbox Party Pack 3',
                                paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                       self.path(path=f'Jackbox3\\Click_ListGames.png', name=name),
                                       self.path(path=f'Jackbox3\\sv\\StartThis.png', name=name),
                                       self.path(path=f'Jackbox3\\sv\\Play.png', name=name),
                                       self.path(path=f'Jackbox3\\sv\\StartGame.png', name=name),
                                       self.path(path=f'Jackbox3\\sv\\endGame.png', name=name)

                                       ])

        elif name == 'св2':
            gpath = r'The Jackbox\\Party Pack 6'
            name = 'The Jackbox Party Pack 6'
            return {"св2": self.info(name='The Jackbox Party Pack 6',
                                 gpath=r'The Jackbox Party Pack 6',
                                 paths=[time.sleep(2),
                                        os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                        self.path(path=f'Jackbox6\\Click_ListGames.png', name=name),
                                        self.path(path=f'Jackbox6\\sv2\\StartThis.png', name=name),
                                        self.path(path=f'Jackbox6\\sv2\\Play.png', name=name),
                                        self.path(path=f'Jackbox6\\sv2\\StartGame.png', name=name),
                                        self.path(path=f'Jackbox6\\sv2\\endsGame.png', name=name),
                                        self.path(path=f'Jackbox6\\sv2\\endGame.png', name=name)

                                        ])}
        elif name == 'сх2':
            gpath = r'The Jackbox\\Party Pack 3'
            name = 'The Jackbox Party Pack 3'
            self.сх2 = self.info(name='The Jackbox Party Pack 3',
                                 gpath=r'The Jackbox Party Pack 3',
                                 paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                        self.path(path=f'Jackbox3\\Click_ListGames.png', name=name),
                                        self.path(path=f'Jackbox3\\cx2\\StartThis.png', name=name),
                                        self.path(path=f'Jackbox3\\cx2\\Play.png', name=name),
                                        self.path(path=f'Jackbox3\\cx2\\StartGame.png', name=name),
                                        self.path(path=f'Jackbox3\\cx2\\endGame.png', name=name)

                                        ])
        elif name == 'сх3':
            gpath = r'The Jackbox\\Party Pack 7'
            name = 'The Jackbox Party Pack 7'
            self.сх3 = self.info(name='The Jackbox Party Pack 7',
                                 gpath=r'The Jackbox Party Pack 7',
                                 paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                        self.path(path=f'Jackbox7\\Click_ListGames.png', name=name),
                                        self.path(path=f'Jackbox7\\cx3\\StartThis.png', name=name),
                                        self.path(path=f'Jackbox7\\cx3\\Play.png', name=name),
                                        self.path(path=f'Jackbox7\\cx3\\StartGame.png', name=name),
                                        self.path(path=f'Jackbox7\\cx3\\endGame.png', name=name)

                                        ])
        elif name == 'работа':
            gpath = r'The Jackbox\\Party Pack 8'
            name = 'The Jackbox Party Pack 8'
            self.работа = self.info(name='The Jackbox Party Pack 8',
                                    gpath=r'The Jackbox Party Pack 8',
                                    paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                           self.path(path=f'Jackbox8\\Click_ListGames.png', name=name),
                                           self.path(path=f'Jackbox8\\rabota\\StartThis.png', name=name),
                                           self.path(path=f'Jackbox8\\rabota\\Play.png', name=name),
                                           self.path(path=f'Jackbox8\\rabota\\StartGame.png', name=name),
                                           self.path(path=f'Jackbox8\\rabota\\endGame.png', name=name)

                                           ])
        elif name == 'колесо':
            gpath = r'The Jackbox\\Party Pack 8'
            name = 'The Jackbox Party Pack 8'
            self.колесо = self.info(name='The Jackbox Party Pack 8',
                                    gpath=r'The Jackbox Party Pack 8',
                                    paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                           self.path(path=f'Jackbox8\\Click_ListGames.png', name=name),
                                           self.path(path=f'Jackbox8\\koleco\\StartThis.png', name=name),
                                           self.path(path=f'Jackbox8\\koleco\\Play.png', name=name),
                                           self.path(path=f'Jackbox8\\koleco\\StartGame.png', name=name),
                                           self.path(path=f'Jackbox8\\koleco\\endGame.png', name=name)

                                           ])
        elif name == 'бред3':
            gpath = r'The Jackbox\\Party Pack 4'
            name = 'The Jackbox Party Pack 4'
            self.бред3 = self.info(name='The Jackbox Party Pack 4',
                                   gpath=r'The Jackbox Party Pack 4',
                                   paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                          self.path(path=f'Jackbox4\\Click_ListGames.png', name=name),
                                          self.path(path=f'Jackbox4\\bred3\\StartThis.png', name=name),
                                          self.path(path=f'Jackbox4\\bred3\\Play.png', name=name),
                                          self.path(path=f'Jackbox4\\bred3\\StartGame.png', name=name),
                                          self.path(path=f'Jackbox4\\bred3\\endGame.png', name=name)

                                          ])
        elif name == 'дьявол':
            gpath = r'The Jackbox\\Party Pack 7'
            name = 'The Jackbox Party Pack 7'
            self.дьявол = self.info(name='The Jackbox Party Pack 7',
                                    gpath=r'The Jackbox Party Pack 7',
                                    paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                           self.path(path=f'Jackbox7\\Click_ListGames.png', name=name),
                                           self.path(path=f'Jackbox7\\devils\\StartThis.png', name=name),
                                           self.path(path=f'Jackbox7\\devils\\Play.png', name=name),
                                           self.path(path=f'Jackbox7\\devils\\StartGame.png', name=name),
                                           self.path(path=f'Jackbox7\\devils\\endGame.png', name=name)

                                           ])
        elif name == 'шпион':
            gpath = r'The Jackbox\\Party Pack 3'
            name = 'The Jackbox Party Pack 3'
            self.шпион = self.info(name='The Jackbox Party Pack 3',
                                   gpath=r'The Jackbox Party Pack 3',
                                   paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                          self.path(path=f'Jackbox3\\Click_ListGames.png', name=name),
                                          self.path(path=f'Jackbox3\\zhpion\\StartThis.png', name=name),
                                          self.path(path=f'Jackbox3\\zhpion\\Play.png', name=name),
                                          self.path(path=f'Jackbox3\\zhpion\\StartGame.png', name=name),
                                          self.path(path=f'Jackbox3\\zhpion\\endGame.png', name=name)

                                          ])
        elif name == 'интер':
            gpath = r'The Jackbox\\Party Pack 4'
            name = 'The Jackbox Party Pack 4'
            self.инт = self.info(name='The Jackbox Party Pack 4',
                                 gpath=r'The Jackbox Party Pack 4',
                                 paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                        self.path(path=f'Jackbox4\\Click_ListGames.png', name=name),
                                        self.path(path=f'Jackbox4\\inter\\StartThis.png', name=name),
                                        self.path(path=f'Jackbox4\\inter\\Play.png', name=name),
                                        self.path(path=f'Jackbox4\\inter\\StartGame.png', name=name),
                                        self.path(path=f'Jackbox4\\inter\\endGame.png', name=name)

                                        ])
        elif name == 'грхолст':
            gpath = r'The Jackbox\\Party Pack 4'
            name = 'The Jackbox Party Pack 4'
            self.грхолст = self.info(name='The Jackbox Party Pack 4',
                                     gpath=r'The Jackbox Party Pack 4',
                                     paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                            self.path(path=f'Jackbox4\\Click_ListGames.png', name=name),
                                            self.path(path=f'Jackbox4\\grholst\\StartThis.png', name=name),
                                            self.path(path=f'Jackbox4\\grholst\\Play.png', name=name),
                                            self.path(path=f'Jackbox4\\grholst\\StartGame.png', name=name),
                                            self.path(path=f'Jackbox4\\grholst\\endGame.png', name=name)

                                            ])
        elif name == 'голова':
            gpath = r'The Jackbox\\Party Pack 5'
            name = 'The Jackbox Party Pack 5'
            self.голова = self.info(name='The Jackbox Party Pack 5',
                                    gpath=r'The Jackbox Party Pack 5',
                                    paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                           self.path(path=f'Jackbox5\\Click_ListGames.png', name=name),
                                           self.path(path=f'Jackbox5\\golova\\StartThis.png', name=name),
                                           self.path(path=f'Jackbox5\\golova\\Play.png', name=name),
                                           self.path(path=f'Jackbox5\\golova\\StartGame.png', name=name),
                                           self.path(path=f'Jackbox5\\golova\\endGame.png', name=name)

                                           ])
        elif name == 'жмикн':
            gpath = r'The Jackbox\\Party Pack 6'
            name = 'The Jackbox Party Pack 6'
            self.жмикн = self.info(name='The Jackbox Party Pack 6',
                                   gpath=r'The Jackbox Party Pack 6',
                                   paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                          self.path(path=f'Jackbox6\\Click_ListGames.png', name=name),
                                          self.path(path=f'Jackbox6\\zhmikn\\StartThis.png', name=name),
                                          self.path(path=f'Jackbox6\\zhmikn\\Play.png', name=name),
                                          self.path(path=f'Jackbox6\\zhmikn\\StartGame.png', name=name),
                                          self.path(path=f'Jackbox6\\zhmikn\\endGame.png', name=name),
                                          self.path(path=f'Jackbox6\\zhmikn\\StartThis.png', name=name),

                                          ])
        elif name == 'монстр':
            gpath = r'The Jackbox\\Party Pack 4'
            name = 'The Jackbox Party Pack 4'
            self.монстр = self.info(name='The Jackbox Party Pack 4',
                                    gpath=r'The Jackbox Party Pack 4',
                                    paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                           self.path(path=f'Jackbox4\\Click_ListGames.png', name=name),
                                           self.path(path=f'Jackbox4\\monstr\\StartThis.png', name=name),
                                           self.path(path=f'Jackbox4\\monstr\\Play.png', name=name),
                                           self.path(path=f'Jackbox4\\monstr\\StartGame.png', name=name),
                                           self.path(path=f'Jackbox4\\monstr\\endGame.png', name=name)

                                           ])
        elif name == 'гладАРТ':
            gpath = r'The Jackbox\\Party Pack 7'
            name = 'The Jackbox Party Pack 7'
            self.гладАРТ = self.info(name='The Jackbox Party Pack 7',
                                     gpath=r'The Jackbox Party Pack 7',
                                     paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                            self.path(path=f'Jackbox7\\Click_ListGames.png', name=name),
                                            self.path(path=f'Jackbox7\\glART\\StartThis.png', name=name),
                                            self.path(path=f'Jackbox7\\glART\\Play.png', name=name),
                                            self.path(path=f'Jackbox7\\glART\\StartGame.png', name=name),
                                            self.path(path=f'Jackbox7\\glART\\endGame.png', name=name)

                                            ])
        elif name == 'футКО':
            gpath = r'The Jackbox\\Party Pack 3'
            name = 'The Jackbox Party Pack 3'
            self.футКО = self.info(name='The Jackbox Party Pack 3',
                                   gpath=r'The Jackbox Party Pack 3',
                                   paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                          self.path(path=f'Jackbox3\\Click_ListGames.png', name=name),
                                          self.path(path=f'Jackbox3\\fytbol\\StartThis.png', name=name),
                                          self.path(path=f'Jackbox3\\fytbol\\Play.png', name=name),
                                          self.path(path=f'Jackbox3\\fytbol\\StartGame.png', name=name),
                                          self.path(path=f'Jackbox3\\fytbol\\endGame.png', name=name)

                                          ])
        elif name == 'чемп':
            gpath = r'The Jackbox\\Party Pack 4'
            name = 'The Jackbox Party Pack 4'
            self.чемп = self.info(name='The Jackbox Party Pack 4',
                                  gpath=r'The Jackbox Party Pack 4',
                                  paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                         self.path(path=f'Jackbox4\\Click_ListGames.png', name=name),
                                         self.path(path=f'Jackbox4\\champ\\StartThis.png', name=name),
                                         self.path(path=f'Jackbox4\\champ\\Play.png', name=name),
                                         self.path(path=f'Jackbox4\\champ\\StartGame.png', name=name),
                                         self.path(path=f'Jackbox4\\champ\\endGame.png', name=name)

                                         ])
        elif name == 'подзем':
            gpath = r'The Jackbox\\Party Pack 8'
            name = 'The Jackbox Party Pack 8'
            self.подзем = self.info(name='The Jackbox Party Pack 8',
                                    gpath=r'The Jackbox Party Pack 8',
                                    paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                           self.path(path=f'Jackbox8\\Click_ListGames.png', name=name),
                                           self.path(path=f'Jackbox8\\podzem\\StartThis.png', name=name),
                                           self.path(path=f'Jackbox8\\podzem\\Play.png', name=name),
                                           self.path(path=f'Jackbox8\\podzem\\StartGame.png', name=name),
                                           self.path(path=f'Jackbox8\\podzem\\endGame.png', name=name)

                                           ])
        elif name == 'прерис':
            gpath = r'The Jackbox\\Party Pack 8'
            name = 'The Jackbox Party Pack 8'
            self.прерис = self.info(
                name='The Jackbox Party Pack 8',
                gpath=r'The Jackbox Party Pack 8',
                paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                       self.path(path=f'Jackbox5\\Click_ListGames.png', name=name),
                       self.path(path=f'Jackbox5\\preris\\StartThis.png', name=name),
                       self.path(path=f'Jackbox5\\preris\\Play.png', name=name),
                       self.path(path=f'Jackbox5\\preris\\StartGame.png', name=name),
                       self.path(path=f'Jackbox5\\preris\\endGame.png', name=name)

                       ])
        elif name == 'рифмы':
            gpath = r'The Jackbox\\Party Pack 5'
            name = 'The Jackbox Party Pack 5'
            self.рифмы = self.info(name='The Jackbox Party Pack 5',
                                   gpath=r'The Jackbox Party Pack 5',
                                   paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                          self.path(path=f'Jackbox5\\Click_ListGames.png', name=name),
                                          self.path(path=f'Jackbox5\\rifm\\StartThis.png', name=name),
                                          self.path(path=f'Jackbox5\\rifm\\Play.png', name=name),
                                          self.path(path=f'Jackbox5\\rifm\\StartGame.png', name=name),
                                          self.path(path=f'Jackbox5\\rifm\\endGame.png', name=name)

                                          ])
        #elif name == 'FT':
        #    gpath = r'The Jackbox\\Party Pack 10 Demo'
        #    name = 'The Jackbox Party Pack 10'
        #    self.FT = self.info(name='The Jackbox Party Pack 10 Demo',
        #                        gpath=r'The Jackbox Party Pack 10',
        #                        paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
        #                               self.path(path=f'Jackbox10\\Click_ListGames.png', name=name),
        #                               self.path(path=f'Jackbox10\\FT\\StartThis.png', name=name),
        #                               self.path(path=f'Jackbox10\\FT\\Play.png', name=name),
        #                               self.path(path=f'Jackbox10\\FT\\StartGame.png', name=name),
        #                               self.path(path=f'Jackbox10\\FT\\endGame.png', name=name)
        #
        #                               ])
        elif name == 'DDRM':
            gpath = r'The Jackbox\\Party Pack 10 Demo'
            name = 'The Jackbox Party Pack 10'
            self.DDRM = self.info(name='The Jackbox Party Pack 10',
                                  gpath=r'The Jackbox Party Pack 10',
                                  paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                         self.path(path=f'Jackbox10\\Click_ListGames.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\settings.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\gameplay.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\controller.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\closeSettings.png', name=name),
                                         self.path(path=f'Jackbox10\\DDRM\\StartThis.png', name=name),
                                         self.path(path=f'Jackbox10\\DDRM\\Play.png', name=name),
                                         self.path(path=f'Jackbox10\\DDRM\\preEnd.png', name=name),
                                         self.path(path=f'Jackbox10\\DDRM\\.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\settings.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\gameplay.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\turnController.png', name=name),
                                         self.path(path=f'Jackbox10\\settings\\closeSettings.png', name=name),
                                         self.path(path=f'Jackbox10\\DDRM\\endGame.png', name=name)

                                         ])

        elif name == 'mp3':
            gpath = r'The Jackbox\\Party Pack 23'
            name = 'The Jackbox Party Pack 2'
            self.mp3 = self.info(name='The Jackbox Party Pack 2',
                                 gpath=r'The Jackbox Party Pack 23',
                                 paths=[os.startfile(f"C:\\Games\\{gpath}\\{name}.lnk"),
                                        self.path(path=f'Jackbox2\\Click_ListGames.png', name=name),
                                        self.path(path=f'Jackbox2\\mp3\\StartThis.png', name=name),
                                        self.path(path=f'Jackbox2\\mp3\\settings\\musics.png', name=name),
                                        self.path(path=f'Jackbox2\\mp3\\settings\\topics.png', name=name),
                                        self.path(path=f'Jackbox2\\mp3\\endGame.png', name=name)

                                        ])
