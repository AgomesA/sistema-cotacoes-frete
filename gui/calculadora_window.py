# calculadora_window.py - DESIGN PREMIUM
import sqlite3
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QGroupBox, QFormLayout,
                             QDoubleSpinBox, QComboBox, QScrollArea, QRadioButton,
                             QButtonGroup, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CalculadoraWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.itens = []
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface da calculadora com design premium"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Aplicar fundo gradiente
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ecf0f1, stop:1 #bdc3c7);")
        
        # Header premium
        header = QLabel("🧮 CALCULADORA DE CUBAGEM")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setStyleSheet("""
            color: white; 
            padding: 25px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8e44ad, stop:1 #9b59b6);
            border-bottom: 3px solid #7d3c98;
            margin-bottom: 0px;
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(25, 25, 25, 25)
        
        # Seção de configuração
        self.setup_configuracao(scroll_layout)
        
        # Seção da tabela
        self.setup_tabela(scroll_layout)
        
        # Seção de resultados
        self.setup_resultados(scroll_layout)
        
        # Botões de ação
        self.setup_botoes(scroll_layout)
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # Adiciona primeira linha automaticamente
        self.adicionar_linha()
    
    def setup_configuracao(self, layout):
        """Configura a seção de unidade de medida com design premium"""
        group = QGroupBox("⚙️ CONFIGURAÇÃO")
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
        
        config_layout = QHBoxLayout()
        config_layout.setSpacing(20)
        
        # Label
        label = QLabel("UNIDADE DE MEDIDA:")
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("color: #2c3e50;")
        
        # Radio buttons para unidade
        self.radio_cm = QRadioButton("📏 CENTÍMETROS (cm)")
        self.radio_cm.setFont(QFont("Arial", 11))
        self.radio_cm.setStyleSheet("""
            QRadioButton {
                color: #2c3e50;
                padding: 8px;
                background: #f8f9fa;
                border-radius: 6px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:checked {
                background-color: #3498db;
                border: 2px solid #2980b9;
            }
        """)
        
        self.radio_metros = QRadioButton("📐 METROS (m)")
        self.radio_metros.setFont(QFont("Arial", 11))
        self.radio_metros.setStyleSheet("""
            QRadioButton {
                color: #2c3e50;
                padding: 8px;
                background: #f8f9fa;
                border-radius: 6px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:checked {
                background-color: #3498db;
                border: 2px solid #2980b9;
            }
        """)
        
        # Grupo para os radios
        self.unidade_group = QButtonGroup()
        self.unidade_group.addButton(self.radio_cm)
        self.unidade_group.addButton(self.radio_metros)
        
        # Configura CM como padrão
        self.radio_cm.setChecked(True)
        
        # Conecta mudança de unidade
        self.radio_cm.toggled.connect(self.recalcular_tudo)
        self.radio_metros.toggled.connect(self.recalcular_tudo)
        
        config_layout.addWidget(label)
        config_layout.addWidget(self.radio_cm)
        config_layout.addWidget(self.radio_metros)
        config_layout.addStretch()
        
        group.setLayout(config_layout)
        layout.addWidget(group)
    
    def setup_tabela(self, layout):
        """Configura a tabela de itens com design premium"""
        group = QGroupBox("📦 DIMENSÕES DOS VOLUMES")
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
        group_layout.setSpacing(15)
        
        # Tabela premium
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels([
            "Item", "Quantidade", "Largura", "Comprimento", "Altura", "Total (m³)"
        ])
        
        # Estilo premium da tabela
        self.tabela.setStyleSheet("""
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
        
        # Configura larguras das colunas
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        group_layout.addWidget(self.tabela)
        
        # Botão para adicionar linha
        btn_adicionar = QPushButton("➕ ADICIONAR LINHA")
        btn_adicionar.setFixedHeight(45)
        btn_adicionar.setStyleSheet("""
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
        btn_adicionar.clicked.connect(self.adicionar_linha)
        group_layout.addWidget(btn_adicionar)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def setup_resultados(self, layout):
        """Configura a seção de resultados com design premium"""
        group = QGroupBox("📊 RESULTADO")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #2c3e50;
                border: 3px solid #2ecc71;
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
        
        result_layout = QVBoxLayout()
        
        # Total da cubagem
        result_item_layout = QHBoxLayout()
        label_total = QLabel("CUBAGEM TOTAL:")
        label_total.setFont(QFont("Arial", 14, QFont.Bold))
        label_total.setStyleSheet("color: #2c3e50;")
        
        self.label_total_valor = QLabel("0,000 m³")
        self.label_total_valor.setFont(QFont("Arial", 18, QFont.Bold))
        self.label_total_valor.setStyleSheet("""
            color: #27ae60; 
            background: #d5f4e6; 
            padding: 15px; 
            border: 2px solid #2ecc71;
            border-radius: 8px;
        """)
        self.label_total_valor.setAlignment(Qt.AlignCenter)
        
        result_item_layout.addWidget(label_total)
        result_item_layout.addWidget(self.label_total_valor)
        result_item_layout.addStretch()
        
        result_layout.addLayout(result_item_layout)
        group.setLayout(result_layout)
        layout.addWidget(group)
    
    def setup_botoes(self, layout):
        """Configura os botões de ação com design premium"""
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        # Botão Calcular
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
        btn_calcular.clicked.connect(self.calcular_tudo)
        
        # Botão Limpar
        btn_limpar = QPushButton("🔄 LIMPAR TUDO")
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
        btn_limpar.clicked.connect(self.limpar_tudo)
        
        # Botão Salvar
        btn_salvar = QPushButton("💾 SALVAR CÁLCULO")
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
        btn_salvar.clicked.connect(self.salvar_calculo)
        
        btn_layout.addWidget(btn_calcular)
        btn_layout.addWidget(btn_limpar)
        btn_layout.addWidget(btn_salvar)
        
        layout.addLayout(btn_layout)

    # MÉTODOS DE FUNCIONALIDADE
    def adicionar_linha(self):
        """Adiciona uma nova linha na tabela"""
        row = self.tabela.rowCount()
        self.tabela.insertRow(row)
        
        # Coluna 0: Número do item
        item_num = QTableWidgetItem(str(row + 1))
        item_num.setFlags(item_num.flags() & ~Qt.ItemIsEditable)
        item_num.setBackground(Qt.lightGray)
        self.tabela.setItem(row, 0, item_num)
        
        # Coluna 1: Quantidade
        quantidade_input = QLineEdit()
        quantidade_input.setPlaceholderText("1")
        quantidade_input.setText("1")
        quantidade_input.setStyleSheet("""
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
        quantidade_input.textChanged.connect(self.recalcular_linha)
        self.tabela.setCellWidget(row, 1, quantidade_input)
        
        # Coluna 2: Largura
        largura_input = QLineEdit()
        largura_input.setPlaceholderText("0")
        largura_input.setStyleSheet("""
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
        largura_input.textChanged.connect(self.recalcular_linha)
        self.tabela.setCellWidget(row, 2, largura_input)
        
        # Coluna 3: Comprimento
        comprimento_input = QLineEdit()
        comprimento_input.setPlaceholderText("0")
        comprimento_input.setStyleSheet("""
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
        comprimento_input.textChanged.connect(self.recalcular_linha)
        self.tabela.setCellWidget(row, 3, comprimento_input)
        
        # Coluna 4: Altura
        altura_input = QLineEdit()
        altura_input.setPlaceholderText("0")
        altura_input.setStyleSheet("""
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
        altura_input.textChanged.connect(self.recalcular_linha)
        self.tabela.setCellWidget(row, 4, altura_input)
        
        # Coluna 5: Total (readonly)
        total_item = QTableWidgetItem("0,000 m³")
        total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
        total_item.setBackground(Qt.lightGray)
        self.tabela.setItem(row, 5, total_item)
    
    def parse_number(self, text):
        """Converte texto para número, aceita . ou , como separador decimal"""
        if not text:
            return 0.0
        
        text = str(text).replace(',', '.').strip()
        try:
            return float(text) if text else 0.0
        except:
            return 0.0
    
    def recalcular_linha(self):
        """Recalcula uma linha específica quando os valores mudam"""
        for row in range(self.tabela.rowCount()):
            quantidade_input = self.tabela.cellWidget(row, 1)
            largura_input = self.tabela.cellWidget(row, 2)
            comprimento_input = self.tabela.cellWidget(row, 3)
            altura_input = self.tabela.cellWidget(row, 4)
            
            if (quantidade_input and largura_input and 
                comprimento_input and altura_input):
                
                # Pega os valores
                quantidade = self.parse_number(quantidade_input.text()) or 1
                largura = self.parse_number(largura_input.text())
                comprimento = self.parse_number(comprimento_input.text())
                altura = self.parse_number(altura_input.text())
                
                # Calcula o volume
                volume_unitario = largura * comprimento * altura
                volume_total = volume_unitario * quantidade
                
                # Converte para m³ se estiver em cm
                if self.radio_cm.isChecked():
                    volume_total /= 1000000  # cm³ para m³
                
                # Atualiza o total da linha
                total_item = self.tabela.item(row, 5)
                if total_item:
                    total_item.setText(f"{volume_total:.3f} m³")
        
        self.calcular_total()
    
    def recalcular_tudo(self):
        """Recalcula tudo quando a unidade muda"""
        for row in range(self.tabela.rowCount()):
            self.recalcular_linha()
    
    def calcular_tudo(self):
        """Força o cálculo de todas as linhas"""
        self.recalcular_tudo()
        QMessageBox.information(self, "Cálculo", "Cubagem calculada com sucesso!")
    
    def calcular_total(self):
        """Calcula o total geral de cubagem"""
        total_geral = 0.0
        
        for row in range(self.tabela.rowCount()):
            total_item = self.tabela.item(row, 5)
            if total_item and total_item.text():
                try:
                    valor = float(total_item.text().replace(' m³', '').replace(',', '.'))
                    total_geral += valor
                except:
                    pass
        
        self.label_total_valor.setText(f"{total_geral:.3f} m³")
    
    def limpar_tudo(self):
        """Limpa toda a tabela"""
        reply = QMessageBox.question(
            self, "Confirmar", 
            "Tem certeza que deseja limpar todos os dados?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.tabela.setRowCount(0)
            self.label_total_valor.setText("0,000 m³")
            # Adiciona uma linha vazia
            self.adicionar_linha()
    
    def salvar_calculo(self):
        """Salva o cálculo no banco de dados"""
        try:
            # Coleta todos os itens
            itens_data = []
            for row in range(self.tabela.rowCount()):
                quantidade_input = self.tabela.cellWidget(row, 1)
                largura_input = self.tabela.cellWidget(row, 2)
                comprimento_input = self.tabela.cellWidget(row, 3)
                altura_input = self.tabela.cellWidget(row, 4)
                total_item = self.tabela.item(row, 5)
                
                if (quantidade_input and largura_input and 
                    comprimento_input and altura_input and total_item):
                    
                    quantidade = self.parse_number(quantidade_input.text()) or 1
                    largura = self.parse_number(largura_input.text())
                    comprimento = self.parse_number(comprimento_input.text())
                    altura = self.parse_number(altura_input.text())
                    total = self.parse_number(total_item.text().replace(' m³', ''))
                    
                    itens_data.append({
                        'quantidade': quantidade,
                        'largura': largura,
                        'comprimento': comprimento,
                        'altura': altura,
                        'total': total
                    })
            
            cubagem_total = self.parse_number(self.label_total_valor.text().replace(' m³', ''))
            
            if not itens_data:
                QMessageBox.warning(self, "Aviso", "Não há dados para salvar!")
                return
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO calculos_cubagem (itens_json, cubagem_total)
                    VALUES (?, ?)
                ''', (
                    json.dumps(itens_data),
                    cubagem_total
                ))
                
                conn.commit()
                QMessageBox.information(self, "Sucesso", "Cálculo salvo com sucesso!")
                
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro", f"Erro ao salvar cálculo: {e}")
            finally:
                conn.close()
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro: {e}")