import sqlite3

conn = sqlite3.connect('NewData.db')
cursor = conn.cursor()


def create_hero():
    playerhero = Hero(input("Enter hero name: "), input("Enter hero class: "), input("Enter hero attack: "),
                      input("Enter hero health: "), input("Enter hero id: "))
    with conn:
        cursor.execute(
            "INSERT INTO heroes(hero_name, hero_class, hero_attack, hero_id, hero_health) VALUES (?, ?, ?, ?, ?)",
            (playerhero.hero_name, playerhero.hero_class, playerhero.hero_attack, playerhero.hero_id,
             playerhero.hero_health))


class Hero:

    def __init__(self, hero_name, hero_class, hero_attack, hero_health, hero_id):
        self.hero_name = hero_name
        self.hero_class = hero_class
        self.hero_attack = hero_attack
        self.hero_health = hero_health
        self.hero_id = hero_id

    @property
    def __repr__(self):
        return "('Your hero is ', '{}', 'and a class of ' {})".format(self.hero_name, self.hero_class)
