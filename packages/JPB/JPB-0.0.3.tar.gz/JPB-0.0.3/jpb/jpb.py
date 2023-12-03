from jpb.components.ListOfGames import dictation, game

number = {'0': 'Смехлыст 2',
          '1': 'Смертельная Вечеринка 1',
          '2': 'Нашшпионаж',
          '3': 'Футбол K.O.',
          '4': 'Бредовуха 3',
          '5': 'Выжить в Интернете',
          '6': 'Монстр Ищет Монстра',
          '7': 'Панччемпионат',
          '8': 'Гражданский Холст',
          '9': 'А Голову Ты Не Забыл?',
          '10': 'Город Злых Рифм',
          '11': 'Раздели Комнату',
          '12': 'Город Злых Рифм',
          '13': 'Купол Зипол',
          '14': 'Творим Патенты',
          '15': 'Смертельная Вечеринка 2',
          '16': 'Корабль Смеха',
          '17': 'Словариум (БА)',
          '18': 'Жми На Кнопку',
          '19': 'Смехлыст 3',
          '20': 'Дьяволы в Деталях',
          '21': 'ГладиАРТоры',
          '22': 'На Пальцах',
          '23': 'Рисовач: Анимач (БА)',
          '24': 'Колесо Невероятных Масштабов',
          '25': 'За Работой',
          '26': 'Подземнения',
          '27': 'Преступление И Рисование',
          '28': 'Колесо Ненормального Троллинга (БА)',
          '29': 'Квартиранг (БА)',
          '30': 'Хламотопия (БА)',
          '31': 'Скоросорт  (БА)\n'
          }


translators = [
    "TJPP1",
    "TJPP2",
    "TJPP3",
    "TJPP4",
    "TJPP5",
    "TJPP6",
    "TJPP7",
    "TJPP8",
    "TJPP9",
    "TJPP10"

]


current_config = []


class setup:
    def __init__(self, translate: list[callable], disable_game: list[callable], discord_rpc: bool | None, server: bool | None):
        global current_config
        if translate:
            current_config = translate
            print('Переводы, которые будут использованы для автоматизации:')
            for i in current_config:
                print(i)
        elif disable_game:
            if disable_game in translate:
                translate.remove(disable_game)
            pass
        elif discord_rpc:
            pass
        elif server:
            try:
               # from flask import Flask, send_file
               # app = Flask(__name__)

               # @app.route('/')
               # def home():
               #     return (str(GPUtil.getGPUs()[0]) + "\n" +
               #             str(round(GPUtil.getGPUs()[0].temperature)) + "\n" +
               #             str(round(GPUtil.getGPUs()[0].load * 100)))


               # app.run(host=self.get_ip(), port=5000)
                pass
            except ImportError as IE:
                print("Модуль flask не установлен, установите его через \"pip install flask\"\n в командной строке",
                      IE)
        try:
            pass
        finally:
            cmd = input('Чтобы запустить автоматизацию напиши \'start\' здесь: ')
            if cmd.startswith('start'):
                print("\n" +
                      '  ___________________________________________________________________________\n' +
                      '||   [0] - Смехлыст 2\n' +
                      '||   [1] - Смертельная Вечеринка 1\n' +
                      '||   [2] - Нашшпионаж\n' +
                      '||   [3] - Футбол K.O.\n' +
                      '||   [4] - Бредовуха 3\n' +
                      '||   [5] - Выжить в Интернете\n' +
                      '||   [6] - Монстр Ищет Монстра\n' +
                      '||   [7] - Панччемпионат\n' +
                      '||   [8] - Гражданский Холст\n' +
                      '||   [9] - А Голову Ты Не Забыл?\n' +
                      '||  [10] - Город Злых Рифм\n' +
                      '||  [11] - Раздели Комнату\n' +
                      '||  [12] - Город Злых Рифм\n' +
                      '||  [13] - Купол Зипол\n' +
                      '||  [14] - Творим Патенты\n' +
                      '||  [15] - Смертельная Вечеринка 2\n' +
                      '||  [16] - Корабль Смеха\n' +
                      '||  [17] - Словариум (БА)\n' +
                      '||  [18] - Жми На Кнопку\n' +
                      '||  [19] - Смехлыст 3\n' +
                      '||  [20] - Дьяволы в Деталях\n' +
                      '||  [21] - ГладиАРТоры\n' +
                      '||  [22] - На Пальцах\n' +
                      '||  [23] - Рисовач: Анимач (БА)\n' +
                      '||  [24] - Колесо Невероятных Масштабов\n' +
                      '||  [25] - За Работой\n' +
                      '||  [26] - Подземнения\n' +
                      '||  [27] - Преступление И Рисование\n' +
                      '||  [28] - Колесо Ненормального Троллинга (БА)\n' +
                      '||  [29] - Квартиранг (БА)\n' +
                      '||  [30] - Хламотопия (БА)\n' +
                      '||  [31] - Скоросорт  (БА)\n'

                      )
                cmd2 = input('Напишите цифру игры, которую хотите запустить: ')
                if str(cmd2) in number.keys():
                    game1 = number.get(str(cmd2))
                    next_tolist = next(key for key, value in dictation.items() if value == str(game1))
                    game().get(next_tolist)

    class TJPP1:
        def whatif(self, версия_перевода: int | float):
            return f"JPP1whatif_{версия_перевода}"
            pass

    class TJPP2:
        def whatif(self, версия_перевода: int | float):
            return f"JPP2whatif_{версия_перевода}"
            pass

    class TJPP3:
        def whatif(self, версия_перевода: int | float | str):
            return f"JPP3whatif_{версия_перевода}"
            pass

    class TJPP4:
        def whatif(self, версия_перевода: int | float | str):
            return f"JPP4whatif_{версия_перевода}"
            pass

    class TJPP5:
        def whatif(self, версия_перевода: int | float | str):
            return f"JPP5whatif_{версия_перевода}"
            pass

    class TJPP6:
        def whatif(self, версия_перевода: int | float):
            return f"JPP6whatif_{версия_перевода}"
            pass

    class TJPP7:
        def whatif(self, версия_перевода: int | float):
            return f"JPP7whatif_{версия_перевода}"
            pass

        def tdot(self, версия_перевода: int | float):
            return f"JPP4tdot_{версия_перевода}"
            pass

    class TJPP8:
        def whatif(self, версия_перевода: int | float | str):
            return f"JPP8whatif_{версия_перевода}"
            pass

        def tdot(self, версия_перевода: int | float):
            return f"JPP8tdot_{версия_перевода}"
            pass

    class TJPP9:
        def whatif(self, версия_перевода: int | float):
            return f"JPP9whatif_{версия_перевода}"
            pass

        def tdot(self, версия_перевода: int | float):
            return f"JPP9tdot_{версия_перевода}"
            pass

        def thebox(self, версия_перевода: int | float):
            return f"JPP9thebox_{версия_перевода}"
            pass

    class TJPP10:
        def loamf(self, версия_перевода: int | float):
            return f"JPP10loamf_{версия_перевода}"
            pass

    def get_ip(self):
        """Получаем локальный IP-адрес, чтобы другие устрйоства могли присоединиться через лоакльный IP компьютера"""
        import socket

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
