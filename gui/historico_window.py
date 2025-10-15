# historico_window.py - DESIGN PREMIUM COMPLETO E FUNCIONAL
import sqlite3
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QGroupBox, QFormLayout,
                             QDateEdit, QScrollArea, QFrame, QSplitter, QComboBox,
                             QDialog, QDialogButtonBox, QTabWidget, QTextEdit,
                             QInputDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
import pandas as pd

class EditarCotacaoDialog(QDialog):
    def __init__(self, db, cotacao_id, parent=None):
        super().__init__(parent)
        self.db = db
        self.cotacao_id = cotacao_id
        self.transportadoras_originais = []
        self.setup_ui()
        self.carregar_dados()
    
    def setup_ui(self):
        self.setWindowTitle(f"✏️ Editar Cotação #{self.cotacao_id}")
        self.setModal(True)
        self.resize(900, 700)
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ecf0f1, stop:1 #bdc3c7);")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel(f"EDITAR COTAÇÃO #{self.cotacao_id}")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("""
            color: white; 
            padding: 20px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
            border-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background: white;
            }
            QTabBar::tab {
                background: #95a5a6;
                color: white;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #3498db;
            }
        """)
        
        self.tab_dados = QWidget()
        self.setup_tab_dados()
        tabs.addTab(self.tab_dados, "📦 Dados do Fornecedor")
        
        self.tab_transportadoras = QWidget()
        self.setup_tab_transportadoras()
        tabs.addTab(self.tab_transportadoras, "🚛 Transportadoras")
        
        layout.addWidget(tabs)
        
        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("💾 Salvar Alterações")
        btn_salvar.setFixedHeight(45)
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
            }
        """)
        btn_salvar.clicked.connect(self.salvar_alteracoes)
        
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.setFixedHeight(45)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #c0392b, stop:1 #e74c3c);
            }
        """)
        btn_cancelar.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def setup_tab_dados(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(20)
        
        self.data_input = QDateEdit()
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        self.fornecedor_input = QLineEdit()
        self.fornecedor_input.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        self.pedido_input = QLineEdit()
        self.pedido_input.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        self.valor_nf_input = QLineEdit()
        self.valor_nf_input.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        self.peso_input = QLineEdit()
        self.peso_input.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        self.volume_input = QLineEdit()
        self.volume_input.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        self.cubagem_input = QLineEdit()
        self.cubagem_input.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        self.ganhadora_combo = QComboBox()
        self.ganhadora_combo.setStyleSheet("padding: 10px; border: 2px solid #bdc3c7; border-radius: 6px;")
        
        layout.addRow("📅 Data:", self.data_input)
        layout.addRow("🏢 Fornecedor*:", self.fornecedor_input)
        layout.addRow("📋 Nº Pedido:", self.pedido_input)
        layout.addRow("💰 Valor NF*:", self.valor_nf_input)
        layout.addRow("⚖️ Peso:", self.peso_input)
        layout.addRow("📦 Volume:", self.volume_input)
        layout.addRow("📐 Cubagem:", self.cubagem_input)
        layout.addRow("🏆 Transportadora Ganhadora:", self.ganhadora_combo)
        
        self.tab_dados.setLayout(layout)
    
    def setup_tab_transportadoras(self):
        layout = QVBoxLayout()
        
        self.tabela_transportadoras = QTableWidget()
        self.tabela_transportadoras.setColumnCount(4)
        self.tabela_transportadoras.setHorizontalHeaderLabels([
            "Transportadora", "Valor Frete", "Ação", "Selecionada"
        ])
        
        self.tabela_transportadoras.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                gridline-color: #ecf0f1;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
        """)
        
        header = self.tabela_transportadoras.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.tabela_transportadoras)
        
        btn_add = QPushButton("➕ Adicionar Transportadora")
        btn_add.setFixedHeight(40)
        btn_add.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        btn_add.clicked.connect(self.adicionar_transportadora)
        layout.addWidget(btn_add)
        
        self.tab_transportadoras.setLayout(layout)
    
    def carregar_dados(self):
        """Carrega os dados da cotação para edição"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT data, fornecedor, num_pedido, valor_nf, peso, volume, cubagem, transportadora_ganhadora_id
                FROM cotacoes WHERE id = ?
            ''', (self.cotacao_id,))
            cotacao = cursor.fetchone()
            
            cursor.execute('SELECT id, nome FROM transportadoras ORDER BY nome')
            todas_transportadoras = cursor.fetchall()
            
            cursor.execute('''
                SELECT ct.transportadora_id, t.nome, ct.valor_frete, ct.selecionada
                FROM cotacoes_transportadoras ct
                JOIN transportadoras t ON ct.transportadora_id = t.id
                WHERE ct.cotacao_id = ?
            ''', (self.cotacao_id,))
            self.transportadoras_originais = cursor.fetchall()
            
            conn.close()
            
            if cotacao:
                self.data_input.setDate(QDate.fromString(cotacao[0], "yyyy-MM-dd"))
                self.fornecedor_input.setText(cotacao[1])
                self.pedido_input.setText(cotacao[2] if cotacao[2] else "")
                self.valor_nf_input.setText(f"R$ {cotacao[3]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                self.peso_input.setText(str(cotacao[4]) if cotacao[4] else "")
                self.volume_input.setText(str(cotacao[5]) if cotacao[5] else "")
                self.cubagem_input.setText(str(cotacao[6]) if cotacao[6] else "")
                
                self.ganhadora_combo.addItem("Nenhuma", None)
                for transp_id, nome in todas_transportadoras:
                    self.ganhadora_combo.addItem(nome, transp_id)
                
                ganhadora_atual = cotacao[7]
                if ganhadora_atual:
                    index = self.ganhadora_combo.findData(ganhadora_atual)
                    if index >= 0:
                        self.ganhadora_combo.setCurrentIndex(index)
                
                self.carregar_transportadoras()
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados: {e}")
    
    def carregar_transportadoras(self):
        """Carrega as transportadoras na tabela"""
        self.tabela_transportadoras.setRowCount(len(self.transportadoras_originais))
        
        for row, transp in enumerate(self.transportadoras_originais):
            nome_item = QTableWidgetItem(transp[1])
            nome_item.setFlags(nome_item.flags() & ~Qt.ItemIsEditable)
            self.tabela_transportadoras.setItem(row, 0, nome_item)
            
            valor_item = QTableWidgetItem(f"R$ {transp[2]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            self.tabela_transportadoras.setItem(row, 1, valor_item)
            
            btn_remover = QPushButton("🗑️ Remover")
            btn_remover.setEnabled(transp[1].lower() != "rodocargas")
            btn_remover.setStyleSheet("""
                QPushButton {
                    background: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background: #c0392b;
                }
            """)
            btn_remover.clicked.connect(lambda checked, r=row: self.remover_transportadora(r))
            self.tabela_transportadoras.setCellWidget(row, 2, btn_remover)
            
            selecionada_item = QTableWidgetItem()
            selecionada_item.setCheckState(Qt.Checked if transp[3] else Qt.Unchecked)
            self.tabela_transportadoras.setItem(row, 3, selecionada_item)
    
    def adicionar_transportadora(self):
        """Adiciona uma nova transportadora à cotação"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Transportadora")
        dialog.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        combo = QComboBox()
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome FROM transportadoras ORDER BY nome')
        transportadoras = cursor.fetchall()
        conn.close()
        
        for transp_id, nome in transportadoras:
            if nome not in [t[1] for t in self.transportadoras_originais]:
                combo.addItem(nome, transp_id)
        
        if combo.count() == 0:
            QMessageBox.information(self, "Aviso", "Todas as transportadoras já foram adicionadas!")
            return
        
        valor_input = QLineEdit()
        valor_input.setPlaceholderText("Valor do frete")
        valor_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Adicionar")
        btn_ok.setStyleSheet("background: #27ae60; color: white; border: none; padding: 8px; border-radius: 4px;")
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background: #95a5a6; color: white; border: none; padding: 8px; border-radius: 4px;")
        
        btn_ok.clicked.connect(dialog.accept)
        btn_cancelar.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addWidget(QLabel("Transportadora:"))
        layout.addWidget(combo)
        layout.addWidget(QLabel("Valor do Frete:"))
        layout.addWidget(valor_input)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            transportadora_id = combo.currentData()
            nome = combo.currentText()
            valor_texto = valor_input.text()
            
            try:
                valor = float(valor_texto.replace('R$', '').replace('.', '').replace(',', '.').strip())
                self.transportadoras_originais.append((transportadora_id, nome, valor, False))
                self.carregar_transportadoras()
                
            except ValueError:
                QMessageBox.warning(self, "Aviso", "Valor do frete inválido!")
    
    def remover_transportadora(self, row):
        """Remove uma transportadora da cotação"""
        transportadora = self.transportadoras_originais[row]
        if transportadora[1].lower() == "rodocargas":
            QMessageBox.warning(self, "Aviso", "Não é possível remover a Rodocargas!")
            return
        
        reply = QMessageBox.question(
            self, "Confirmar", 
            f"Remover {transportadora[1]} desta cotação?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.transportadoras_originais.pop(row)
            self.carregar_transportadoras()
    
    def salvar_alteracoes(self):
        """Salva as alterações da cotação"""
        try:
            if not self.fornecedor_input.text().strip():
                QMessageBox.warning(self, "Aviso", "Informe o fornecedor!")
                return
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    UPDATE cotacoes SET
                    data=?, fornecedor=?, num_pedido=?, valor_nf=?, peso=?, volume=?, cubagem=?, transportadora_ganhadora_id=?
                    WHERE id=?
                ''', (
                    self.data_input.date().toString("yyyy-MM-dd"),
                    self.fornecedor_input.text(),
                    self.pedido_input.text() or None,
                    float(self.valor_nf_input.text().replace('R$', '').replace('.', '').replace(',', '.').strip()),
                    float(self.peso_input.text()) if self.peso_input.text() else None,
                    int(self.volume_input.text()) if self.volume_input.text() else None,
                    float(self.cubagem_input.text()) if self.cubagem_input.text() else None,
                    self.ganhadora_combo.currentData(),
                    self.cotacao_id
                ))
                
                cursor.execute('DELETE FROM cotacoes_transportadoras WHERE cotacao_id = ?', (self.cotacao_id,))
                
                for row in range(self.tabela_transportadoras.rowCount()):
                    nome = self.tabela_transportadoras.item(row, 0).text()
                    valor_texto = self.tabela_transportadoras.item(row, 1).text()
                    selecionada = self.tabela_transportadoras.item(row, 3).checkState() == Qt.Checked
                    
                    transp_id = None
                    for transp in self.transportadoras_originais:
                        if transp[1] == nome:
                            transp_id = transp[0]
                            break
                    
                    if transp_id:
                        valor = float(valor_texto.replace('R$', '').replace('.', '').replace(',', '.').strip())
                        cursor.execute('''
                            INSERT INTO cotacoes_transportadoras (cotacao_id, transportadora_id, valor_frete, selecionada)
                            VALUES (?, ?, ?, ?)
                        ''', (self.cotacao_id, transp_id, valor, selecionada))
                
                conn.commit()
                QMessageBox.information(self, "Sucesso", "Cotação atualizada com sucesso!")
                self.accept()
                
            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")
            finally:
                conn.close()
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro: {e}")

class HistoricoWindow(QWidget):  
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.cotacao_selecionada_id = None
        self.setup_ui()
        self.carregar_cotacoes()
    
    def setup_ui(self):
        """Configura a interface com design premium"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
        # Aplicar fundo gradiente
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ecf0f1, stop:1 #bdc3c7);")
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("QSplitter::handle { background: #95a5a6; }")
        
        self.setup_painel_lista(splitter)
        self.setup_painel_detalhes(splitter)
        
        splitter.setSizes([400, 600])
        main_layout.addWidget(splitter)
    
    def setup_painel_lista(self, splitter):
        """Configura o painel da lista com design premium"""
        painel_lista = QWidget()
        painel_lista.setStyleSheet("background: rgba(255,255,255,0.9);")
        
        layout_lista = QVBoxLayout()
        layout_lista.setContentsMargins(0, 0, 0, 0)
        layout_lista.setSpacing(0)
        
        # Splitter vertical
        splitter_vertical = QSplitter(Qt.Vertical)
        splitter_vertical.setChildrenCollapsible(False)
        splitter_vertical.setStyleSheet("QSplitter::handle { background: #95a5a6; }")
        
        # Parte superior fixa
        parte_superior = QWidget()
        parte_superior.setStyleSheet("background: white;")
        layout_superior = QVBoxLayout(parte_superior)
        layout_superior.setContentsMargins(15, 15, 15, 15)
        layout_superior.setSpacing(15)
        
        # Título
        title = QLabel("📋 HISTÓRICO DE COTAÇÕES")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white; 
            padding: 15px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
            border-radius: 10px;
        """)
        layout_superior.addWidget(title)
        
        # Filtros
        self.setup_filtros(layout_superior)
        
        # Parte inferior rolável (tabela)
        parte_inferior = QWidget()
        layout_inferior = QVBoxLayout(parte_inferior)
        layout_inferior.setContentsMargins(15, 15, 15, 15)
        layout_inferior.setSpacing(15)
        
        # Tabela de cotações premium
        self.tabela_cotacoes = QTableWidget()
        self.tabela_cotacoes.setColumnCount(10)
        self.tabela_cotacoes.setHorizontalHeaderLabels([
            "ID", "Data", "Fornecedor", "Valor NF", "Peso", "Volume", "Cubagem", 
            "Transportadora", "Frete", "Percentual do Frete"
        ])
        
        # Estilo premium da tabela
        self.tabela_cotacoes.setStyleSheet("""
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
        
        header = self.tabela_cotacoes.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)
        
        self.tabela_cotacoes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_cotacoes.cellClicked.connect(self.carregar_detalhes_cotacao)
        layout_inferior.addWidget(self.tabela_cotacoes)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        
        btn_atualizar = QPushButton("🔄 ATUALIZAR")
        btn_atualizar.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        btn_atualizar.clicked.connect(self.carregar_cotacoes)
        
        btn_limpar_filtros = QPushButton("🧹 LIMPAR FILTROS")
        btn_limpar_filtros.setStyleSheet("""
            QPushButton {
                background: #e67e22;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #d35400;
            }
        """)
        btn_limpar_filtros.clicked.connect(self.limpar_filtros)
        
        btn_exportar = QPushButton("📊 EXPORTAR EXCEL")
        btn_exportar.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2ecc71;
            }
        """)
        btn_exportar.clicked.connect(self.exportar_excel)
        
        btn_layout.addWidget(btn_atualizar)
        btn_layout.addWidget(btn_limpar_filtros)
        btn_layout.addWidget(btn_exportar)
        
        layout_inferior.addLayout(btn_layout)
        
        # Adiciona as partes ao splitter vertical
        splitter_vertical.addWidget(parte_superior)
        splitter_vertical.addWidget(parte_inferior)
        splitter_vertical.setSizes([200, 400])
        
        layout_lista.addWidget(splitter_vertical)
        painel_lista.setLayout(layout_lista)
        splitter.addWidget(painel_lista)
    
    def setup_filtros(self, layout):
        """Configura os filtros com design premium"""
        group_filtros = QGroupBox("🔍 FILTROS")
        group_filtros.setStyleSheet("""
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
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        layout_filtros = QVBoxLayout()
        
        linha_data = QHBoxLayout()
        linha_data.addWidget(QLabel("📅 Data:"))
        self.filtro_data_inicio = QDateEdit()
        self.filtro_data_inicio.setDate(QDate.currentDate().addDays(-30))
        self.filtro_data_inicio.setDisplayFormat("dd/MM/yyyy")
        self.filtro_data_inicio.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")
        self.filtro_data_inicio.dateChanged.connect(self.aplicar_filtros)
        
        self.filtro_data_fim = QDateEdit()
        self.filtro_data_fim.setDate(QDate.currentDate())
        self.filtro_data_fim.setDisplayFormat("dd/MM/yyyy")
        self.filtro_data_fim.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")
        self.filtro_data_fim.dateChanged.connect(self.aplicar_filtros)
        
        linha_data.addWidget(self.filtro_data_inicio)
        linha_data.addWidget(QLabel("até"))
        linha_data.addWidget(self.filtro_data_fim)
        linha_data.addStretch()
        
        linha_busca = QHBoxLayout()
        
        label_fornecedor = QLabel("🏢 Fornecedor:")
        self.filtro_fornecedor_input = QLineEdit()
        self.filtro_fornecedor_input.setPlaceholderText("Buscar fornecedor...")
        self.filtro_fornecedor_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")
        self.filtro_fornecedor_input.textChanged.connect(self.aplicar_filtros)
        
        label_transportadora = QLabel("🚛 Transportadora:")
        self.filtro_transportadora_input = QLineEdit()
        self.filtro_transportadora_input.setPlaceholderText("Buscar transportadora...")
        self.filtro_transportadora_input.setStyleSheet("padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px;")
        self.filtro_transportadora_input.textChanged.connect(self.aplicar_filtros)
        
        linha_busca.addWidget(label_fornecedor)
        linha_busca.addWidget(self.filtro_fornecedor_input)
        linha_busca.addWidget(label_transportadora)
        linha_busca.addWidget(self.filtro_transportadora_input)
        linha_busca.addStretch()
        
        layout_filtros.addLayout(linha_data)
        layout_filtros.addLayout(linha_busca)
        
        group_filtros.setLayout(layout_filtros)
        layout.addWidget(group_filtros)
    
    def setup_painel_detalhes(self, splitter):
        """Configura o painel de detalhes com design premium"""
        painel_detalhes = QWidget()
        painel_detalhes.setStyleSheet("background: rgba(255,255,255,0.9);")
        
        layout_detalhes = QVBoxLayout()
        layout_detalhes.setContentsMargins(0, 0, 0, 0)
        layout_detalhes.setSpacing(0)
        
        # Título dos detalhes
        self.titulo_detalhes = QLabel("👀 SELECIONE UMA COTAÇÃO")
        self.titulo_detalhes.setFont(QFont("Arial", 16, QFont.Bold))
        self.titulo_detalhes.setAlignment(Qt.AlignCenter)
        self.titulo_detalhes.setStyleSheet("""
            color: #7f8c8d; 
            padding: 20px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #95a5a6, stop:1 #7f8c8d);
            color: white;
            border-bottom: 3px solid #6c7a89;
        """)
        layout_detalhes.addWidget(self.titulo_detalhes)
        
        # Botões de ação
        self.botoes_acao_widget = QWidget()
        self.botoes_acao_widget.setFixedHeight(60)
        self.botoes_acao_widget.setStyleSheet("background: #f8f9fa; border-bottom: 1px solid #bdc3c7;")
        self.botoes_acao_layout = QHBoxLayout(self.botoes_acao_widget)
        self.botoes_acao_layout.setContentsMargins(15, 10, 15, 10)
        self.setup_botoes_acao()
        layout_detalhes.addWidget(self.botoes_acao_widget)
        
        # Área de conteúdo dos detalhes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.conteudo_detalhes = QWidget()
        self.layout_conteudo = QVBoxLayout(self.conteudo_detalhes)
        self.layout_conteudo.setContentsMargins(20, 20, 20, 20)
        self.layout_conteudo.setSpacing(15)
        
        # Label vazio inicial
        self.label_vazio = QLabel("Selecione uma cotação para visualizar os detalhes")
        self.label_vazio.setAlignment(Qt.AlignCenter)
        self.label_vazio.setStyleSheet("color: #95a5a6; font-size: 16px; padding: 50px;")
        self.layout_conteudo.addWidget(self.label_vazio)
        
        scroll_area.setWidget(self.conteudo_detalhes)
        layout_detalhes.addWidget(scroll_area)
        
        painel_detalhes.setLayout(layout_detalhes)
        splitter.addWidget(painel_detalhes)
    
    def setup_botoes_acao(self):
        """Configura os botões de ação com design premium"""
        # Limpa botões anteriores
        for i in reversed(range(self.botoes_acao_layout.count())): 
            item = self.botoes_acao_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        if self.cotacao_selecionada_id:
            btn_editar = QPushButton("✏️ EDITAR")
            btn_editar.setStyleSheet("""
                QPushButton {
                    background: #3498db;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #2980b9;
                }
            """)
            btn_editar.clicked.connect(self.editar_cotacao)
            
            btn_imprimir = QPushButton("🖨️ IMPRIMIR")
            btn_imprimir.setStyleSheet("""
                QPushButton {
                    background: #95a5a6;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #7f8c8d;
                }
            """)
            btn_imprimir.clicked.connect(self.imprimir_cotacao)
            
            btn_pdf = QPushButton("📄 EXPORTAR PDF")
            btn_pdf.setStyleSheet("""
                QPushButton {
                    background: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #c0392b;
                }
            """)
            btn_pdf.clicked.connect(self.exportar_pdf)
            
            btn_excel = QPushButton("📊 EXPORTAR EXCEL")
            btn_excel.setStyleSheet("""
                QPushButton {
                    background: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #2ecc71;
                }
            """)
            btn_excel.clicked.connect(self.exportar_excel_cotacao)
            
            btn_excluir = QPushButton("🗑️ EXCLUIR")
            btn_excluir.setStyleSheet("""
                QPushButton {
                    background: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #c0392b;
                }
            """)
            btn_excluir.clicked.connect(self.excluir_cotacao)
            
            self.botoes_acao_layout.addWidget(btn_editar)
            self.botoes_acao_layout.addWidget(btn_imprimir)
            self.botoes_acao_layout.addWidget(btn_pdf)
            self.botoes_acao_layout.addWidget(btn_excel)
            self.botoes_acao_layout.addWidget(btn_excluir)
        
        self.botoes_acao_layout.addStretch()

    # MÉTODOS DE FUNCIONALIDADE
    def carregar_cotacoes(self):
        """Carrega as cotações do banco"""
        try:
            self.aplicar_filtros()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar cotações: {e}")

    def aplicar_filtros(self):
        """Aplica os filtros na lista de cotações"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    c.id, 
                    c.data, 
                    c.fornecedor, 
                    c.valor_nf,
                    c.peso,
                    c.volume,
                    c.cubagem,
                    t.nome as transportadora_ganhadora,
                    ct.valor_frete
                FROM cotacoes c
                LEFT JOIN transportadoras t ON c.transportadora_ganhadora_id = t.id
                LEFT JOIN cotacoes_transportadoras ct ON c.id = ct.cotacao_id AND ct.selecionada = 1
                WHERE 1=1
            """
            params = []
            
            data_inicio = self.filtro_data_inicio.date().toString("yyyy-MM-dd")
            data_fim = self.filtro_data_fim.date().toString("yyyy-MM-dd")
            query += " AND c.data BETWEEN ? AND ?"
            params.extend([data_inicio, data_fim])
            
            fornecedor_filtro = self.filtro_fornecedor_input.text().strip()
            if fornecedor_filtro:
                query += " AND c.fornecedor LIKE ?"
                params.append(f"%{fornecedor_filtro}%")
            
            transportadora_filtro = self.filtro_transportadora_input.text().strip()
            if transportadora_filtro:
                query += " AND t.nome LIKE ?"
                params.append(f"%{transportadora_filtro}%")
            
            query += " ORDER BY c.data DESC, c.id DESC"
            
            cursor.execute(query, params)
            cotacoes = cursor.fetchall()
            conn.close()
            
            self.tabela_cotacoes.setRowCount(len(cotacoes))
            
            for row, cotacao in enumerate(cotacoes):
                # ID
                self.tabela_cotacoes.setItem(row, 0, QTableWidgetItem(str(cotacao[0])))
                
                # Data
                data_obj = QDate.fromString(cotacao[1], "yyyy-MM-dd")
                data_formatada = data_obj.toString("dd/MM/yyyy")
                self.tabela_cotacoes.setItem(row, 1, QTableWidgetItem(data_formatada))
                
                # Fornecedor
                self.tabela_cotacoes.setItem(row, 2, QTableWidgetItem(cotacao[2]))
                
                # Valor NF
                valor_nf = f"R$ {cotacao[3]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                self.tabela_cotacoes.setItem(row, 3, QTableWidgetItem(valor_nf))
                
                # Peso
                if cotacao[4]:
                    peso = f"{cotacao[4]:.3f} kg".replace('.', ',')
                    self.tabela_cotacoes.setItem(row, 4, QTableWidgetItem(peso))
                else:
                    self.tabela_cotacoes.setItem(row, 4, QTableWidgetItem("-"))
                
                # Volume
                if cotacao[5]:
                    self.tabela_cotacoes.setItem(row, 5, QTableWidgetItem(str(cotacao[5])))
                else:
                    self.tabela_cotacoes.setItem(row, 5, QTableWidgetItem("-"))
                
                # Cubagem
                if cotacao[6]:
                    cubagem = f"{cotacao[6]:.3f} m³".replace('.', ',')
                    self.tabela_cotacoes.setItem(row, 6, QTableWidgetItem(cubagem))
                else:
                    self.tabela_cotacoes.setItem(row, 6, QTableWidgetItem("-"))
                
                # Transportadora
                transportadora = cotacao[7] if cotacao[7] else "Nenhuma"
                self.tabela_cotacoes.setItem(row, 7, QTableWidgetItem(transportadora))
                
                # Frete
                if cotacao[8]:
                    valor_frete = f"R$ {cotacao[8]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                    self.tabela_cotacoes.setItem(row, 8, QTableWidgetItem(valor_frete))
                else:
                    self.tabela_cotacoes.setItem(row, 8, QTableWidgetItem("-"))
                
                # Percentual do Frete
                if cotacao[8] and cotacao[3] and cotacao[3] > 0:
                    percentual = (cotacao[8] / cotacao[3] * 100)
                    percentual_texto = f"{percentual:.2f}%"
                else:
                    percentual_texto = "-"
                
                self.tabela_cotacoes.setItem(row, 9, QTableWidgetItem(percentual_texto))
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar filtros: {e}")

    def carregar_detalhes_cotacao(self, row, column):
        """Carrega os detalhes da cotação selecionada"""
        try:
            cotacao_id = int(self.tabela_cotacoes.item(row, 0).text())
            self.cotacao_selecionada_id = cotacao_id
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    c.data, c.fornecedor, c.num_pedido, c.valor_nf, 
                    c.peso, c.volume, c.cubagem, t.nome as transportadora_ganhadora
                FROM cotacoes c
                LEFT JOIN transportadoras t ON c.transportadora_ganhadora_id = t.id
                WHERE c.id = ?
            ''', (cotacao_id,))
            cotacao = cursor.fetchone()
            
            cursor.execute('''
                SELECT 
                    t.nome, ct.valor_frete, ct.selecionada,
                    (ct.valor_frete / c.valor_nf * 100) as percentual
                FROM cotacoes_transportadoras ct
                JOIN transportadoras t ON ct.transportadora_id = t.id
                JOIN cotacoes c ON ct.cotacao_id = c.id
                WHERE ct.cotacao_id = ?
                ORDER BY ct.valor_frete
            ''', (cotacao_id,))
            transportadoras = cursor.fetchall()
            
            conn.close()
            
            if cotacao:
                self.mostrar_detalhes_cotacao(cotacao, transportadoras)
                self.setup_botoes_acao()
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar detalhes: {e}")

    def mostrar_detalhes_cotacao(self, cotacao, transportadoras):
        """Mostra os detalhes da cotação selecionada com design premium"""
        # Remove o label vazio se existir
        if self.label_vazio and self.label_vazio.parent():
            self.layout_conteudo.removeWidget(self.label_vazio)
            self.label_vazio.setParent(None)
            self.label_vazio = None
        
        # Limpa conteúdo anterior
        self.limpar_conteudo_detalhes()
        
        # Atualiza título
        data_obj = QDate.fromString(cotacao[0], "yyyy-MM-dd")
        data_formatada = data_obj.toString("dd/MM/yyyy")
        self.titulo_detalhes.setText(f"👀 COTAÇÃO #{self.cotacao_selecionada_id} - {data_formatada}")
        self.titulo_detalhes.setStyleSheet("""
            color: white; 
            padding: 20px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
            border-bottom: 3px solid #2471a3;
        """)
        
        # Grupo: Dados do Fornecedor
        group_fornecedor = QGroupBox("📦 DADOS DO FORNECEDOR")
        group_fornecedor.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        layout_fornecedor = QFormLayout()
        layout_fornecedor.setVerticalSpacing(10)
        layout_fornecedor.setHorizontalSpacing(20)
        
        layout_fornecedor.addRow("📅 Data:", QLabel(data_formatada))
        layout_fornecedor.addRow("🏢 Fornecedor:", QLabel(cotacao[1]))
        layout_fornecedor.addRow("📋 Nº Pedido:", QLabel(cotacao[2] if cotacao[2] else "-"))
        
        valor_nf = f"R$ {cotacao[3]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        layout_fornecedor.addRow("💰 Valor NF:", QLabel(valor_nf))
        
        if cotacao[4]:
            peso = f"{cotacao[4]:.3f} kg".replace('.', ',')
            layout_fornecedor.addRow("⚖️ Peso:", QLabel(peso))
        else:
            layout_fornecedor.addRow("⚖️ Peso:", QLabel("-"))
        
        if cotacao[5]:
            layout_fornecedor.addRow("📦 Volume:", QLabel(str(cotacao[5])))
        else:
            layout_fornecedor.addRow("📦 Volume:", QLabel("-"))
        
        if cotacao[6]:
            cubagem = f"{cotacao[6]:.3f} m³".replace('.', ',')
            layout_fornecedor.addRow("📐 Cubagem:", QLabel(cubagem))
        else:
            layout_fornecedor.addRow("📐 Cubagem:", QLabel("-"))
        
        transportadora_ganhadora = cotacao[7] if cotacao[7] else "Nenhuma selecionada"
        label_ganhadora = QLabel(transportadora_ganhadora)
        if cotacao[7]:
            label_ganhadora.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 12px; background: #d5f4e6; padding: 5px; border-radius: 4px;")
        else:
            label_ganhadora.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout_fornecedor.addRow("🏆 Transportadora Ganhadora:", label_ganhadora)
        
        group_fornecedor.setLayout(layout_fornecedor)
        self.layout_conteudo.addWidget(group_fornecedor)
        
        # Grupo: Comparação de Transportadoras
        group_comparacao = QGroupBox("🚛 COMPARAÇÃO DE TRANSPORTADORAS")
        group_comparacao.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #e67e22;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        layout_comparacao = QVBoxLayout()
        
        tabela_comparacao = QTableWidget()
        tabela_comparacao.setColumnCount(4)
        tabela_comparacao.setHorizontalHeaderLabels([
            "Transportadora", "Valor Frete", "Percentual", "Status"
        ])
        
        tabela_comparacao.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                gridline-color: #ecf0f1;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        tabela_comparacao.setRowCount(len(transportadoras))
        
        for row, transp in enumerate(transportadoras):
            # Transportadora
            nome_item = QTableWidgetItem(transp[0])
            tabela_comparacao.setItem(row, 0, nome_item)
            
            # Valor Frete
            valor_frete = f"R$ {transp[1]:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            valor_item = QTableWidgetItem(valor_frete)
            tabela_comparacao.setItem(row, 1, valor_item)
            
            # Percentual
            percentual = f"{transp[3]:.2f}%"
            percentual_item = QTableWidgetItem(percentual)
            tabela_comparacao.setItem(row, 2, percentual_item)
            
            # Status
            status = "🥇 SELECIONADA" if transp[2] else ""
            status_item = QTableWidgetItem(status)
            if transp[2]:
                status_item.setBackground(Qt.green)
                status_item.setForeground(Qt.white)
                status_item.setTextAlignment(Qt.AlignCenter)
            tabela_comparacao.setItem(row, 3, status_item)
        
        header_comp = tabela_comparacao.horizontalHeader()
        header_comp.setSectionResizeMode(0, QHeaderView.Stretch)
        header_comp.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header_comp.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header_comp.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        tabela_comparacao.setMinimumHeight(150)
        layout_comparacao.addWidget(tabela_comparacao)
        group_comparacao.setLayout(layout_comparacao)
        self.layout_conteudo.addWidget(group_comparacao)
        
        # Adiciona um stretch no final
        self.layout_conteudo.addStretch()

    def limpar_conteudo_detalhes(self):
        """Limpa completamente o conteúdo dos detalhes"""
        while self.layout_conteudo.count():
            item = self.layout_conteudo.takeAt(0)
            if item.widget():
                widget = item.widget()
                if widget != self.label_vazio:
                    widget.setParent(None)
                    widget.deleteLater()

    def editar_cotacao(self):
        """Abre a janela de edição da cotação"""
        if self.cotacao_selecionada_id:
            dialog = EditarCotacaoDialog(self.db, self.cotacao_selecionada_id, self)
            if dialog.exec_() == QDialog.Accepted:
                self.carregar_detalhes_cotacao(0, 0)
                self.carregar_cotacoes()

    def imprimir_cotacao(self):
        """Imprime a cotação selecionada"""
        if not self.cotacao_selecionada_id:
            QMessageBox.warning(self, "Aviso", "Selecione uma cotação para imprimir!")
            return
        
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            QMessageBox.information(self, "Impressão", f"Cotação #{self.cotacao_selecionada_id} enviada para impressão!")

    def exportar_pdf(self):
        """Exporta a cotação para PDF"""
        if not self.cotacao_selecionada_id:
            QMessageBox.warning(self, "Aviso", "Selecione uma cotação para exportar!")
            return
        
        QMessageBox.information(self, "PDF", f"Exportando cotação #{self.cotacao_selecionada_id} para PDF...")

    def exportar_excel_cotacao(self):
        """Exporta a cotação específica para Excel"""
        if not self.cotacao_selecionada_id:
            QMessageBox.warning(self, "Aviso", "Selecione uma cotação para exportar!")
            return
        
        try:
            conn = self.db.get_connection()
            
            df_cotacao = pd.read_sql(f'''
                SELECT 
                    c.id as "ID",
                    c.data as "Data",
                    c.fornecedor as "Fornecedor",
                    c.num_pedido as "Pedido",
                    c.valor_nf as "Valor NF",
                    c.peso as "Peso",
                    c.volume as "Volume",
                    c.cubagem as "Cubagem",
                    t.nome as "Transportadora Ganhadora"
                FROM cotacoes c
                LEFT JOIN transportadoras t ON c.transportadora_ganhadora_id = t.id
                WHERE c.id = {self.cotacao_selecionada_id}
            ''', conn)
            
            df_transportadoras = pd.read_sql(f'''
                SELECT 
                    t.nome as "Transportadora",
                    ct.valor_frete as "Valor Frete",
                    CASE WHEN ct.selecionada THEN 'Sim' ELSE 'Não' END as "Selecionada",
                    (ct.valor_frete / c.valor_nf * 100) as "Percentual do Frete"
                FROM cotacoes_transportadoras ct
                JOIN transportadoras t ON ct.transportadora_id = t.id
                JOIN cotacoes c ON ct.cotacao_id = c.id
                WHERE ct.cotacao_id = {self.cotacao_selecionada_id}
                ORDER BY ct.valor_frete
            ''', conn)
            
            conn.close()
            
            from datetime import datetime
            filename = f"cotacao_{self.cotacao_selecionada_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df_cotacao.to_excel(writer, sheet_name='Cotação', index=False)
                df_transportadoras.to_excel(writer, sheet_name='Transportadoras', index=False)
            
            QMessageBox.information(self, "Sucesso", f"Cotação #{self.cotacao_selecionada_id} exportada para:\n{filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar Excel: {e}")

    def exportar_excel(self):
        """Exporta todas as cotações para Excel"""
        try:
            conn = self.db.get_connection()
            
            query = """
                SELECT 
                    c.id as "ID",
                    c.data as "Data",
                    c.fornecedor as "Fornecedor",
                    c.num_pedido as "Pedido",
                    c.valor_nf as "Valor NF",
                    c.peso as "Peso",
                    c.volume as "Volume",
                    c.cubagem as "Cubagem",
                    t.nome as "Transportadora Ganhadora",
                    ct.valor_frete as "Frete",
                    (ct.valor_frete / c.valor_nf * 100) as "Percentual do Frete"
                FROM cotacoes c
                LEFT JOIN transportadoras t ON c.transportadora_ganhadora_id = t.id
                LEFT JOIN cotacoes_transportadoras ct ON c.id = ct.cotacao_id AND ct.selecionada = 1
                WHERE 1=1
            """
            params = []
            
            data_inicio = self.filtro_data_inicio.date().toString("yyyy-MM-dd")
            data_fim = self.filtro_data_fim.date().toString("yyyy-MM-dd")
            query += " AND c.data BETWEEN ? AND ?"
            params.extend([data_inicio, data_fim])
            
            fornecedor_filtro = self.filtro_fornecedor_input.text().strip()
            if fornecedor_filtro:
                query += " AND c.fornecedor LIKE ?"
                params.append(f"%{fornecedor_filtro}%")
            
            transportadora_filtro = self.filtro_transportadora_input.text().strip()
            if transportadora_filtro:
                query += " AND t.nome LIKE ?"
                params.append(f"%{transportadora_filtro}%")
            
            query += " ORDER BY c.data DESC, c.id DESC"
            
            df_cotacoes = pd.read_sql(query, conn, params=params)
            
            conn.close()
            
            from datetime import datetime
            filename = f"cotações_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            df_cotacoes.to_excel(filename, index=False)
            
            QMessageBox.information(self, "Sucesso", f"Dados exportados para:\n{filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar Excel: {e}")

    def excluir_cotacao(self):
        """Exclui a cotação selecionada"""
        if not self.cotacao_selecionada_id:
            return
        
        texto, ok = QInputDialog.getText(
            self, 
            "Confirmar Exclusão", 
            f"Digite 'SIM' para confirmar a exclusão da cotação #{self.cotacao_selecionada_id}:",
            text=""
        )
        
        if ok and texto.strip().upper() == "SIM":
            try:
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                try:
                    cursor.execute('DELETE FROM cotacoes_transportadoras WHERE cotacao_id = ?', (self.cotacao_selecionada_id,))
                    cursor.execute('DELETE FROM cotacoes WHERE id = ?', (self.cotacao_selecionada_id,))
                    
                    conn.commit()
                    QMessageBox.information(self, "Sucesso", f"Cotação #{self.cotacao_selecionada_id} excluída com sucesso!")
                    
                    self.cotacao_selecionada_id = None
                    self.carregar_cotacoes()
                    self.limpar_detalhes()
                    
                except Exception as e:
                    conn.rollback()
                    QMessageBox.critical(self, "Erro", f"Erro ao excluir cotação: {e}")
                finally:
                    conn.close()
                    
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro de conexão: {e}")
        elif ok:
            QMessageBox.warning(self, "Aviso", "Texto incorreto. A cotação não foi excluída.")

    def limpar_detalhes(self):
        """Limpa completamente os detalhes e volta ao estado inicial"""
        self.limpar_conteudo_detalhes()
        
        # Recria o label vazio
        self.label_vazio = QLabel("Selecione uma cotação para visualizar os detalhes")
        self.label_vazio.setAlignment(Qt.AlignCenter)
        self.label_vazio.setStyleSheet("color: #95a5a6; font-size: 16px; padding: 50px;")
        self.layout_conteudo.addWidget(self.label_vazio)
        
        # Reseta o título
        self.titulo_detalhes.setText("👀 SELECIONE UMA COTAÇÃO")
        self.titulo_detalhes.setStyleSheet("""
            color: #7f8c8d; 
            padding: 20px; 
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #95a5a6, stop:1 #7f8c8d);
            color: white;
            border-bottom: 3px solid #6c7a89;
        """)
        self.setup_botoes_acao()

    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.filtro_data_inicio.setDate(QDate.currentDate().addDays(-30))
        self.filtro_data_fim.setDate(QDate.currentDate())
        self.filtro_fornecedor_input.clear()
        self.filtro_transportadora_input.clear()