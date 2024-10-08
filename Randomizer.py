import random
from GameObjects import SpecialCondition as Sc
import SpecialConditions as Scs
from GameObjects import Biology, Occupation, Character, Health, Hobby, Phobia, Inventory, Fact, Catastrophe


def year_word(age: int):
    mod = age % 100
    if 5 <= mod <= 19:
        return 'лет'
    mod %= 10
    if mod == 0 or 5 <= mod <= 9:
        return "лет"
    if mod == 1:
        return 'год'
    return 'года'


occupations_safe_mode = "Агроном,Садовод,Фермер,Лесник,Системный администратор," \
                        "Военный,Офицер,Солдат,Инженер,Программист,Дизайнер," \
                        "Кондитер,Повар,Конструктор,Проектировщик,Строитель," \
                        "Терапевт,Официант,Художник,Танцор,Актёр,Музыкант,Режиссёр," \
                        "Учитель,Преподаватель,Психолог,Фельдшер,Стоматолог," \
                        "Ветеринар,Хирург,Библиотекарь,Экономист,Бухгалтер," \
                        "Менеджер по продажам,Инвестор,Архитектор,Фотограф," \
                        "Маркетолог,Генетик,Судья,Полицейский,Научный сотрудник," \
                        "Лаборант,Экскурсовод,Тренер,Сантехник,Электрик,Слесарь," \
                        "Автомеханик,Физик,Энергетик,Математик,Химик,Биолог," \
                        "Эколог,Экстрасенс,Вирусолог".split(',')

occupations_additive = "Проститутка,Варщик мета,Кладмен,Киллер,Стриптизёр".split(',')

characters_safe_mode = 'Интроверт,Экстраверт,Добрый,Оптимистичный,Толерантный,' \
                       'Ответственный,Безответственный,Наглый,Непоседа,Эгоист,Жестокий,' \
                       'Завистливый,Ревнивый,Мстительный,Ленивый,Лживый,Жадный,' \
                       'Пессимистичный,Агрессивный,Злопамятный,Застенчивый,' \
                       'Общительный,Гиперактивный,Сквернословный,Конфликтный,' \
                       'Надёжный,Безжалостный,Безотказный'.split(',')

characters_additive = ''.split(',')

healthes_safe_mode = 'Мигрень,Ожирение,ВИЧ I стадии (осталось жить 5 лет),' \
                     'Глухонемой,Идеально здоров,Рак лёгких,Идеально здоров,' \
                     'Алкоголизм,Анорексия,Дефект речи,Идеально здоров,' \
                     'Наркотическая зависимость,Диабет,Дальтоник,Идеально здоров,' \
                     'Бесплодие,Бесплодие,Бесплодие,Идеально здоров,' \
                     'Несворачиваемость крови,Аллергия на солнце,' \
                     'Бесплодие,Астма,Идеально здоров,Заикание,Глухой,' \
                     'Глухой,Глухонемой,Глухонемой,Немой,Немой,' \
                     'Идеально здоров,Идеально здоров,Идеально здоров,' \
                     'Идеально здоров'.split(',')

healthes_additive = 'Импотенция,Импотенция,Импотенция'.split(',')

hobbies_safe_mode = 'Охота,Рисование,Карточные фокусы,Изучение топографических ' \
                    'карт,Ремонт часов,Зоология,Пивоварение,Шитьё и вязание,' \
                    'Медитация,Выращивание растений,Стрельба из лука,' \
                    'Стрельба по мишеням,Радиосвязь,Изделия из кожи,Фотография,' \
                    'Плотницкое дело,Альпинизм,Игра на губной гармошке,' \
                    'Игра в гольф,Рыбалка,Сбор грибов,Боевые искусства,' \
                    'Футбол,Танцы,Парусный спорт,Кулинария,Пение'.split(',')

hobbies_additive = 'Гимнофобия - боязнь обнажённого тела'.split(',')

phobias_safe_mode = 'Нет фобии,Нет фобии,Нет фобии,Нет фобии,Нет фобии,Нет фобии,' \
                    'Клаустрофобия,Паразитофобия,Киберофобия - боязнь компьютеров,' \
                    'Фазмофобия - боязнь призраков и духов,Фазмофобия - боязнь призраков и духов,' \
                    'Канинофобия - боязнь собак,Топофобия - боязнь остаться одному в помещении,' \
                    'Коулрофобия - боязнь клоунов,Герпетофобия - боязнь рептилий и змей,' \
                    'Мусофобия - боязнь мышей и крыс,Аквафобия - боязнь воды,' \
                    'Демонофобия - боязнь демонов,Гоплофобия - боязнь оружия,' \
                    'Турофобия - боязнь сыра,Зоофобия - боязнь животных,' \
                    'Орнитофобия - боязнь птиц и их перьев,Библиофобия - боязнь библиотек,' \
                    'Клаустрофобия,Клаустрофобия,Клаустрофобия'.split(',')

