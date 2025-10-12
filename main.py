import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """Função principal que inicia a aplicação"""
    app = QApplication(sys.argv)
    
    # Configuração global da aplicação
    app.setApplicationName("Sistema Transportadora")
    app.setApplicationVersion("1.0")
    
    # Cria e exibe a janela principal
    window = MainWindow()
    window.show()
    
    # Executa a aplicação
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()