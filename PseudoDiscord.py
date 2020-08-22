import sqlite3
from Heroes import create_hero
from Monsters import create_monster
from Monsters import Monster
from Heroes import Hero



conn = sqlite3.connect('NewData.db')
cursor = conn.cursor()


# def delete_all_tasks(conn):
#
#     sql = 'DELETE FROM heroes'
#     sql2 = 'DELETE FROM monsters'
#     conn = conn.cursor()
#     conn.execute(sql)
#     conn.execute(sql2)
#     conn.close()


# delete_all_tasks(conn)

# cursor.execute("CREATE TABLE games(game_id n(5), hero char(30), monster char(35));")
# cursor.execute("""CREATE TABLE heroes(
#     hero_name text,
#     hero_attack integer,
#     hero_class text,
#     hero_health integer,
#     hero_id integer)""")
#
# create_hero()


# cursor.execute("""CREATE TABLE monsters(
# monster_name text,
# monster_attack integer,
# monster_health integer,
# monster_id integer)""")

create_monster()


def attack():
    hero_id = input()
    monster_id = input()
    cursor.execute("""Update monsters set monster_health = (select hero_attack from heroes 
    where hero_id = ?) - monster_health WHERE monster_id=?""", (monster_id, hero_id))
    conn.commit()
    print("Record Updated successfully ")
    cursor.close()
# c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_2.last, emp_1.pay))


attack()

print("Checking if everything is fine...")
conn.close()
