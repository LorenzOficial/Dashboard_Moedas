import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="users.db"):
        """Inicializa a conexão com o banco de dados e cria a tabela se não existir."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_user_table()

    def create_user_table(self):
        """Cria a tabela de usuários se ela ainda não existir."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def _hash_password(self, password):
        """Criptografa a senha usando o algoritmo SHA256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def add_user(self, username, password):
        """Adiciona um novo usuário ao banco de dados com senha criptografada."""
        if not username or not password:
            return False, "Usuário e senha não podem estar vazios."
        
        try:
            hashed_password = self._hash_password(password)
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True, "Usuário registrado com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Este nome de usuário já existe."

    def check_user(self, username, password):
        """Verifica se o usuário e a senha correspondem aos registros do banco."""
        hashed_password = self._hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = self.cursor.fetchone()
        return user is not None

    def __del__(self):
        """Fecha a conexão com o banco de dados quando o objeto é destruído."""
        self.conn.close()
