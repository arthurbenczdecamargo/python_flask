import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="root")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Usuário ou senha inválidos.")
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

TABLES = {}
TABLES["Jogos"] = (
    """
        CREATE TABLE `jogos` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `nome` varchar(50) NOT NULL,
        `categoria` varchar(40) NOT NULL,
        `console` varchar(20) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"""
)

TABLES["Usuarios"] = (
    """
        CREATE TABLE `usuarios` (
        `nome` varchar(20) NOT NULL,
        `nickname` varchar(20) NOT NULL,
        `senha` varchar(100) NOT NULL,
        PRIMARY KEY (`nickname`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"""
)

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f"Criando tabela {tabela_nome}:", end=" ")
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Já existe")
        else:
            print(err.msg)
    else:
        print("OK")

usuario_sql = "INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)"
usuarios = [
    ("Arthur Camargo", "art", generate_password_hash("test123").decode("utf-8")),
    ("Gabriela Camargo", "gabi", generate_password_hash("1234").decode("utf-8")),
    ("Lucimar Camargo", "lu", generate_password_hash("lu123").decode("utf-8")),
]

cursor.executemany(usuario_sql, usuarios)

cursor.execute("select * from jogoteca.usuarios")
print(" ------------- Usuários: -------------")
for user in cursor.fetchall():
    print(user[1])

jogos_sql = "INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)"
jogos = [
    ("Tetris", "Puzzle", "GameBoy"),
    ("The Last of Us", "Survival Horror", "PS4"),
    ("God of War II", "Hack and Slash", "PS2"),
    ("VALORANT", "FPS", "PC"),
    ("League of Legends", "MOBA", "PC"),
    ("F1 2024", "Racing", "PC"),
    ("Mortal Kombat: Shaolin Monks", "Fighting", "PS2"),
    ("PUBG", "Battle Royale", "PC"),
    ("Mario Kart 8 Deluxe", "Racing", "Switch"),
    ("The Witcher 3: Wild Hunt", "RPG", "PC"),
]

cursor.executemany(jogos_sql, jogos)

cursor.execute("select * from jogoteca.jogos")
print(" ------------- Jogos: -------------")
for jogo in cursor.fetchall():
    print(jogo[1])

conn.commit()

cursor.close()
conn.close()