phobias_additive = ''.split(',')

inventories_safe_mode = 'Ничего,Ничего,Ничего,Ничего,Ничего,Ничего,Ничего,Ничего,' \
                        'Ноутбук,Ноутбук,Ноутбук,Рюкзак,Рюкзак,' \
                        'Чемодан,Суперкомпьютер,Суперкомпьютер,Набор водных пистолетов,' \
                        'Пистолет без патронов,Пистолет без патронов,' \
                        'Пистолет и 100 патронов,Пистолет и 150 патронов,' \
                        'Пистолет и 2 патрона,Сборник анекдотов,' \
                        '"Война и мир",Конституция Гондураса,' \
                        'Учебник по истории,Зажигалка,Спички,' \
                        'Блок сигарет,DVD-проигрыватель,Спутниковая связь,' \
                        'Спутниковая связь,Коллекция монет разных стран,' \
                        '1 000 000 долларов, 1 000 000 долларов,' \
                        'Фотоаппарат,Литий-ионный аккумулятор,' \
                        '10 батареек,Тетрадь по физике,Автограф Влада А4,' \
                        'Аптечка,Аптечка,Аспирин,Аспирин,Парацетамол'.split(',')

inventories_additive = 'Резиновый дилдо,Набор секс-игрушек,Вибратор,' \
                       'Презерватив,Презерватив,Виагра'.split(',')

facts_safe_mode = '5 раз читал Гарри Поттера,Владеет языком жестов,' \
                  'Объездил весь мир,Верит в экстрасенсов,Знает азбуку Морзе,' \
                  'Рос в семье фермеров,Умеет ориентироваться по звёздам,' \
                  'КМС по боксу,Рос в семье географов,Читал все книги про зомби,' \
                  'Знает все стихи Пушкина наизусть,Имеет экстрасенсорные способности,' \
                  'Учился в медицинском университете 4 года,' \
                  'Знает лично президента,Подрабатывает в театре,' \
                  'По первому образованию биолог,' \
                  'По первому образованию химик,Изучал воду и её очищение,' \
                  'Может сделать алкоголь из чего угодно,' \
                  'Верит в инопланетян,Знает где склад оружия,Знает всё про компьютеры,' \
                  'Состоит в клубе "Навыки выживания" 3 года,' \
                  'Умеет делать луки и копья,По первому образованию архитектор,' \
                  'Остался в живых на необитаемом острове,Знает 5 языков,' \
                  'Подрабатывал в больнице,Вечный везунчик,' \
                  'Проходил курсы психолога'.split(',')

facts_additive = 'Скорострел'.split(',')

special_conditions = [Sc('Поменять карту профессии', Scs.change_occupation),
                      Sc('Поменять карту биологии', Scs.change_biology),
                      Sc('Поменять карту характера', Scs.change_character),
                      Sc('Поменять карту здоровья', Scs.change_health),
                      Sc('Поменять карту хобби', Scs.change_hobby),
                      Sc('Поменять карту фобии', Scs.change_phobia),
                      Sc('Поменять карту багажа', Scs.change_inventory),
                      Sc('Поменять карту факта', Scs.change_fact),
                      Sc('Перемешать открытые карты профессии', Scs.shuffle_occupation),
                      Sc('Перемешать открытые карты биологии', Scs.shuffle_biology),
                      Sc('Перемешать открытые карты характера', Scs.shuffle_character),
                      Sc('Перемешать открытые карты здоровья', Scs.shuffle_health),
                      Sc('Перемешать открытые карты хобби', Scs.shuffle_hobby),
                      Sc('Перемешать открытые карты фобии', Scs.shuffle_phobia),
                      Sc('Перемешать открытые карты багажа', Scs.shuffle_inventory),
                      Sc('Перемешать открытые карты факта', Scs.shuffle_fact)
                      ]

