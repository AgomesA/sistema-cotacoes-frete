import re

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

    @staticmethod
    def validate_email(email):
        """Valida formato básico de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None