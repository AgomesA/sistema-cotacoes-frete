# main.py - SISTEMA COMPLETO DE COTAÇÕES DE FRETE (CÓDIGO CORRIGIDO)
import sys
import os
import sqlite3
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
        self.setWindowTitle("🚚 Sistema de Cotações de Frete")
        self.setMinimumSize(1000, 600)
        
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
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2c3e50;")
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)
        
        # Título
        title = QLabel("🚚 MERLI")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: white; padding: 20px;")
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)
        
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
            btn.setFixedHeight(45)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495e;
                    color: white;
                    border: none;
                    text-align: left;
                    padding-left: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3498db;
                }
            """)
            btn.clicked.connect(menu_action)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
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
        """Cria a página inicial com dashboard em tempo real"""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Barra superior
        top_bar = QFrame()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("background-color: white; border-bottom: 1px solid #bdc3c7;")
        
        top_layout = QHBoxLayout()
        title = QLabel("SISTEMA DE COTAÇÕES DE FRETE - DASHBOARD")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        
        top_layout.addWidget(title)
        top_layout.addStretch()
        
        # Data atual
        data_atual = QLabel(datetime.now().strftime("%d/%m/%Y"))
        data_atual.setStyleSheet("color: #7f8c8d; font-weight: bold;")
        top_layout.addWidget(data_atual)
        
        top_bar.setLayout(top_layout)
        
        # Área de conteúdo com scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        # Buscar dados em tempo real
        dashboard_data = self.get_dashboard_data()
        
        # 1. CARDS DE RESUMO (KPI's)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)
        
        # Card: Total de Cotações
        total_cotacoes = dashboard_data.get('total_cotacoes_mes', 0)
        card1 = self.create_card("📊 TOTAL DE COTAÇÕES", str(total_cotacoes), "Este mês", "#3498db")
        
        # Card: Transportadoras
        total_transportadoras = dashboard_data.get('total_transportadoras', 0)
        card2 = self.create_card("🚛 TRANSPORTADORAS", str(total_transportadoras), "Cadastradas", "#2ecc71")
        
        # Card: Economia
        economia = dashboard_data.get('economia_estimada', 0)
        economia_formatada = f"R$ {economia:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        card3 = self.create_card("💰 ECONOMIA ESTIMADA", economia_formatada, "Este mês", "#e74c3c")
        
        # Card: Cotação Mais Recente
        ultima_data = dashboard_data.get('ultima_cotacao_data', 'Nenhuma')
        card4 = self.create_card("🕒 ÚLTIMA COTAÇÃO", ultima_data, "Mais recente", "#f39c12")
        
        cards_layout.addWidget(card1)
        cards_layout.addWidget(card2)
        cards_layout.addWidget(card3)
        cards_layout.addWidget(card4)
        
        content_layout.addLayout(cards_layout)
        
        # 2. AÇÕES RÁPIDAS
        quick_actions_group = QGroupBox("⚡ AÇÕES RÁPIDAS")
        quick_actions_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        quick_layout = QHBoxLayout()
        
        btn_nova_cotacao = QPushButton("📦 NOVA COTAÇÃO")
        btn_nova_cotacao.setFixedHeight(60)
        btn_nova_cotacao.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        btn_nova_cotacao.clicked.connect(self.show_cotacao)
        
        btn_calculadora = QPushButton("🧮 CALCULADORA CUBAGEM")
        btn_calculadora.setFixedHeight(60)
        btn_calculadora.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        btn_calculadora.clicked.connect(self.show_calculadora)
        
        btn_transportadoras = QPushButton("🚛 TRANSPORTADORAS")
        btn_transportadoras.setFixedHeight(60)
        btn_transportadoras.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                border: none;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #9b59b6;
            }
        """)
        btn_transportadoras.clicked.connect(self.show_transportadoras)
        
        quick_layout.addWidget(btn_nova_cotacao)
        quick_layout.addWidget(btn_calculadora)
        quick_layout.addWidget(btn_transportadoras)
        quick_actions_group.setLayout(quick_layout)
        content_layout.addWidget(quick_actions_group)
        
        # 3. COTAÇÕES RECENTES
        recent_group = QGroupBox("🕒 COTAÇÕES MAIS RECENTES")
        recent_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        recent_layout = QVBoxLayout()
        
        # Tabela de cotações recentes do banco
        recent_table = QTableWidget()
        recent_table.setColumnCount(5)
        recent_table.setHorizontalHeaderLabels(["Data", "Fornecedor", "Valor NF", "Frete", "Transportadora"])
        
        cotacoes_recentes = dashboard_data.get('cotacoes_recentes', [])
        recent_table.setRowCount(len(cotacoes_recentes))
        
        for row, cotacao in enumerate(cotacoes_recentes):
            # Data
            data_item = QTableWidgetItem(cotacao['data'])
            recent_table.setItem(row, 0, data_item)
            
            # Fornecedor
            fornecedor_item = QTableWidgetItem(cotacao['fornecedor'])
            recent_table.setItem(row, 1, fornecedor_item)
            
            # Valor NF
            valor_nf = f"R$ {cotacao['valor_nf']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            valor_item = QTableWidgetItem(valor_nf)
            recent_table.setItem(row, 2, valor_item)
            
            # Frete
            if cotacao['valor_frete']:
                frete = f"R$ {cotacao['valor_frete']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            else:
                frete = "-"
            frete_item = QTableWidgetItem(frete)
            recent_table.setItem(row, 3, frete_item)
            
            # Transportadora
            transp_item = QTableWidgetItem(cotacao['transportadora'] or "-")
            recent_table.setItem(row, 4, transp_item)
        
        # Configurar header da tabela - CORREÇÃO AQUI
        header = recent_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        recent_table.setMaximumHeight(200)
        recent_layout.addWidget(recent_table)
        
        # Botão ver todas
        btn_ver_todas = QPushButton("📋 Ver Todas as Cotações")
        btn_ver_todas.clicked.connect(self.show_historico)
        recent_layout.addWidget(btn_ver_todas)
        
        recent_group.setLayout(recent_layout)
        content_layout.addWidget(recent_group)
        
        # 4. ESTATÍSTICAS RÁPIDAS
        stats_group = QGroupBox("📊 ESTATÍSTICAS")
        stats_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        stats_layout = QHBoxLayout()
        
        stats_left = QVBoxLayout()
        stats_right = QVBoxLayout()
        
        # Estatísticas à esquerda
        stats_left.addWidget(self.create_stat_item("📅 Cotações este mês:", str(dashboard_data.get('total_cotacoes_mes', 0))))
        
        valor_total = f"R$ {dashboard_data.get('valor_total_mes', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        stats_left.addWidget(self.create_stat_item("💰 Valor total NF:", valor_total))
        
        maior_valor = f"R$ {dashboard_data.get('maior_valor_nf', 0):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        stats_left.addWidget(self.create_stat_item("📦 Maior valor de NF:", maior_valor))
        
        # Estatísticas à direita  
        stats_right.addWidget(self.create_stat_item("🚛 Transportadoras ativas:", str(dashboard_data.get('total_transportadoras', 0))))
        stats_right.addWidget(self.create_stat_item("🏆 Transportadora mais usada:", dashboard_data.get('transp_mais_usada', 'Nenhuma')))
        stats_right.addWidget(self.create_stat_item("📈 Taxa média de frete:", f"{dashboard_data.get('taxa_media_frete', 0):.1f}%"))
        
        stats_layout.addLayout(stats_left)
        stats_layout.addLayout(stats_right)
        stats_group.setLayout(stats_layout)
        content_layout.addWidget(stats_group)
        
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)
        
        # Layout principal
        layout.addWidget(top_bar)
        layout.addWidget(scroll)
        
        page.setLayout(layout)
        return page

    def create_card(self, title, value, subtitle, color):
        """Cria um card de métrica"""
        card = QFrame()
        card.setFixedSize(180, 100)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 11px;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addStretch()
        card_layout.addWidget(subtitle_label)
        
        card.setLayout(card_layout)
        return card

    def create_stat_item(self, label, value):
        """Cria um item de estatística"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #2c3e50; font-size: 12px;")
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet("color: #27ae60; font-size: 12px; font-weight: bold;")
        
        layout.addWidget(label_widget)
        layout.addStretch()
        layout.addWidget(value_widget)
        
        widget.setLayout(layout)
        return widget

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