catastrophes = [
                Catastrophe('Химическая война',
                            'В результате применения химикатов серьёзно изменился '
                            'экологический баланс. Был нарушен микробиологический '
                            'состав почв, отравлены растения. После выхода из '
                            'бункера осталась малая часть животных и растений, '
                            'заражена вода и почва. Остаток здорового населения - 10%.'),
                Catastrophe('Супервулканы',
                            'Супервулканами называют вулканы, производящие '
                            'чрезвычайно мощные и объёмные извержения. Подобные '
                            'извержения приводят к тому, что ландшафт и климат '
                            'на нашей планете коренным образом изменятся. После '
                            'выхода из бункера глобальная засуха. Остаток населения '
                            'Земли - 5%.'),
                Catastrophe('Зомби-вирус',
                            'Прогрессирующее во времени и пространстве распространение '
                            'инфекционного заболевания среди людей способно стать '
                            'источником чрезвычайной ситуации. Люди теперь зомби. '
                            'После выхода из бункера малая часть зомби бродит по земле, '
                            'которая неизбежно погибнет. Остаток здорового населения - 15%.'),
                Catastrophe('Падение метеорита',
                            'Крупный метеорит попал в землю, что приводит к глобальным '
                            'разрушениям и смене климата. После выхода из бункера на земле '
                            'вечная зима. Остаток населения Земли - 15%.'),
                Catastrophe('Ядерная катастрофа',
                            'Начнётся ядерная война, радиоактивная пыль окутает всю планету, '
                            'закрыв солнечный свет, и на планете наступит долгая ядерная '
                            'зима. После выхода из бункера сложности с почвой, водой. '
                            'Необходима дополнительная химическая обработка. '
                            'Остаток населения Земли - 5%.'),
                Catastrophe('Всемирный потоп',
                            'Из-за глобального потепления растают все полярные и континентальные '
                            'льды. Процент суши составит 15%. Вода поглотит всё вокруг. После '
                            'выхода из бункера произошло нарушение климата - тропики теперь '
                            'повсюду. Необходимо приспособиться к новым видам растений и '
                            'крупным насекомым. Остаток населения Земли - люди в бункерах.'),
                Catastrophe('Биотерроризм',
                            'Смертельный вирус, созданный как биологическое оружие, выйдет из-под '
                            'контроля и спровоцирует глобальную эпидемию. После выхода из бункера '
                            'будет выявлена мутация практически всех видов животных, растений и '
                            'людей. Остаток здорового населения - 7%.')
                ]


class GameRandomizer:
    def __init__(self, safe_mode=True):
        self.safe_mode = safe_mode  # безопасный режим (для 18-)

    def generate_occupation(self):
        if self.safe_mode:
            return Occupation(occupations_safe_mode[random.randint(0, len(occupations_safe_mode) - 1)])
        occupations = occupations_additive + occupations_safe_mode
        return Occupation(occupations[random.randint(0, len(occupations) - 1)])

    def generate_character(self):
        if self.safe_mode:
            return Character(characters_safe_mode[random.randint(0, len(characters_safe_mode) - 1)])
        characters = characters_additive + characters_safe_mode
        return Character(characters[random.randint(0, len(characters) - 1)])

    def generate_health(self):
        if self.safe_mode:
            return Health(healthes_safe_mode[random.randint(0, len(healthes_safe_mode) - 1)])
        healthes = healthes_additive + healthes_safe_mode
        return Health(healthes[random.randint(0, len(healthes) - 1)])

    def generate_hobby(self):
        if self.safe_mode:
            return Hobby(hobbies_safe_mode[random.randint(0, len(hobbies_safe_mode) - 1)])
        hobbies = hobbies_additive + hobbies_safe_mode
        return Hobby(hobbies[random.randint(0, len(hobbies) - 1)])

    def generate_phobia(self):
        if self.safe_mode:
            return Phobia(phobias_safe_mode[random.randint(0, len(phobias_safe_mode) - 1)])
        phobias = phobias_additive + phobias_safe_mode
        return Phobia(phobias[random.randint(0, len(phobias) - 1)])

    def generate_inventory(self):
        if self.safe_mode:
            return Inventory(inventories_safe_mode[random.randint(0, len(inventories_safe_mode) - 1)])
        inventories = inventories_additive + inventories_safe_mode
        return Inventory(inventories[random.randint(0, len(inventories) - 1)])

    def generate_fact(self):
        if self.safe_mode:
            return Fact(facts_safe_mode[random.randint(0, len(facts_safe_mode) - 1)])
        facts = facts_additive + facts_safe_mode
        return Fact(facts[random.randint(0, len(facts) - 1)])

    def generate_biology(self):
        age = random.randint(18, 100)
        sex = 'Мужчина' if random.random() >= 0.5 else 'Женщина'
        orientation = 'гетеросексуал'
        if not self.safe_mode:
            if random.random() <= 0.10:
                if random.random() < 0.5:
                    orientation = 'гомосексуал'
                else:
                    orientation = 'бисексуал'
        if self.safe_mode:
            return Biology(f'{sex}, {age} {year_word(age)}')
        else:
            return Biology(f'{sex}, {age} {year_word(age)}, {orientation}')

    @staticmethod
    def generate_special_condition():
        return special_conditions[random.randint(0, len(special_conditions)-1)]

    @staticmethod
    def generate_catastrophe():
        return catastrophes[random.randint(0, len(catastrophes)-1)]
