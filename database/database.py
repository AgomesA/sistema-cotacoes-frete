import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = "data/transportadora.db"
        self._create_database()
        self._create_tables()
    
    def _create_database(self):
        """Cria a pasta data se não existir"""
        os.makedirs("data", exist_ok=True)
    
    def _create_tables(self):
        """Cria todas as tabelas do sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Tabela de transportadoras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transportadoras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cnpj TEXT UNIQUE,
                    percentual_base REAL DEFAULT 0,
                    icms REAL DEFAULT 0,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de cotações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cotacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fornecedor TEXT NOT NULL,
                    num_pedido TEXT,
                    valor_nf REAL NOT NULL,
                    peso REAL,
                    volume INTEGER,
                    cubagem REAL,
                    transportadora_ganhadora_id INTEGER,
                    FOREIGN KEY (transportadora_ganhadora_id) REFERENCES transportadoras (id)
                )
            ''')
            
            # Tabela de cotações por transportadora
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cotacoes_transportadoras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cotacao_id INTEGER NOT NULL,
                    transportadora_id INTEGER NOT NULL,
                    valor_frete REAL NOT NULL,
                    selecionada BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (cotacao_id) REFERENCES cotacoes (id),
                    FOREIGN KEY (transportadora_id) REFERENCES transportadoras (id)
                )
            ''')
            
            # Tabela de cálculos de cubagem
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calculos_cubagem (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    itens_json TEXT NOT NULL,
                    cubagem_total REAL NOT NULL
                )
            ''')
            
            # Tabela de contatos das transportadoras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transportadora_contatos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transportadora_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,  -- 'telefone' ou 'email'
                    valor TEXT NOT NULL,
                    contato TEXT,        -- nome do contato (opcional)
                    FOREIGN KEY (transportadora_id) REFERENCES transportadoras (id)
                )
            ''')
            
            # Insere a Rodocargas como transportadora padrão
            cursor.execute('''
                INSERT OR IGNORE INTO transportadoras 
                (nome, cnpj, percentual_base, icms) 
                VALUES (?, ?, ?, ?)
            ''', ('Rodocargas', '00.000.000/0000-00', 14.0, 7.0))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_connection(self):
        """Retorna uma conexão com o banco com timeout aumentado"""
        conn = sqlite3.connect(self.db_path, timeout=20)
        conn.execute("PRAGMA busy_timeout = 30000")  # 30 segundos de timeout
        return conn