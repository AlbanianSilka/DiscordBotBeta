import sqlite3

conn = sqlite3.connect('NewData.db')
cursor = conn.cursor()


def create_monster():
    # print("Please, enter your monster name: ")
    # monster_name = input()
    # print("Enter your monster attack count: ")
    # monster_attack = input()
    # print("Enter your monster id: ")
    # monster_id = input()
    # print("Enter your monster health: ")
    # monster_health = input()
    enemy = Monster(input("Enter monster name: "), input("Enter monster id: "),
                           input("Enter monster attack: "), input("Enter monster health: "))
    with conn:
        cursor.execute("INSERT INTO monsters VALUES (:monster_name, :monster_attack, :monster_health, :monster_id)",
                       {'monster_name': enemy.monster_name, 'monster_attack': enemy.monster_attack,
                        'monster_health': enemy.monster_health,
                        'monster_id': enemy.monster_id})


class Monster:

    def __init__(self, monster_name, monster_id, monster_attack, monster_health):
        self.monster_name = monster_name
        self.monster_id = monster_id
        self.monster_attack = monster_attack
        self.monster_health = monster_health

    @property
    def __repr__(self):
        return "('Your monster is ', '{}')".format(self.monster_name)
