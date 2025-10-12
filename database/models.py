from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Transportadora:
    id: Optional[int]
    nome: str
    cnpj: str
    contato: str = ""
    telefone: str = ""
    email: str = ""
    percentual_base: float = 0.0
    icms: float = 0.0
    data_criacao: datetime = None

@dataclass
class Cotacao:
    id: Optional[int]
    data: datetime
    fornecedor: str
    num_pedido: str = ""
    valor_nf: float = 0.0
    peso: float = 0.0
    volume: int = 0
    cubagem: float = 0.0
    transportadora_ganhadora_id: Optional[int] = None

@dataclass
class CotacaoTransportadora:
    id: Optional[int]
    cotacao_id: int
    transportadora_id: int
    valor_frete: float
    selecionada: bool = False

@dataclass
class CalculoCubagem:
    id: Optional[int]
    data: datetime
    itens_json: str
    cubagem_total: float