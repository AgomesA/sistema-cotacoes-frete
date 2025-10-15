# transportadoras_window.py - VERSÃO CORRIGIDA - LAYOUT OTIMIZADO
import sqlite3
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QGroupBox, QFormLayout,
                             QDoubleSpinBox, QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Formatters:
    @staticmethod
    def format_cnpj(cnpj):
        """Formata CNPJ para 00.000.000/0000-00"""
        cnpj = re.sub(r'[^\d]', '', cnpj)
        
        if len(cnpj) <= 2:
            return cnpj
        elif len(cnpj) <= 5:
            return f"{cnpj[:2]}.{cnpj[2:]}"
        elif len(cnpj) <= 8:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:]}"
        elif len(cnpj) <= 12:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:]}"
        else:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

    @staticmethod
    def format_telefone(telefone):
        """Formata telefone para (00) 00000-0000"""
        telefone = re.sub(r'[^\d]', '', telefone)
        
        if len(telefone) <= 2:
            return telefone
        elif len(telefone) <= 6:
            return f"({telefone[:2]}) {telefone[2:]}"
        elif len(telefone) <= 10:
            return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        else:
            return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:11]}"

class TransportadorasWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_transportadora_id = None
        self.telefones_widgets = []
        self.emails_widgets = []
        self.setup_ui()
        self.load_transportadoras()
    
    def setup_ui(self):
        """Configura a interface com layout responsivo"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # ✅ Margens reduzidas
        main_layout.setSpacing(10)  # ✅ Espaçamento reduzido
        self.setLayout(main_layout)
        
        # Aplicar fundo gradiente
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ecf0f1, stop:1 #bdc3c7);")
        
        # Painel esquerdo - Lista (40% da tela)
        self.setup_list_panel(main_layout)
        
        # Painel direito - Formulário (60% da tela)
        self.setup_form_panel(main_layout)
    
    def setup_list_panel(self, main_layout):
        """Configura o painel da lista com layout responsivo"""
        list_panel = QWidget()
        list_panel.setMaximumWidth(450)  # ✅ Largura máxima reduzida
        list_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_panel.setStyleSheet("""
            background: rgba(255,255,255,0.95); 
            border-radius: 8px;
            border: 1px solid #bdc3c7;
        """)
        
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(12, 12, 12, 12)  # ✅ Margens reduzidas
        list_layout.setSpacing(12)  # ✅ Espaçamento reduzido
        
        # Header
        header = QLabel("🚛 TRANSPORTADORAS")
        header.setFont(QFont("Arial", 14, QFont.Bold))  # ✅ Fonte menor
        header.setStyleSheet("""
            color: white;
            padding: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
            border-radius: 6px;
            margin-bottom: 8px;
        """)
        header.setAlignment(Qt.AlignCenter)
        list_layout.addWidget(header)
        
        # Botão Novo
        btn_novo = QPushButton("➕ NOVA TRANSPORTADORA")
        btn_novo.setFixedHeight(40)  # ✅ Altura reduzida
        btn_novo.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2ecc71, stop:1 #27ae60);
            }
        """)
        btn_novo.clicked.connect(self.nova_transportadora)
        list_layout.addWidget(btn_novo)
        
        # Tabela otimizada
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CNPJ"])
        
        # Estilo da tabela otimizado
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                gridline-color: #ecf0f1;
                font-size: 11px;
                font-family: Arial;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 6px 4px;
                border-bottom: 1px solid #ecf0f1;
                font-size: 11px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        header = self.table.horizontalHeader()
        
        # ✅ LARGURAS OTIMIZADAS - SEM BARRA DE ROLAGEM
        self.table.setColumnWidth(0, 50)   # ID menor
        self.table.setColumnWidth(1, 200)  # Nome reduzido
        self.table.setColumnWidth(2, 150)  # CNPJ reduzido
        
        # ✅ CONFIGURAÇÃO RESPONSIVA
        header.setSectionResizeMode(0, QHeaderView.Fixed)   # ID fixo
        header.setSectionResizeMode(1, QHeaderView.Stretch) # Nome expansível
        header.setSectionResizeMode(2, QHeaderView.Fixed)   # CNPJ fixo
        
        # Altura das linhas reduzida
        self.table.verticalHeader().setDefaultSectionSize(32)
        self.table.setAlternatingRowColors(True)
        
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellDoubleClicked.connect(self.editar_transportadora)
        list_layout.addWidget(self.table)
        
        list_panel.setLayout(list_layout)
        main_layout.addWidget(list_panel)
    
    def setup_form_panel(self, main_layout):
        """Configura o painel do formulário com layout compacto"""
        form_panel = QWidget()
        form_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_panel.setStyleSheet("background: transparent;")
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(8, 8, 8, 8)  # ✅ Margens reduzidas
        form_layout.setSpacing(8)  # ✅ Espaçamento reduzido
        
        # Header do formulário
        self.form_title = QLabel("CADASTRAR TRANSPORTADORA")
        self.form_title.setFont(QFont("Arial", 12, QFont.Bold))  # ✅ Fonte menor
        self.form_title.setStyleSheet("""
            color: white;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:1 #c0392b);
            border-radius: 6px;
        """)
        self.form_title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.form_title)
        
        # Scroll area otimizada
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none; 
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(8)  # ✅ Espaçamento reduzido
        scroll_layout.setContentsMargins(6, 6, 6, 6)  # ✅ Margens reduzidas
        
        # Grupo de dados básicos - MAIS COMPACTO
        basic_group = QGroupBox("📋 DADOS DA TRANSPORTADORA")
        basic_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 6px;
                padding: 0 6px 0 6px;
                background: white;
            }
        """)
        
        basic_layout = QFormLayout()
        basic_layout.setLabelAlignment(Qt.AlignRight)
        basic_layout.setVerticalSpacing(6)  # ✅ Reduzido
        basic_layout.setHorizontalSpacing(8)  # ✅ Reduzido
        basic_layout.setContentsMargins(8, 12, 8, 8)  # ✅ Margens reduzidas
        
        self.nome_input = QLineEdit()
        self.nome_input.setMaximumHeight(30)  # ✅ Altura reduzida
        self.nome_input.setStyleSheet("""
            QLineEdit {
                padding: 4px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        self.cnpj_input = QLineEdit()
        self.cnpj_input.setMaximumHeight(30)  # ✅ Altura reduzida
        self.cnpj_input.setStyleSheet("""
            QLineEdit {
                padding: 4px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        self.cnpj_input.textChanged.connect(self.format_cnpj_field)
        
        basic_layout.addRow("Nome*:", self.nome_input)
        basic_layout.addRow("CNPJ:", self.cnpj_input)
        
        basic_group.setLayout(basic_layout)
        scroll_layout.addWidget(basic_group)
        
        # Grupo de telefones - MAIS COMPACTO
        self.telefones_group = QGroupBox("📞 TELEFONES")
        self.telefones_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #2c3e50;
                border: 1px solid #27ae60;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 6px;
                padding: 0 6px 0 6px;
                background: white;
            }
        """)
        
        self.telefones_layout = QVBoxLayout()
        self.telefones_layout.setSpacing(4)  # ✅ Espaçamento reduzido
        self.telefones_layout.setContentsMargins(6, 8, 6, 6)  # ✅ Margens reduzidas
        
        self.btn_add_telefone = QPushButton("➕ Adicionar Telefone")
        self.btn_add_telefone.setFixedHeight(28)  # ✅ Altura reduzida
        self.btn_add_telefone.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                padding: 4px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background: #2ecc71;
            }
        """)
        self.btn_add_telefone.clicked.connect(lambda: self.adicionar_contato('telefone'))
        self.telefones_layout.addWidget(self.btn_add_telefone)
        
        self.telefones_group.setLayout(self.telefones_layout)
        scroll_layout.addWidget(self.telefones_group)
        
        # Grupo de emails - MAIS COMPACTO
        self.emails_group = QGroupBox("✉️ EMAILS")
        self.emails_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #2c3e50;
                border: 1px solid #e67e22;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 6px;
                padding: 0 6px 0 6px;
                background: white;
            }
        """)
        
        self.emails_layout = QVBoxLayout()
        self.emails_layout.setSpacing(4)  # ✅ Espaçamento reduzido
        self.emails_layout.setContentsMargins(6, 8, 6, 6)  # ✅ Margens reduzidas
        
        self.btn_add_email = QPushButton("➕ Adicionar Email")
        self.btn_add_email.setFixedHeight(28)  # ✅ Altura reduzida
        self.btn_add_email.setStyleSheet("""
            QPushButton {
                background: #e67e22;
                color: white;
                border: none;
                padding: 4px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background: #f39c12;
            }
        """)
        self.btn_add_email.clicked.connect(lambda: self.adicionar_contato('email'))
        self.emails_layout.addWidget(self.btn_add_email)
        
        self.emails_group.setLayout(self.emails_layout)
        scroll_layout.addWidget(self.emails_group)
        
        # Grupo Rodocargas - MAIS COMPACTO
        self.rodocargas_group = QGroupBox("⚙️ CONFIGURAÇÕES RODOCARGAS")
        self.rodocargas_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11px;
                color: #2c3e50;
                border: 1px solid #8e44ad;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 6px;
                padding: 0 6px 0 6px;
                background: white;
            }
        """)
        
        rodocargas_layout = QFormLayout()
        rodocargas_layout.setVerticalSpacing(4)  # ✅ Reduzido
        rodocargas_layout.setContentsMargins(6, 8, 6, 6)  # ✅ Margens reduzidas
        
        self.percentual_input = QDoubleSpinBox()
        self.percentual_input.setRange(0.1, 100.0)
        self.percentual_input.setSuffix(" %")
        self.percentual_input.setDecimals(1)
        self.percentual_input.setValue(14.0)
        self.percentual_input.setFixedHeight(26)  # ✅ Altura reduzida
        self.percentual_input.setStyleSheet("padding: 3px; border: 1px solid #bdc3c7; border-radius: 3px; font-size: 10px;")
        
        self.icms_input = QDoubleSpinBox()
        self.icms_input.setRange(0.0, 100.0)
        self.icms_input.setSuffix(" %")
        self.icms_input.setDecimals(1)
        self.icms_input.setValue(7.0)
        self.icms_input.setFixedHeight(26)  # ✅ Altura reduzida
        self.icms_input.setStyleSheet("padding: 3px; border: 1px solid #bdc3c7; border-radius: 3px; font-size: 10px;")
        
        rodocargas_layout.addRow("Percentual Base:", self.percentual_input)
        rodocargas_layout.addRow("ICMS:", self.icms_input)
        
        self.rodocargas_group.setLayout(rodocargas_layout)
        self.rodocargas_group.setVisible(False)
        scroll_layout.addWidget(self.rodocargas_group)
        
        # Botões de ação - MAIS COMPACTOS
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)  # ✅ Espaçamento reduzido
        
        self.btn_salvar = QPushButton("💾 SALVAR")
        self.btn_salvar.setFixedHeight(35)  # ✅ Altura reduzida
        self.btn_salvar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2ecc71, stop:1 #27ae60);
            }
        """)
        self.btn_salvar.clicked.connect(self.salvar_transportadora)
        
        self.btn_limpar = QPushButton("🔄 LIMPAR")
        self.btn_limpar.setFixedHeight(35)  # ✅ Altura reduzida
        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2980b9, stop:1 #3498db);
            }
        """)
        self.btn_limpar.clicked.connect(self.limpar_formulario)
        
        self.btn_excluir = QPushButton("🗑️ EXCLUIR")
        self.btn_excluir.setFixedHeight(35)  # ✅ Altura reduzida
        self.btn_excluir.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c0392b, stop:1 #e74c3c);
            }
        """)
        self.btn_excluir.clicked.connect(self.excluir_transportadora)
        self.btn_excluir.setVisible(False)
        
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_limpar)
        btn_layout.addWidget(self.btn_excluir)
        
        scroll_layout.addLayout(btn_layout)
        scroll_layout.addStretch()
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        form_layout.addWidget(scroll)
        
        form_panel.setLayout(form_layout)
        main_layout.addWidget(form_panel)

    # OS MÉTODOS RESTANTES PERMANECEM OS MESMOS (format_cnpj_field, adicionar_contato, etc.)
    # ... [mantenha todos os outros métodos exatamente como estavam]

    def format_cnpj_field(self, text):
        """Aplica formatação automática no campo de CNPJ"""
        cursor_position = self.cnpj_input.cursorPosition()
        formatted = Formatters.format_cnpj(text)
        
        if formatted != text:
            self.cnpj_input.setText(formatted)
            new_position = cursor_position + (len(formatted) - len(text))
            self.cnpj_input.setCursorPosition(min(new_position, len(formatted)))

    def format_telefone_field(self, field, text):
        """Aplica formatação automática no campo de telefone"""
        cursor_position = field.cursorPosition()
        formatted = Formatters.format_telefone(text)
        
        if formatted != text:
            field.setText(formatted)
            new_position = cursor_position + (len(formatted) - len(text))
            field.setCursorPosition(min(new_position, len(formatted)))

    def adicionar_contato(self, tipo, valor="", contato_nome=""):
        """Adiciona uma nova linha de contato (telefone ou email)"""
        if tipo == 'telefone':
            layout = self.telefones_layout
            widgets_list = self.telefones_widgets
            placeholder_valor = "(00) 00000-0000"
            placeholder_contato = "Nome do contato"
        else:
            layout = self.emails_layout
            widgets_list = self.emails_widgets
            placeholder_valor = "email@empresa.com"
            placeholder_contato = "Nome do contato"
        
        # Frame para cada linha de contato - MAIS COMPACTO
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame.setStyleSheet("""
            QFrame { 
                border: 1px solid #bdc3c7; 
                border-radius: 4px; 
                background: #f8f9fa; 
                margin: 2px;
            }
        """)
        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(4, 4, 4, 4)  # ✅ Margens reduzidas
        frame_layout.setSpacing(4)  # ✅ Espaçamento reduzido
        
        # Campo do valor (telefone/email)
        valor_input = QLineEdit()
        valor_input.setPlaceholderText(placeholder_valor)
        valor_input.setText(valor)
        valor_input.setMaximumHeight(24)  # ✅ Altura reduzida
        valor_input.setStyleSheet("""
            padding: 2px; 
            border: 1px solid #bdc3c7; 
            border-radius: 2px; 
            font-size: 10px;
        """)
        
        # Para telefones, adiciona formatação automática
        if tipo == 'telefone':
            valor_input.textChanged.connect(
                lambda text, field=valor_input: self.format_telefone_field(field, text)
            )
        
        # Campo do nome do contato
        contato_input = QLineEdit()
        contato_input.setPlaceholderText(placeholder_contato)
        contato_input.setText(contato_nome)
        contato_input.setMaximumHeight(24)  # ✅ Altura reduzida
        contato_input.setStyleSheet("""
            padding: 2px; 
            border: 1px solid #bdc3c7; 
            border-radius: 2px; 
            font-size: 10px;
        """)
        
        # Botão remover
        btn_remover = QPushButton("❌")
        btn_remover.setFixedSize(22, 22)  # ✅ Tamanho reduzido
        btn_remover.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 2px;
                font-size: 8px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        btn_remover.clicked.connect(lambda: self.remover_contato(frame, widgets_list))
        
        # ✅ LABELS MAIS COMPACTAS
        frame_layout.addWidget(QLabel("Nº:" if tipo == 'telefone' else "Email:"))
        frame_layout.addWidget(valor_input)
        frame_layout.addWidget(QLabel("Contato:"))
        frame_layout.addWidget(contato_input)
        frame_layout.addWidget(btn_remover)
        
        frame.setLayout(frame_layout)
        
        # Insere antes do botão "Adicionar"
        layout.insertWidget(layout.count() - 1, frame)
        
        # Guarda referência
        widgets_list.append({
            'frame': frame,
            'valor_input': valor_input,
            'contato_input': contato_input,
            'tipo': tipo
        })

    def remover_contato(self, frame, widgets_list):
        """Remove uma linha de contato"""
        for i, widget in enumerate(widgets_list):
            if widget['frame'] == frame:
                widget['frame'].deleteLater()
                widgets_list.pop(i)
                break

    def limpar_contatos(self):
        """Limpa todas as linhas de contatos"""
        # Limpa telefones
        for widget in self.telefones_widgets:
            widget['frame'].deleteLater()
        self.telefones_widgets.clear()
        
        # Limpa emails
        for widget in self.emails_widgets:
            widget['frame'].deleteLater()
        self.emails_widgets.clear()

    def load_transportadoras(self):
        """Carrega a lista de transportadoras do banco"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cnpj FROM transportadoras ORDER BY nome")
            transportadoras = cursor.fetchall()
            conn.close()
            
            self.table.setRowCount(len(transportadoras))
            
            for row, transp in enumerate(transportadoras):
                # ID
                id_item = QTableWidgetItem(str(transp[0]))
                id_item.setTextAlignment(Qt.AlignCenter)
                id_item.setFont(QFont("Arial", 10))  # ✅ Fonte menor
                self.table.setItem(row, 0, id_item)
                
                # Nome
                nome_item = QTableWidgetItem(transp[1])
                nome_item.setFont(QFont("Arial", 10))  # ✅ Fonte menor
                self.table.setItem(row, 1, nome_item)
                
                # CNPJ
                cnpj_item = QTableWidgetItem(transp[2] if transp[2] else "")
                cnpj_item.setTextAlignment(Qt.AlignCenter)
                cnpj_item.setFont(QFont("Arial", 9))  # ✅ Fonte menor
                self.table.setItem(row, 2, cnpj_item)
            
            # ✅ LARGURAS OTIMIZADAS
            self.table.setColumnWidth(0, 50)
            self.table.setColumnWidth(1, 200)  
            self.table.setColumnWidth(2, 150)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar transportadoras: {e}")

    def nova_transportadora(self):
        """Prepara o formulário para novo cadastro"""
        self.current_transportadora_id = None
        self.limpar_formulario()
        self.form_title.setText("CADASTRAR TRANSPORTADORA")
        self.btn_excluir.setVisible(False)
        self.rodocargas_group.setVisible(False)

    def editar_transportadora(self, row, column):
        """Carrega os dados da transportadora para edição"""
        try:
            transportadora_id = int(self.table.item(row, 0).text())
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Dados básicos
            cursor.execute('''
                SELECT id, nome, cnpj, percentual_base, icms 
                FROM transportadoras WHERE id = ?
            ''', (transportadora_id,))
            transp = cursor.fetchone()
            
            # Contatos
            cursor.execute('''
                SELECT tipo, valor, contato 
                FROM transportadora_contatos 
                WHERE transportadora_id = ? 
                ORDER BY tipo, id
            ''', (transportadora_id,))
            contatos = cursor.fetchall()
            
            conn.close()
            
            if transp:
                self.current_transportadora_id = transp[0]
                self.nome_input.setText(transp[1])
                self.cnpj_input.setText(transp[2] if transp[2] else "")
                
                # Limpa e carrega contatos
                self.limpar_contatos()
                for tipo, valor, contato in contatos:
                    if tipo == 'telefone':
                        self.adicionar_contato('telefone', valor, contato)
                    elif tipo == 'email':
                        self.adicionar_contato('email', valor, contato)
                
                # Configurações Rodocargas
                is_rodocargas = transp[1].lower() == "rodocargas"
                self.rodocargas_group.setVisible(is_rodocargas)
                
                if is_rodocargas:
                    self.percentual_input.setValue(transp[3] if transp[3] else 14.0)
                    self.icms_input.setValue(transp[4] if transp[4] else 7.0)
                
                self.form_title.setText(f"EDITAR: {transp[1]}")
                self.btn_excluir.setVisible(True)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar transportadora: {e}")

    def salvar_transportadora(self):
        """Salva ou atualiza uma transportadora"""
        try:
            nome = self.nome_input.text().strip()
            if not nome:
                QMessageBox.warning(self, "Aviso", "O nome da transportadora é obrigatório!")
                return
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            try:
                if self.current_transportadora_id is None:
                    # NOVO CADASTRO
                    cursor.execute('''
                        INSERT INTO transportadoras (nome, cnpj, percentual_base, icms)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        nome,
                        self.cnpj_input.text() or None,
                        self.percentual_input.value() if nome.lower() == "rodocargas" else 0,
                        self.icms_input.value() if nome.lower() == "rodocargas" else 0
                    ))
                    transportadora_id = cursor.lastrowid
                    message = "Transportadora cadastrada com sucesso!"
                else:
                    # EDIÇÃO
                    transportadora_id = self.current_transportadora_id
                    cursor.execute('''
                        UPDATE transportadoras 
                        SET nome=?, cnpj=?, percentual_base=?, icms=?
                        WHERE id=?
                    ''', (
                        nome,
                        self.cnpj_input.text() or None,
                        self.percentual_input.value() if nome.lower() == "rodocargas" else 0,
                        self.icms_input.value() if nome.lower() == "rodocargas" else 0,
                        transportadora_id
                    ))
                    message = "Transportadora atualizada com sucesso!"
                
                # Salva contatos (telefones)
                cursor.execute("DELETE FROM transportadora_contatos WHERE transportadora_id = ?", (transportadora_id,))
                
                for widget in self.telefones_widgets:
                    valor = widget['valor_input'].text().strip()
                    contato = widget['contato_input'].text().strip()
                    if valor:
                        cursor.execute('''
                            INSERT INTO transportadora_contatos (transportadora_id, tipo, valor, contato)
                            VALUES (?, ?, ?, ?)
                        ''', (transportadora_id, 'telefone', valor, contato or None))
                
                # Salva contatos (emails)
                for widget in self.emails_widgets:
                    valor = widget['valor_input'].text().strip()
                    contato = widget['contato_input'].text().strip()
                    if valor:
                        cursor.execute('''
                            INSERT INTO transportadora_contatos (transportadora_id, tipo, valor, contato)
                            VALUES (?, ?, ?, ?)
                        ''', (transportadora_id, 'email', valor, contato or None))
                
                conn.commit()
                QMessageBox.information(self, "Sucesso", message)
                
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Aviso", "CNPJ já cadastrado no sistema!")
                conn.rollback()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar transportadora: {e}")
                conn.rollback()
            finally:
                conn.close()
            
            self.load_transportadoras()
            self.nova_transportadora()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro de conexão: {e}")

    def excluir_transportadora(self):
        """Exclui a transportadora selecionada"""
        if self.current_transportadora_id is None:
            return
        
        reply = QMessageBox.question(
            self, "Confirmação", 
            "Tem certeza que deseja excluir esta transportadora?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                try:
                    # Exclui contatos primeiro
                    cursor.execute("DELETE FROM transportadora_contatos WHERE transportadora_id = ?", (self.current_transportadora_id,))
                    # Exclui transportadora
                    cursor.execute("DELETE FROM transportadoras WHERE id = ?", (self.current_transportadora_id,))
                    
                    conn.commit()
                    QMessageBox.information(self, "Sucesso", "Transportadora excluída com sucesso!")
                    
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao excluir transportadora: {e}")
                    conn.rollback()
                finally:
                    conn.close()
                
                self.load_transportadoras()
                self.nova_transportadora()
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro de conexão: {e}")

    def limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.nome_input.clear()
        self.cnpj_input.clear()
        self.percentual_input.setValue(14.0)
        self.icms_input.setValue(7.0)
        self.limpar_contatos()