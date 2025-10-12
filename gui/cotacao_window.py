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
        """Configura a interface da tela de cotação"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Título
        title = QLabel("NOVA COTAÇÃO")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Scroll area para o formulário
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Seção 1: Dados do Fornecedor
        self.setup_dados_fornecedor(scroll_layout)
        
        # Seção 2: Transportadoras e Fretes
        self.setup_transportadoras_fretes(scroll_layout)
        
        # Botões de ação
        self.setup_botoes_acao(scroll_layout)
        
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def formatar_moeda(self, valor):
        """Formata qualquer valor digitado para moeda"""
        try:
            # Remove tudo que não é número
            texto_limpo = re.sub(r'[^\d]', '', str(valor))
            if not texto_limpo:
                return ""
            
            # Converte para número (assume que são centavos)
            numero = float(texto_limpo) / 100
            
            # Formata como moeda brasileira
            return f"R$ {numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return ""
    
    def setup_dados_fornecedor(self, layout):
        """Configura a seção de dados do fornecedor"""
        group = QGroupBox("📦 DADOS DO FORNECEDOR")
        form_layout = QFormLayout()
        
        # Data atual
        self.data_input = QDateEdit()
        self.data_input.setDate(QDate.currentDate())
        self.data_input.setCalendarPopup(True)
        self.data_input.setDisplayFormat("dd/MM/yyyy")
        
        # Fornecedor
        self.fornecedor_input = QLineEdit()
        self.fornecedor_input.setPlaceholderText("Nome do fornecedor")
        
        # Nº Pedido
        self.pedido_input = QLineEdit()
        self.pedido_input.setPlaceholderText("Número do pedido")
        
        # Valor da NF - FORMATA QUALQUER VALOR DIGITADO
        self.valor_nf_input = QLineEdit()
        self.valor_nf_input.setPlaceholderText("Digite o valor da NF")
        self.valor_nf_input.textChanged.connect(self.on_valor_nf_changed)
        
        # Volume
        self.volume_input = QLineEdit()
        self.volume_input.setPlaceholderText("Quantidade de volumes")
        
        # Peso
        self.peso_input = QLineEdit()
        self.peso_input.setPlaceholderText("Ex: 77,7")
        
        # Cubagem
        self.cubagem_input = QLineEdit()
        self.cubagem_input.setPlaceholderText("Ex: 0,746")
        
        form_layout.addRow("Data:", self.data_input)
        form_layout.addRow("Fornecedor*:", self.fornecedor_input)
        form_layout.addRow("Nº Pedido:", self.pedido_input)
        form_layout.addRow("Valor NF*:", self.valor_nf_input)
        form_layout.addRow("Volume:", self.volume_input)
        form_layout.addRow("Peso:", self.peso_input)
        form_layout.addRow("Cubagem:", self.cubagem_input)
        
        group.setLayout(form_layout)
        layout.addWidget(group)
    
    def on_valor_nf_changed(self, texto):
        """Formata qualquer valor digitado e calcula Rodocargas"""
        if not texto:
            self.limpar_rodocargas()
            return
        
        # Formata o valor digitado
        texto_formatado = self.formatar_moeda(texto)
        if texto_formatado and texto_formatado != texto:
            self.valor_nf_input.blockSignals(True)
            self.valor_nf_input.setText(texto_formatado)
            self.valor_nf_input.setCursorPosition(len(texto_formatado))
            self.valor_nf_input.blockSignals(False)
        
        # Calcula Rodocargas
        self.calcular_rodocargas_automatico()
    
    def setup_transportadoras_fretes(self, layout):
        """Configura a seção de transportadoras e fretes"""
        group = QGroupBox("🚛 TRANSPORTADORAS E FRETES")
        group_layout = QVBoxLayout()
        
        # Tabela de transportadoras
        self.table_transportadoras = QTableWidget()
        self.table_transportadoras.setColumnCount(5)
        self.table_transportadoras.setHorizontalHeaderLabels([
            "Transportadora", "Valor Frete", "Percentual", "Cálculo", "Ação"
        ])
        
        header = self.table_transportadoras.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        group_layout.addWidget(self.table_transportadoras)
        
        # Info da Rodocargas
        self.rodocargas_info = QLabel("")
        self.rodocargas_info.setStyleSheet("color: #2c3e50; font-weight: bold; margin: 10px;")
        self.rodocargas_info.setVisible(False)
        group_layout.addWidget(self.rodocargas_info)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def setup_botoes_acao(self, layout):
        """Configura os botões de ação"""
        btn_layout = QHBoxLayout()
        
        btn_calcular = QPushButton("🧮 CALCULAR")
        btn_calcular.setFixedHeight(40)
        btn_calcular.clicked.connect(self.calcular_fretes)
        
        btn_limpar = QPushButton("🔄 LIMPAR")
        btn_limpar.setFixedHeight(40)
        btn_limpar.clicked.connect(self.limpar_formulario)
        
        btn_salvar = QPushButton("💾 SALVAR COTAÇÃO")
        btn_salvar.setFixedHeight(40)
        btn_salvar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        btn_salvar.clicked.connect(self.salvar_cotacao)
        
        btn_layout.addWidget(btn_calcular)
        btn_layout.addWidget(btn_limpar)
        btn_layout.addWidget(btn_salvar)
        
        layout.addLayout(btn_layout)
    
    def on_valor_frete_changed(self, texto, row):
        """Formata qualquer valor digitado nos campos de frete"""
        if not texto:
            self.atualizar_calculos(row)
            return
        
        # Formata o valor digitado
        texto_formatado = self.formatar_moeda(texto)
        if texto_formatado and texto_formatado != texto:
            # Encontra o input correto
            valor_input = self.table_transportadoras.cellWidget(row, 1)
            if valor_input:
                valor_input.blockSignals(True)
                valor_input.setText(texto_formatado)
                valor_input.setCursorPosition(len(texto_formatado))
                valor_input.blockSignals(False)
        
        # Atualiza cálculos
        self.atualizar_calculos(row)
    
    def parse_number(self, text):
        """Converte texto para número - VERSÃO CORRIGIDA"""
        if not text:
            return 0.0
        
        try:
            # Remove R$ e espaços
            text = str(text).replace('R$', '').replace(' ', '').strip()
            
            # Se já tem ponto como separador decimal, usa direto
            if '.' in text and text.count('.') == 1:
                partes = text.split('.')
                if len(partes) == 2 and partes[1].isdigit():
                    return float(text)
            
            # Remove pontos de milhar e converte vírgula decimal para ponto
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
                valor_label.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #f8f9fa; padding: 5px;")
                valor_label.setAlignment(Qt.AlignCenter)
                self.table_transportadoras.setCellWidget(row, 1, valor_label)
            else:
                valor_input = QLineEdit()
                valor_input.setPlaceholderText("Digite o valor")
                # CONECTA COM A FORMATAÇÃO AUTOMÁTICA
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
            btn_selecionar.clicked.connect(lambda checked, r=row: self.selecionar_transportadora(r))
            self.table_transportadoras.setCellWidget(row, 4, btn_selecionar)
    
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
        """Atualiza os cálculos - VERSÃO CORRIGIDA"""
        try:
            valor_nf = self.get_valor_nf_numerico()
            print(f"DEBUG - Valor NF: {valor_nf}")  # DEBUG
            
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
                    print(f"DEBUG - Rodocargas valor: {valor_frete}")  # DEBUG
            else:
                valor_input = self.table_transportadoras.cellWidget(row, 1)
                if valor_input and valor_input.text():
                    valor_frete = self.parse_number(valor_input.text())
                    print(f"DEBUG - {transportadora[1]} valor: {valor_frete}")  # DEBUG
            
            if valor_frete <= 0:
                self.table_transportadoras.item(row, 2).setText("0,00%")
                self.table_transportadoras.item(row, 3).setText("")
                return
            
            # CÁLCULO DO PERCENTUAL - CORRIGIDO
            percentual = (valor_frete / valor_nf) * 100
            print(f"DEBUG - Cálculo: ({valor_frete} / {valor_nf}) × 100 = {percentual}%")  # DEBUG
            
            # Atualiza percentual na tabela
            self.table_transportadoras.item(row, 2).setText(f"{percentual:.2f}%".replace('.', ','))
            
            # Mostra detalhes do cálculo
            detalhes = f"({valor_frete:.2f} / {valor_nf:.2f}) × 100 = {percentual:.2f}%"
            detalhes = detalhes.replace('.', ',')
            self.table_transportadoras.item(row, 3).setText(detalhes)
            
            # Info da Rodocargas
            if transportadora[1].lower() == "rodocargas":
                info_text = f"Rodocargas: {transportadora[3] or 14}% + {transportadora[4] or 7}% ICMS = R$ {valor_frete:.2f}"
                info_text = info_text.replace('.', ',')
                self.rodocargas_info.setText(info_text)
                self.rodocargas_info.setVisible(True)
                    
        except Exception as e:
            print(f"Erro no cálculo linha {row}: {e}")
            self.table_transportadoras.item(row, 2).setText("Erro")
    
    def selecionar_transportadora(self, row):
        """Seleciona transportadora"""
        for i in range(self.table_transportadoras.rowCount()):
            btn = self.table_transportadoras.cellWidget(i, 4)
            if btn:
                btn.setText("SELECIONAR")
                btn.setStyleSheet("")
        
        btn_selecionado = self.table_transportadoras.cellWidget(row, 4)
        btn_selecionado.setText("🥇 SELECIONADA")
        btn_selecionado.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        
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
                btn.setStyleSheet("")
        
        if hasattr(self, 'transportadora_selecionada_id'):
            del self.transportadora_selecionada_id