# main.py - SISTEMA COMPLETO DE COTAÇÕES DE FRETE COM DASHBOARD PREMIUM
import sys
import os
import sqlite3
import colorsys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QMessageBox, QFrame,
                             QTableWidget, QTableWidgetItem, QScrollArea, QGroupBox, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Adiciona as subpastas ao path do Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'gui'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Importa dos subdiretórios
try:
    from gui.transportadoras_window import TransportadorasWindow
    from gui.cotacao_window import CotacaoWindow
    from gui.calculadora_window import CalculadoraWindow
    from gui.historico_window import HistoricoWindow
    from database.database import Database
    print("✅ Todos os módulos importados com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("🚚 Sistema de Cotações de Frete - MERLI")
        self.setMinimumSize(1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Sidebar (menu lateral)
        self.setup_sidebar(main_layout)
        
        # Área de conteúdo com StackedWidget
        self.setup_content_area(main_layout)
    
    def setup_sidebar(self, main_layout):
        # Frame da sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #34495e);
            }
        """)
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)
        
        # Logo e título
        logo_widget = QWidget()
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        
        logo_icon = QLabel("🚚")
        logo_icon.setStyleSheet("font-size: 40px;")
        logo_icon.setAlignment(Qt.AlignCenter)
        
        logo_text = QLabel("MERLI")
        logo_text.setFont(QFont("Arial", 18, QFont.Bold))
        logo_text.setStyleSheet("color: white;")
        logo_text.setAlignment(Qt.AlignCenter)
        
        logo_subtext = QLabel("Sistema de Cotações")
        logo_subtext.setStyleSheet("color: #bdc3c7; font-size: 10px;")
        logo_subtext.setAlignment(Qt.AlignCenter)
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addWidget(logo_subtext)
        logo_widget.setLayout(logo_layout)
        
        sidebar_layout.addWidget(logo_widget)
        sidebar_layout.addSpacing(20)
        
        # Botões do menu com ações
        menu_actions = [
            ("🏠 INÍCIO", self.show_home),
            ("🚛 TRANSPORTADORAS", self.show_transportadoras), 
            ("📦 COTAÇÃO", self.show_cotacao),
            ("🧮 CALCULADORA", self.show_calculadora),
            ("📋 HISTÓRICO", self.show_historico)
        ]
        
        for menu_text, menu_action in menu_actions:
            btn = QPushButton(menu_text)
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.1);
                    color: white;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    font-weight: bold;
                    font-size: 13px;
                    border-radius: 5px;
                    margin: 2px 10px;
                }
                QPushButton:hover {
                    background-color: rgba(52, 152, 219, 0.3);
                    border-left: 3px solid #3498db;
                }
            """)
            btn.clicked.connect(menu_action)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        
        # Rodapé da sidebar
        footer_label = QLabel("© 2024 MERLI")
        footer_label.setStyleSheet("color: #7f8c8d; font-size: 10px; padding: 10px;")
        footer_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(footer_label)
        
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)
    
    def setup_content_area(self, main_layout):
        # StackedWidget para alternar entre páginas
        self.stacked_widget = QStackedWidget()
        
        # Criar as páginas
        self.home_page = self.create_home_page()
        self.transportadoras_page = TransportadorasWindow(self.db)
        self.cotacao_page = CotacaoWindow(self.db)
        self.calculadora_page = CalculadoraWindow(self.db)
        self.historico_page = HistoricoWindow(self.db)
        
        # Adicionar páginas ao stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.transportadoras_page)
        self.stacked_widget.addWidget(self.cotacao_page)
        self.stacked_widget.addWidget(self.calculadora_page)
        self.stacked_widget.addWidget(self.historico_page)
        
        main_layout.addWidget(self.stacked_widget)

    def create_home_page(self):
        """Cria a página inicial com dashboard premium em tempo real"""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Barra superior premium
        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #3498db);
                border-bottom: 3px solid #2980b9;
            }
        """)
        
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(25, 0, 25, 0)
        
        # Título e informações
        title_layout = QVBoxLayout()
        
        welcome_text = QLabel("Bem-vindo ao MERLI!")
        welcome_text.setFont(QFont("Arial", 16, QFont.Bold))
        welcome_text.setStyleSheet("color: white;")
        
        date_text = QLabel(f"📅 {datetime.now().strftime('%A, %d de %B de %Y')} | ⏰ {datetime.now().strftime('%H:%M')}")
        date_text.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 12px;")
        
        title_layout.addWidget(welcome_text)
        title_layout.addWidget(date_text)
        
        # Botões de ação
        action_layout = QHBoxLayout()
        
        btn_atualizar = QPushButton("🔄 Atualizar Dashboard")
        btn_atualizar.setFixedSize(150, 35)
        btn_atualizar.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """)
        btn_atualizar.clicked.connect(self.atualizar_dashboard)
        
        action_layout.addStretch()
        action_layout.addWidget(btn_atualizar)
        
        top_layout.addLayout(title_layout)
        top_layout.addStretch()
        top_layout.addLayout(action_layout)
        top_bar.setLayout(top_layout)
        
        # Área de conteúdo principal
        content_area = QWidget()
        content_area.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ecf0f1, stop:1 #bdc3c7);")
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(25)
        
        # Buscar dados em tempo real
        dashboard_data = self.get_dashboard_data()
        
        # 1. CARDS DE MÉTRICAS PRINCIPAIS
        metrics_group = QGroupBox("📊 VISÃO GERAL DO SISTEMA")
        metrics_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #2c3e50;
                border: 2px solid #95a5a6;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)
        
        # Cards de métricas
        cards_data = [
            {
                "title": "Cotações do Mês", 
                "value": str(dashboard_data.get('total_cotacoes_mes', 0)),
                "subtitle": "Realizadas este mês",
                "color": "#3498db",
                "icon": "📦"
            },
            {
                "title": "Transportadoras", 
                "value": str(dashboard_data.get('total_transportadoras', 0)),
                "subtitle": "Cadastradas no sistema", 
                "color": "#2ecc71",
                "icon": "🚛"
            },
            {
                "title": "Economia Estimada", 
                "value": f"R$ {dashboard_data.get('economia_estimada', 0):,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                "subtitle": "Total economizado",
                "color": "#e74c3c", 
                "icon": "💰"
            },
            {
                "title": "Performance",
                "value": f"{dashboard_data.get('taxa_media_frete', 0):.1f}%",
                "subtitle": "Taxa média de frete",
                "color": "#f39c12",
                "icon": "📈"
            }
        ]
        
        for card_info in cards_data:
            card = self.create_premium_card(
                card_info["title"],
                card_info["value"], 
                card_info["subtitle"],
                card_info["color"],
                card_info["icon"]
            )
            metrics_layout.addWidget(card)
        
        metrics_group.setLayout(metrics_layout)
        content_layout.addWidget(metrics_group)
        
        # 2. LAYOUT DUPLO: AÇÕES + ESTATÍSTICAS
        dual_layout = QHBoxLayout()
        dual_layout.setSpacing(25)
        
        # COLUNA ESQUERDA - AÇÕES RÁPIDAS
        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        
        # Ações rápidas
        actions_group = QGroupBox("⚡ AÇÕES RÁPIDAS")
        actions_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(10)
        
        action_buttons = [
            ("📦 NOVA COTAÇÃO", self.show_cotacao, "#27ae60"),
            ("🧮 CALCULADORA CUBAGEM", self.show_calculadora, "#2980b9"), 
            ("🚛 TRANSPORTADORAS", self.show_transportadoras, "#8e44ad"),
            ("📋 VER HISTÓRICO", self.show_historico, "#e67e22")
        ]
        
        for text, action, color in action_buttons:
            btn = self.create_action_button(text, color)
            btn.clicked.connect(action)
            actions_layout.addWidget(btn)
        
        actions_group.setLayout(actions_layout)
        left_column.addWidget(actions_group)
        
        # COLUNA DIREITA - ESTATÍSTICAS
        right_column = QVBoxLayout()
        right_column.setSpacing(20)
        
        # Estatísticas detalhadas
        stats_group = QGroupBox("📈 ESTATÍSTICAS DETALHADAS")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(8)
        
        stats_data = [
            ("📅 Cotações este mês:", str(dashboard_data.get('total_cotacoes_mes', 0))),
            ("💰 Valor total das NF:", f"R$ {dashboard_data.get('valor_total_mes', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')),
            ("📦 Maior valor de NF:", f"R$ {dashboard_data.get('maior_valor_nf', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')),
            ("🚛 Transportadoras ativas:", str(dashboard_data.get('total_transportadoras', 0))),
            ("🏆 Transportadora mais usada:", dashboard_data.get('transp_mais_usada', 'Nenhuma')),
            ("📊 Taxa média de frete:", f"{dashboard_data.get('taxa_media_frete', 0):.1f}%"),
            ("💸 Economia total estimada:", f"R$ {dashboard_data.get('economia_estimada', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')),
            ("🕒 Última cotação:", dashboard_data.get('ultima_cotacao_data', 'Nenhuma'))
        ]
        
        for label, value in stats_data:
            stat_item = self.create_premium_stat_item(label, value)
            stats_layout.addWidget(stat_item)
        
        stats_group.setLayout(stats_layout)
        right_column.addWidget(stats_group)
        
        # Adiciona as colunas ao layout duplo
        dual_layout.addLayout(left_column, 40)
        dual_layout.addLayout(right_column, 60)
        
        content_layout.addLayout(dual_layout)
        
        # 3. COTAÇÕES RECENTES
        recent_group = QGroupBox("🕒 COTAÇÕES MAIS RECENTES")
        recent_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        recent_layout = QVBoxLayout()
        
        # Tabela de cotações recentes
        recent_table = self.create_premium_table(dashboard_data.get('cotacoes_recentes', []))
        recent_layout.addWidget(recent_table)
        
        recent_group.setLayout(recent_layout)
        content_layout.addWidget(recent_group)
        
        content_area.setLayout(content_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(content_area)
        
        # Layout principal
        layout.addWidget(top_bar)
        layout.addWidget(scroll)
        
        page.setLayout(layout)
        return page

    def create_premium_card(self, title, value, subtitle, color, icon):
        """Cria um card premium com gradiente"""
        card = QFrame()
        card.setFixedSize(220, 130)
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {self.darken_color(color, 15)});
                border-radius: 12px;
                border: 1px solid {self.darken_color(color, 10)};
            }}
            QFrame:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.lighten_color(color, 5)}, stop:1 {color});
                border: 2px solid {self.lighten_color(color, 20)};
            }}
        """)
        
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(8)
        
        # Header do card
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Valor principal
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        
        # Subtítulo
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: rgba(255,255,255,0.9); font-size: 11px; font-style: italic;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        card_layout.addLayout(header_layout)
        card_layout.addWidget(value_label)
        card_layout.addStretch()
        card_layout.addWidget(subtitle_label)
        
        card.setLayout(card_layout)
        return card

    def create_action_button(self, text, color):
        """Cria botões de ação estilizados"""
        btn = QPushButton(text)
        btn.setFixedHeight(55)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {self.lighten_color(color, 15)});
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
                padding: 15px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.lighten_color(color, 5)}, stop:1 {self.lighten_color(color, 20)});
                border: 2px solid rgba(255,255,255,0.3);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.darken_color(color, 5)}, stop:1 {color});
            }}
        """)
        return btn

    def create_premium_stat_item(self, label, value):
        """Cria itens de estatística premium"""
        widget = QWidget()
        widget.setFixedHeight(35)
        widget.setStyleSheet("""
            QWidget {
                background: rgba(255,255,255,0.8);
                border-radius: 8px;
                margin: 2px;
            }
            QWidget:hover {
                background: rgba(255,255,255,0.95);
                border: 1px solid #3498db;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #2c3e50; font-size: 12px; font-weight: bold;")
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet("color: #27ae60; font-size: 12px; font-weight: bold;")
        
        layout.addWidget(label_widget)
        layout.addStretch()
        layout.addWidget(value_widget)
        
        widget.setLayout(layout)
        return widget

    def create_premium_table(self, cotacoes_recentes):
        """Cria tabela premium para cotações recentes"""
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["📅 Data", "🏢 Fornecedor", "💰 Valor NF", "🚚 Frete", "📊 Transportadora"])
        
        # Estilo da tabela
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                gridline-color: #ecf0f1;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        table.setRowCount(len(cotacoes_recentes))
        
        for row, cotacao in enumerate(cotacoes_recentes):
            # Data
            data_item = QTableWidgetItem(cotacao['data'])
            table.setItem(row, 0, data_item)
            
            # Fornecedor
            fornecedor_item = QTableWidgetItem(cotacao['fornecedor'])
            table.setItem(row, 1, fornecedor_item)
            
            # Valor NF
            valor_nf = f"R$ {cotacao['valor_nf']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            valor_item = QTableWidgetItem(valor_nf)
            table.setItem(row, 2, valor_item)
            
            # Frete
            if cotacao['valor_frete']:
                frete = f"R$ {cotacao['valor_frete']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            else:
                frete = "-"
            frete_item = QTableWidgetItem(frete)
            table.setItem(row, 3, frete_item)
            
            # Transportadora
            transp_item = QTableWidgetItem(cotacao['transportadora'] or "-")
            table.setItem(row, 4, transp_item)
        
        # Configurar header
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        table.setMaximumHeight(220)
        return table

    def darken_color(self, color, percent):
        """Escurece uma cor HEX"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        hls = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        darker = colorsys.hls_to_rgb(hls[0], max(0, hls[1] - percent/100), hls[2])
        return '#{:02x}{:02x}{:02x}'.format(int(darker[0]*255), int(darker[1]*255), int(darker[2]*255))

    def lighten_color(self, color, percent):
        """Clareia uma cor HEX"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        hls = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        lighter = colorsys.hls_to_rgb(hls[0], min(1, hls[1] + percent/100), hls[2])
        return '#{:02x}{:02x}{:02x}'.format(int(lighter[0]*255), int(lighter[1]*255), int(lighter[2]*255))

    def atualizar_dashboard(self):
        """Atualiza o dashboard"""
        # Recria a página home
        self.stacked_widget.removeWidget(self.home_page)
        self.home_page = self.create_home_page()
        self.stacked_widget.insertWidget(0, self.home_page)
        self.stacked_widget.setCurrentIndex(0)
        
        QMessageBox.information(self, "Atualizado", "Dashboard atualizado com sucesso!")

    def get_dashboard_data(self):
        """Busca dados reais do banco para o dashboard"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Total de cotações este mês
            cursor.execute("""
                SELECT COUNT(*) FROM cotacoes 
                WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
            """)
            total_cotacoes_mes = cursor.fetchone()[0] or 0
            
            # Total de transportadoras
            cursor.execute("SELECT COUNT(*) FROM transportadoras")
            total_transportadoras = cursor.fetchone()[0] or 0
            
            # Valor total das cotações este mês
            cursor.execute("""
                SELECT COALESCE(SUM(valor_nf), 0) FROM cotacoes 
                WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
            """)
            valor_total_mes = cursor.fetchone()[0] or 0
            
            # Maior valor de NF
            cursor.execute("SELECT COALESCE(MAX(valor_nf), 0) FROM cotacoes")
            maior_valor_nf = cursor.fetchone()[0] or 0
            
            # Última cotação
            cursor.execute("""
                SELECT c.data, c.fornecedor 
                FROM cotacoes c 
                ORDER BY c.data DESC LIMIT 1
            """)
            ultima_result = cursor.fetchone()
            if ultima_result:
                data_parts = ultima_result[0].split('-')
                ultima_cotacao_data = f"{data_parts[2]}/{data_parts[1]}"
            else:
                ultima_cotacao_data = "Nenhuma"
            
            # Transportadora mais usada
            cursor.execute("""
                SELECT t.nome, COUNT(ct.id) as total
                FROM cotacoes_transportadoras ct
                JOIN transportadoras t ON ct.transportadora_id = t.id
                WHERE ct.selecionada = 1
                GROUP BY t.nome
                ORDER BY total DESC
                LIMIT 1
            """)
            transp_result = cursor.fetchone()
            transp_mais_usada = transp_result[0] if transp_result else "Nenhuma"
            
            # Taxa média de frete
            cursor.execute("""
                SELECT AVG((ct.valor_frete / c.valor_nf) * 100)
                FROM cotacoes_transportadoras ct
                JOIN cotacoes c ON ct.cotacao_id = c.id
                WHERE ct.selecionada = 1 AND c.valor_nf > 0
            """)
            taxa_result = cursor.fetchone()[0]
            taxa_media = round(taxa_result, 1) if taxa_result else 0.0
            
            # Cotações recentes (últimas 5)
            cursor.execute("""
                SELECT 
                    c.data, 
                    c.fornecedor, 
                    c.valor_nf,
                    ct.valor_frete,
                    t.nome as transportadora
                FROM cotacoes c
                LEFT JOIN cotacoes_transportadoras ct ON c.id = ct.cotacao_id AND ct.selecionada = 1
                LEFT JOIN transportadoras t ON ct.transportadora_id = t.id
                ORDER BY c.data DESC, c.id DESC
                LIMIT 5
            """)
            
            cotacoes_recentes = []
            for row in cursor.fetchall():
                data_original = row[0]
                data_formatada = f"{data_original[8:10]}/{data_original[5:7]}"  # DD/MM
                
                cotacoes_recentes.append({
                    'data': data_formatada,
                    'fornecedor': row[1],
                    'valor_nf': row[2] or 0,
                    'valor_frete': row[3],
                    'transportadora': row[4]
                })
            
            # Economia estimada (exemplo: 10% do valor total)
            economia_estimada = valor_total_mes * 0.10
            
            conn.close()
            
            return {
                'total_cotacoes_mes': total_cotacoes_mes,
                'total_transportadoras': total_transportadoras,
                'valor_total_mes': valor_total_mes,
                'maior_valor_nf': maior_valor_nf,
                'ultima_cotacao_data': ultima_cotacao_data,
                'transp_mais_usada': transp_mais_usada,
                'taxa_media_frete': taxa_media,
                'cotacoes_recentes': cotacoes_recentes,
                'economia_estimada': economia_estimada
            }
            
        except Exception as e:
            print(f"Erro ao buscar dados do dashboard: {e}")
            # Retorna dados padrão em caso de erro
            return {
                'total_cotacoes_mes': 0,
                'total_transportadoras': 0,
                'valor_total_mes': 0,
                'maior_valor_nf': 0,
                'ultima_cotacao_data': "Nenhuma",
                'transp_mais_usada': "Nenhuma",
                'taxa_media_frete': 0,
                'cotacoes_recentes': [],
                'economia_estimada': 0
            }

    # MÉTODOS DE NAVEGAÇÃO
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
    
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Sair',
            'Deseja realmente sair?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())