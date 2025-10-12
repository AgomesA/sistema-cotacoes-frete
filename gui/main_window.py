import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.database import Database
from gui.transportadoras_window import TransportadorasWindow
from gui.cotacao_window import CotacaoWindow
from gui.calculadora_window import CalculadoraWindow
from gui.historico_window import HistoricoWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()  # ← ADICIONE ESTA LINHA
        self.setWindowTitle("Sistema de Cotações - Transportadora")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Painel lateral (menu)
        self.setup_sidebar(main_layout)
        
        # Área de conteúdo
        self.setup_content_area(main_layout)
    
    def setup_sidebar(self, main_layout):
        """Configura o menu lateral"""
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: white;
            }
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setSpacing(5)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        
        # Título
        title = QLabel("MENU PRINCIPAL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 20px;")
        sidebar_layout.addWidget(title)
        
        # Botões do menu
        buttons = [
            ("🏠 INÍCIO", self.show_home),
            ("🚛 TRANSPORTADORAS", self.show_transportadoras),
            ("📊 COTAÇÃO", self.show_cotacao),
            ("🧮 CALCULADORA", self.show_calculadora),
            ("📋 HISTÓRICO", self.show_historico)
        ]
        
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.clicked.connect(callback)
            sidebar_layout.addWidget(btn)
        
        # Espaço flexível no final
        sidebar_layout.addStretch()
        
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)
    
    def setup_content_area(self, main_layout):
        """Configura a área de conteúdo principal"""
        self.stacked_widget = QStackedWidget()
        
        # Páginas do sistema
        self.home_page = self.create_home_page()
        self.transportadoras_page = TransportadorasWindow(self.db)
        self.cotacao_page = CotacaoWindow(self.db)
        self.calculadora_page = CalculadoraWindow(self.db)
        self.historico_page = HistoricoWindow(self.db)  # ← NOVA TELA REAL
        
        # Adiciona páginas ao stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.transportadoras_page)
        self.stacked_widget.addWidget(self.cotacao_page)
        self.stacked_widget.addWidget(self.calculadora_page)
        self.stacked_widget.addWidget(self.historico_page)
    
        main_layout.addWidget(self.stacked_widget)
    
    def create_home_page(self):
        """Cria a página inicial (Dashboard)"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("SISTEMA DE COTAÇÕES - TRANSPORTADORA")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)
        
        # Mensagem de boas-vindas
        welcome = QLabel("Bem-vindo ao sistema de gestão de cotações!")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet("font-size: 14px; color: #666; margin: 20px;")
        layout.addWidget(welcome)
        
        # Área para métricas futuras
        metrics_label = QLabel("📊 Dashboard em desenvolvimento...")
        metrics_label.setAlignment(Qt.AlignCenter)
        metrics_label.setStyleSheet("font-size: 16px; margin: 50px;")
        layout.addWidget(metrics_label)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_placeholder_page(self, page_name):
        """Cria páginas placeholder para desenvolvimento"""
        page = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel(f"PÁGINA: {page_name}")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        message = QLabel(f"Funcionalidade {page_name} em desenvolvimento...")
        message.setAlignment(Qt.AlignCenter)
        message.setStyleSheet("font-size: 14px; color: #666; margin: 50px;")
        layout.addWidget(message)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    # Métodos de navegação
    def show_home(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def show_transportadoras(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def show_cotacao(self):
        self.stacked_widget.setCurrentIndex(2)
    
    def show_calculadora(self):
        self.stacked_widget.setCurrentIndex(3)
    
    def show_historico(self):
        self.stacked_widget.setCurrentIndex(4)