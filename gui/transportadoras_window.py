import sqlite3
import re
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QGroupBox, QFormLayout,
                             QDoubleSpinBox, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Formatters:
    @staticmethod
    def format_cnpj(cnpj):
        """Formata CNPJ para 00.000.000/0000-00"""
        # Remove tudo que não é número
        cnpj = re.sub(r'[^\d]', '', cnpj)
        
        # Aplica a formatação
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
        # Remove tudo que não é número
        telefone = re.sub(r'[^\d]', '', telefone)
        
        # Aplica a formatação
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
        """Configura a interface da tela de transportadoras"""
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Painel esquerdo - Lista de transportadoras
        self.setup_list_panel(main_layout)
        
        # Painel direito - Formulário de cadastro/edição
        self.setup_form_panel(main_layout)
    
    def setup_list_panel(self, main_layout):
        """Configura o painel da lista de transportadoras"""
        list_panel = QWidget()
        list_panel.setFixedWidth(400)
        list_layout = QVBoxLayout()
        
        # Título
        title = QLabel("TRANSPORTADORAS CADASTRADAS")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        list_layout.addWidget(title)
        
        # Botão Novo
        btn_novo = QPushButton("➕ NOVA TRANSPORTADORA")
        btn_novo.setFixedHeight(40)
        btn_novo.clicked.connect(self.nova_transportadora)
        list_layout.addWidget(btn_novo)
        
        # Tabela de transportadoras
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CNPJ"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellDoubleClicked.connect(self.editar_transportadora)
        list_layout.addWidget(self.table)
        
        list_panel.setLayout(list_layout)
        main_layout.addWidget(list_panel)
    
    def setup_form_panel(self, main_layout):
        """Configura o painel do formulário"""
        form_panel = QWidget()
        form_layout = QVBoxLayout()
        
        # Título do formulário
        self.form_title = QLabel("CADASTRAR TRANSPORTADORA")
        self.form_title.setFont(QFont("Arial", 14, QFont.Bold))
        self.form_title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.form_title)
        
        # Scroll area para o formulário
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Grupo de dados básicos
        basic_group = QGroupBox("Dados da Transportadora")
        basic_layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.cnpj_input = QLineEdit()
        
        # Conecta a formatação do CNPJ
        self.cnpj_input.textChanged.connect(self.format_cnpj_field)
        
        basic_layout.addRow("Nome*:", self.nome_input)
        basic_layout.addRow("CNPJ:", self.cnpj_input)
        
        basic_group.setLayout(basic_layout)
        scroll_layout.addWidget(basic_group)
        
        # Grupo de telefones
        self.telefones_group = QGroupBox("📞 TELEFONES")
        self.telefones_layout = QVBoxLayout()
        
        # Botão para adicionar telefone (só um botão)
        self.btn_add_telefone = QPushButton("➕ Adicionar Telefone")
        self.btn_add_telefone.clicked.connect(lambda: self.adicionar_contato('telefone'))
        self.telefones_layout.addWidget(self.btn_add_telefone)
        
        self.telefones_group.setLayout(self.telefones_layout)
        scroll_layout.addWidget(self.telefones_group)
        
        # Grupo de emails
        self.emails_group = QGroupBox("✉️ EMAILS")
        self.emails_layout = QVBoxLayout()
        
        # Botão para adicionar email (só um botão)
        self.btn_add_email = QPushButton("➕ Adicionar Email")
        self.btn_add_email.clicked.connect(lambda: self.adicionar_contato('email'))
        self.emails_layout.addWidget(self.btn_add_email)
        
        self.emails_group.setLayout(self.emails_layout)
        scroll_layout.addWidget(self.emails_group)
        
        # Grupo de configurações Rodocargas
        self.rodocargas_group = QGroupBox("Configurações Rodocargas")
        rodocargas_layout = QFormLayout()
        
        self.percentual_input = QDoubleSpinBox()
        self.percentual_input.setRange(0.1, 100.0)
        self.percentual_input.setSuffix(" %")
        self.percentual_input.setDecimals(1)
        self.percentual_input.setValue(14.0)
        
        self.icms_input = QDoubleSpinBox()
        self.icms_input.setRange(0.0, 100.0)
        self.icms_input.setSuffix(" %")
        self.icms_input.setDecimals(1)
        self.icms_input.setValue(7.0)
        
        rodocargas_layout.addRow("Percentual Base:", self.percentual_input)
        rodocargas_layout.addRow("ICMS:", self.icms_input)
        
        self.rodocargas_group.setLayout(rodocargas_layout)
        self.rodocargas_group.setVisible(False)
        scroll_layout.addWidget(self.rodocargas_group)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        
        self.btn_salvar = QPushButton("💾 SALVAR")
        self.btn_salvar.setFixedHeight(40)
        self.btn_salvar.clicked.connect(self.salvar_transportadora)
        
        self.btn_limpar = QPushButton("🔄 LIMPAR")
        self.btn_limpar.setFixedHeight(40)
        self.btn_limpar.clicked.connect(self.limpar_formulario)
        
        self.btn_excluir = QPushButton("🗑️ EXCLUIR")
        self.btn_excluir.setFixedHeight(40)
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
        
        # Frame para cada linha de contato
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box)
        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(5, 5, 5, 5)
        
        # Campo do valor (telefone/email)
        valor_input = QLineEdit()
        valor_input.setPlaceholderText(placeholder_valor)
        valor_input.setText(valor)
        valor_input.setMinimumWidth(150)
        
        # Para telefones, adiciona formatação automática
        if tipo == 'telefone':
            valor_input.textChanged.connect(
                lambda text, field=valor_input: self.format_telefone_field(field, text)
            )
        
        # Campo do nome do contato
        contato_input = QLineEdit()
        contato_input.setPlaceholderText(placeholder_contato)
        contato_input.setText(contato_nome)
        contato_input.setMinimumWidth(120)
        
        # Botão remover
        btn_remover = QPushButton("➖")
        btn_remover.setFixedSize(30, 30)
        btn_remover.clicked.connect(lambda: self.remover_contato(frame, widgets_list))
        
        frame_layout.addWidget(QLabel("Número:" if tipo == 'telefone' else "Email:"))
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
    
    def format_cnpj_field(self, text):
        """Aplica formatação automática no campo de CNPJ"""
        cursor_position = self.cnpj_input.cursorPosition()
        formatted = Formatters.format_cnpj(text)
        
        if formatted != text:
            self.cnpj_input.setText(formatted)
            # Mantém a posição do cursor considerando os caracteres adicionados
            new_position = cursor_position + (len(formatted) - len(text))
            self.cnpj_input.setCursorPosition(min(new_position, len(formatted)))
    
    def format_telefone_field(self, field, text):
        """Aplica formatação automática no campo de telefone"""
        cursor_position = field.cursorPosition()
        formatted = Formatters.format_telefone(text)
        
        if formatted != text:
            field.setText(formatted)
            # Mantém a posição do cursor considerando os caracteres adicionados
            new_position = cursor_position + (len(formatted) - len(text))
            field.setCursorPosition(min(new_position, len(formatted)))
    
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
                self.table.setItem(row, 0, QTableWidgetItem(str(transp[0])))
                self.table.setItem(row, 1, QTableWidgetItem(transp[1]))
                self.table.setItem(row, 2, QTableWidgetItem(transp[2] if transp[2] else ""))
            
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