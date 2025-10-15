# cotacao_window.py - DESIGN PREMIUM
import sqlite3
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QGroupBox, QFormLayout,
                             QDoubleSpinBox, QComboBox, QDateEdit, QScrollArea)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class CotacaoWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.transportadoras = []
        self.cotacao_data = []
        self.setup_ui()
        self.carregar_transportadoras()
    
    def setup_ui(self):
        """Configura a interface da tela de cotação com design premium"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Aplicar fundo gradiente
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ecf0f1, stop:1 #bdc3c7);")
        
        # Header premium
        header = QLabel("📦 NOVA COTAÇÃO")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("""
            color: white; 
            padding: 25px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:1 #c0392b);
            border-bottom: 3px solid #a23526;
            margin-bottom: 0px;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Scroll area para o formulário
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(25, 25, 25, 25)
        
        # Seção 1: Dados do Fornecedor
        self.setup_dados_fornecedor(scroll_layout)
        
        # Seção 2: Transportadoras e Fretes
        self.setup_transportadoras_fretes(scroll_layout)
        
        # Botões de ação
        self.setup_botoes_acao(scroll_layout)
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def setup_dados_fornecedor(self, layout):
        """Configura a seção de dados do fornecedor com design premium"""
        group = QGroupBox("📦 DADOS DO FORNECEDOR")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #2c3e50;
                border: 3px solid #3498db;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 15px 0 15px;
                background: white;
            }
        """)
        
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(25)
        
        # Data atual
        self.data_input = QDateEdit()
        self.data_input.setDate(QDate.currentDate())
        self.data_input.setCalendarPopup(True)
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setStyleSheet("""
            QDateEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
                background: white;
            }
            QDateEdit:focus {
                border-color: #3498db;
            }
        """)
        
        # Fornecedor
        self.fornecedor_input = QLineEdit()
        self.fornecedor_input.setPlaceholderText("Nome do fornecedor")
        self.fornecedor_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        # Nº Pedido
        self.pedido_input = QLineEdit()
        self.pedido_input.setPlaceholderText("Número do pedido")
        self.pedido_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        # Valor da NF
        self.valor_nf_input = QLineEdit()
        self.valor_nf_input.setPlaceholderText("Digite o valor da NF")
        self.valor_nf_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #27ae60;
            }
        """)
        self.valor_nf_input.textChanged.connect(self.on_valor_nf_changed)
        
        # Volume
        self.volume_input = QLineEdit()
        self.volume_input.setPlaceholderText("Quantidade de volumes")
        self.volume_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        # Peso
        self.peso_input = QLineEdit()
        self.peso_input.setPlaceholderText("Ex: 77,7")
        self.peso_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        # Cubagem
        self.cubagem_input = QLineEdit()
        self.cubagem_input.setPlaceholderText("Ex: 0,746")
        self.cubagem_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        form_layout.addRow("📅 Data:", self.data_input)
        form_layout.addRow("🏢 Fornecedor*:", self.fornecedor_input)
        form_layout.addRow("📋 Nº Pedido:", self.pedido_input)
        form_layout.addRow("💰 Valor NF*:", self.valor_nf_input)
        form_layout.addRow("📦 Volume:", self.volume_input)
        form_layout.addRow("⚖️ Peso:", self.peso_input)
        form_layout.addRow("📐 Cubagem:", self.cubagem_input)
        
        group.setLayout(form_layout)
        layout.addWidget(group)
    
    def setup_transportadoras_fretes(self, layout):
        """Configura a seção de transportadoras e fretes com design premium"""
        group = QGroupBox("🚛 TRANSPORTADORAS E FRETES")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #2c3e50;
                border: 3px solid #e67e22;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 15px 0 15px;
                background: white;
            }
        """)
        
        group_layout = QVBoxLayout()
        
        # Tabela de transportadoras premium
        self.table_transportadoras = QTableWidget()
        self.table_transportadoras.setColumnCount(5)
        self.table_transportadoras.setHorizontalHeaderLabels([
            "Transportadora", "Valor Frete", "Percentual", "Cálculo", "Ação"
        ])
        
        # Estilo premium da tabela
        self.table_transportadoras.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
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
        
        header = self.table_transportadoras.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        group_layout.addWidget(self.table_transportadoras)
        
        # Info da Rodocargas
        self.rodocargas_info = QLabel("")
        self.rodocargas_info.setStyleSheet("""
            color: #c0392b; 
            font-weight: bold; 
            font-size: 12px; 
            padding: 12px; 
            background: #fadbd8; 
            border: 2px solid #e74c3c;
            border-radius: 8px;
            margin: 10px;
        """)
        self.rodocargas_info.setVisible(False)
        group_layout.addWidget(self.rodocargas_info)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def setup_botoes_acao(self, layout):
        """Configura os botões de ação com design premium"""
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        btn_calcular = QPushButton("🧮 CALCULAR")
        btn_calcular.setFixedHeight(50)
        btn_calcular.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2980b9, stop:1 #3498db);
                border: 2px solid rgba(255,255,255,0.3);
            }
        """)
        btn_calcular.clicked.connect(self.calcular_fretes)
        
        btn_limpar = QPushButton("🔄 LIMPAR")
        btn_limpar.setFixedHeight(50)
        btn_limpar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e67e22, stop:1 #d35400);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #d35400, stop:1 #e67e22);
                border: 2px solid rgba(255,255,255,0.3);
            }
        """)
        btn_limpar.clicked.connect(self.limpar_formulario)
        
        btn_salvar = QPushButton("💾 SALVAR COTAÇÃO")
        btn_salvar.setFixedHeight(50)
        btn_salvar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2ecc71, stop:1 #27ae60);
                border: 2px solid rgba(255,255,255,0.3);
            }
        """)
        btn_salvar.clicked.connect(self.salvar_cotacao)
        
        btn_layout.addWidget(btn_calcular)
        btn_layout.addWidget(btn_limpar)
        btn_layout.addWidget(btn_salvar)
        
        layout.addLayout(btn_layout)

    # MÉTODOS DE FUNCIONALIDADE (mantenha os mesmos do código original)
    def formatar_moeda(self, valor):
        """Formata qualquer valor digitado para moeda"""
        try:
            texto_limpo = re.sub(r'[^\d]', '', str(valor))
            if not texto_limpo:
                return ""
            
            numero = float(texto_limpo) / 100
            return f"R$ {numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return ""

    def on_valor_nf_changed(self, texto):
        """Formata qualquer valor digitado e calcula Rodocargas"""
        if not texto:
            self.limpar_rodocargas()
            return
        
        texto_formatado = self.formatar_moeda(texto)
        if texto_formatado and texto_formatado != texto:
            self.valor_nf_input.blockSignals(True)
            self.valor_nf_input.setText(texto_formatado)
            self.valor_nf_input.setCursorPosition(len(texto_formatado))
            self.valor_nf_input.blockSignals(False)
        
        self.calcular_rodocargas_automatico()

    def parse_number(self, text):
        """Converte texto para número"""
        if not text:
            return 0.0
        
        try:
            text = str(text).replace('R$', '').replace(' ', '').strip()
            
            if '.' in text and text.count('.') == 1:
                partes = text.split('.')
                if len(partes) == 2 and partes[1].isdigit():
                    return float(text)
            
            text = text.replace('.', '').replace(',', '.')
            return float(text) if text else 0.0
        except:
            return 0.0

    def get_valor_nf_numerico(self):
        """Retorna o valor da NF como número"""
        return self.parse_number(self.valor_nf_input.text())
    
    def get_peso_numerico(self):
        return self.parse_number(self.peso_input.text())
    
    def get_cubagem_numerico(self):
        return self.parse_number(self.cubagem_input.text())

    def carregar_transportadoras(self):
        """Carrega transportadoras do banco"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, nome, cnpj, percentual_base, icms FROM transportadoras ORDER BY nome')
            self.transportadoras = cursor.fetchall()
            conn.close()
            self.atualizar_tabela_transportadoras()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar transportadoras: {e}")

    def atualizar_tabela_transportadoras(self):
        """Atualiza a tabela de transportadoras"""
        self.table_transportadoras.setRowCount(len(self.transportadoras))
        
        for row, transp in enumerate(self.transportadoras):
            # Nome
            nome_item = QTableWidgetItem(transp[1])
            nome_item.setFlags(nome_item.flags() & ~Qt.ItemIsEditable)
            self.table_transportadoras.setItem(row, 0, nome_item)
            
            # Valor Frete
            if transp[1].lower() == "rodocargas":
                valor_label = QLabel("")
                valor_label.setStyleSheet("""
                    font-weight: bold; 
                    color: #2c3e50; 
                    background-color: #f8f9fa; 
                    padding: 8px;
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                """)
                valor_label.setAlignment(Qt.AlignCenter)
                self.table_transportadoras.setCellWidget(row, 1, valor_label)
            else:
                valor_input = QLineEdit()
                valor_input.setPlaceholderText("Digite o valor")
                valor_input.setStyleSheet("""
                    QLineEdit {
                        padding: 8px;
                        border: 1px solid #bdc3c7;
                        border-radius: 4px;
                        font-size: 11px;
                    }
                    QLineEdit:focus {
                        border-color: #3498db;
                    }
                """)
                valor_input.textChanged.connect(lambda text, r=row: self.on_valor_frete_changed(text, r))
                self.table_transportadoras.setCellWidget(row, 1, valor_input)
            
            # Percentual
            percentual_item = QTableWidgetItem("0,00%")
            percentual_item.setFlags(percentual_item.flags() & ~Qt.ItemIsEditable)
            self.table_transportadoras.setItem(row, 2, percentual_item)
            
            # Cálculo
            calculo_item = QTableWidgetItem("")
            calculo_item.setFlags(calculo_item.flags() & ~Qt.ItemIsEditable)
            self.table_transportadoras.setItem(row, 3, calculo_item)
            
            # Botão Selecionar
            btn_selecionar = QPushButton("SELECIONAR")
            btn_selecionar.setFixedWidth(100)
            btn_selecionar.setStyleSheet("""
                QPushButton {
                    background: #95a5a6;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    font-weight: bold;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background: #7f8c8d;
                }
            """)
            btn_selecionar.clicked.connect(lambda checked, r=row: self.selecionar_transportadora(r))
            self.table_transportadoras.setCellWidget(row, 4, btn_selecionar)

    def on_valor_frete_changed(self, texto, row):
        """Formata qualquer valor digitado nos campos de frete"""
        if not texto:
            self.atualizar_calculos(row)
            return
        
        texto_formatado = self.formatar_moeda(texto)
        if texto_formatado and texto_formatado != texto:
            valor_input = self.table_transportadoras.cellWidget(row, 1)
            if valor_input:
                valor_input.blockSignals(True)
                valor_input.setText(texto_formatado)
                valor_input.setCursorPosition(len(texto_formatado))
                valor_input.blockSignals(False)
        
        self.atualizar_calculos(row)

    def limpar_rodocargas(self):
        """Limpa o valor da Rodocargas"""
        for row, transp in enumerate(self.transportadoras):
            if transp[1].lower() == "rodocargas":
                valor_label = self.table_transportadoras.cellWidget(row, 1)
                if valor_label:
                    valor_label.clear()
                self.table_transportadoras.item(row, 2).setText("0,00%")
                self.table_transportadoras.item(row, 3).setText("")
                self.rodocargas_info.setVisible(False)
                break

    def calcular_rodocargas_automatico(self):
        """Calcula Rodocargas automaticamente"""
        valor_nf = self.get_valor_nf_numerico()
        
        if valor_nf <= 0:
            self.limpar_rodocargas()
            return
        
        for row, transp in enumerate(self.transportadoras):
            if transp[1].lower() == "rodocargas":
                percentual_base = transp[3] or 14.0
                icms = transp[4] or 7.0
                
                valor_percentual = valor_nf * (percentual_base / 100)
                valor_icms = valor_percentual * (icms / 100)
                valor_total = valor_percentual + valor_icms
                
                valor_label = self.table_transportadoras.cellWidget(row, 1)
                if valor_label:
                    valor_formatado = f"R$ {valor_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    valor_label.setText(valor_formatado)
                
                self.atualizar_calculos(row)
                break

    def atualizar_calculos(self, row):
        """Atualiza os cálculos"""
        try:
            valor_nf = self.get_valor_nf_numerico()
            
            if valor_nf <= 0:
                self.table_transportadoras.item(row, 2).setText("0,00%")
                self.table_transportadoras.item(row, 3).setText("")
                return
            
            transportadora = self.transportadoras[row]
            valor_frete = 0.0
            
            if transportadora[1].lower() == "rodocargas":
                valor_label = self.table_transportadoras.cellWidget(row, 1)
                if valor_label and valor_label.text():
                    valor_frete = self.parse_number(valor_label.text())
            else:
                valor_input = self.table_transportadoras.cellWidget(row, 1)
                if valor_input and valor_input.text():
                    valor_frete = self.parse_number(valor_input.text())
            
            if valor_frete <= 0:
                self.table_transportadoras.item(row, 2).setText("0,00%")
                self.table_transportadoras.item(row, 3).setText("")
                return
            
            percentual = (valor_frete / valor_nf) * 100
            self.table_transportadoras.item(row, 2).setText(f"{percentual:.2f}%".replace('.', ','))
            
            detalhes = f"({valor_frete:.2f} / {valor_nf:.2f}) × 100 = {percentual:.2f}%"
            detalhes = detalhes.replace('.', ',')
            self.table_transportadoras.item(row, 3).setText(detalhes)
            
            if transportadora[1].lower() == "rodocargas":
                info_text = f"Rodocargas: {transportadora[3] or 14}% + {transportadora[4] or 7}% ICMS = R$ {valor_frete:.2f}"
                info_text = info_text.replace('.', ',')
                self.rodocargas_info.setText(info_text)
                self.rodocargas_info.setVisible(True)
                    
        except Exception as e:
            self.table_transportadoras.item(row, 2).setText("Erro")

    def selecionar_transportadora(self, row):
        """Seleciona transportadora"""
        for i in range(self.table_transportadoras.rowCount()):
            btn = self.table_transportadoras.cellWidget(i, 4)
            if btn:
                btn.setText("SELECIONAR")
                btn.setStyleSheet("""
                    QPushButton {
                        background: #95a5a6;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px;
                        font-weight: bold;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        background: #7f8c8d;
                    }
                """)
        
        btn_selecionado = self.table_transportadoras.cellWidget(row, 4)
        btn_selecionado.setText("🥇 SELECIONADA")
        btn_selecionado.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
                font-size: 10px;
            }
        """)
        
        self.transportadora_selecionada_id = self.transportadoras[row][0]

    def calcular_fretes(self):
        """Calcula todos os fretes"""
        valor_nf = self.get_valor_nf_numerico()
        if valor_nf <= 0:
            QMessageBox.warning(self, "Aviso", "Informe o valor da NF para calcular!")
            return
        
        self.calcular_rodocargas_automatico()
        
        for row in range(self.table_transportadoras.rowCount()):
            self.atualizar_calculos(row)

    def salvar_cotacao(self):
        """Salva a cotação"""
        try:
            fornecedor = self.fornecedor_input.text().strip()
            if not fornecedor:
                QMessageBox.warning(self, "Aviso", "Informe o fornecedor!")
                return
            
            valor_nf = self.get_valor_nf_numerico()
            if valor_nf <= 0:
                QMessageBox.warning(self, "Aviso", "Informe o valor da NF!")
                return
            
            fretes_data = []
            for row in range(self.table_transportadoras.rowCount()):
                transportadora = self.transportadoras[row]
                valor_frete = 0.0
                
                if transportadora[1].lower() == "rodocargas":
                    valor_label = self.table_transportadoras.cellWidget(row, 1)
                    if valor_label and valor_label.text():
                        valor_frete = self.parse_number(valor_label.text())
                else:
                    valor_input = self.table_transportadoras.cellWidget(row, 1)
                    if valor_input and valor_input.text():
                        valor_frete = self.parse_number(valor_input.text())
                
                if valor_frete > 0:
                    selecionada = (hasattr(self, 'transportadora_selecionada_id') and 
                                 self.transportadora_selecionada_id == transportadora[0])
                    
                    fretes_data.append({
                        'transportadora_id': transportadora[0],
                        'valor_frete': valor_frete,
                        'selecionada': selecionada
                    })
            
            if not fretes_data:
                QMessageBox.warning(self, "Aviso", "Informe pelo menos um valor de frete!")
                return
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO cotacoes 
                    (data, fornecedor, num_pedido, valor_nf, peso, volume, cubagem, transportadora_ganhadora_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.data_input.date().toString("yyyy-MM-dd"),
                    fornecedor,
                    self.pedido_input.text() or None,
                    valor_nf,
                    self.get_peso_numerico(),
                    int(self.volume_input.text()) if self.volume_input.text().isdigit() else None,
                    self.get_cubagem_numerico(),
                    self.transportadora_selecionada_id if hasattr(self, 'transportadora_selecionada_id') else None
                ))
                
                cotacao_id = cursor.lastrowid
                
                for frete in fretes_data:
                    cursor.execute('''
                        INSERT INTO cotacoes_transportadoras 
                        (cotacao_id, transportadora_id, valor_frete, selecionada)
                        VALUES (?, ?, ?, ?)
                    ''', (cotacao_id, frete['transportadora_id'], frete['valor_frete'], frete['selecionada']))
                
                conn.commit()
                QMessageBox.information(self, "Sucesso", "Cotação salva com sucesso!")
                self.limpar_formulario()
                
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")
            finally:
                conn.close()
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro: {e}")

    def limpar_formulario(self):
        """Limpa todo o formulário"""
        self.data_input.setDate(QDate.currentDate())
        self.fornecedor_input.clear()
        self.pedido_input.clear()
        self.valor_nf_input.clear()
        self.volume_input.clear()
        self.peso_input.clear()
        self.cubagem_input.clear()
        self.rodocargas_info.setVisible(False)
        
        for row in range(self.table_transportadoras.rowCount()):
            transportadora = self.transportadoras[row]
            
            if transportadora[1].lower() == "rodocargas":
                valor_label = self.table_transportadoras.cellWidget(row, 1)
                if valor_label:
                    valor_label.clear()
            else:
                valor_input = self.table_transportadoras.cellWidget(row, 1)
                if valor_input:
                    valor_input.clear()
            
            self.table_transportadoras.item(row, 2).setText("0,00%")
            self.table_transportadoras.item(row, 3).setText("")
            
            btn = self.table_transportadoras.cellWidget(row, 4)
            if btn:
                btn.setText("SELECIONAR")
                btn.setStyleSheet("""
                    QPushButton {
                        background: #95a5a6;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px;
                        font-weight: bold;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        background: #7f8c8d;
                    }
                """)
        
        if hasattr(self, 'transportadora_selecionada_id'):
            del self.transportadora_selecionada_id