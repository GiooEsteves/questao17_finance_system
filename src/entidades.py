from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List


class TipoTransacao(Enum):
    CREDITO = "credito"
    DEBITO = "debito"
    TRANSFERENCIA_ENVIADA = "transferencia_enviada"
    TRANSFERENCIA_RECEBIDA = "transferencia_recebida"
    PAGAMENTO_BOLETO = "pagamento_boleto"


class Moeda(Enum):
    BRL = "BRL"
    USD = "USD"


# Exceções customizadas
class ContaNaoEncontradaError(Exception): pass
class SaldoInsuficienteError(Exception): pass
class TransacaoInvalidaError(Exception): pass
class MoedaIncompativelError(Exception): pass


@dataclass(frozen=True)
class Transacao:
    id_transacao: str
    data_hora: datetime
    tipo: TipoTransacao
    valor: float
    moeda: Moeda
    descricao: Optional[str] = None
    categoria: Optional[str] = None


@dataclass
class Conta:
    id_conta: str
    numero_agencia: str
    numero_conta: str
    saldo_atual: float
    moeda_padrao: Moeda
    historico_de_transacoes: List[Transacao] = field(default_factory=list)
    limite_cheque_especial: float = 0.0

    def adicionar_transacao(self, transacao: Transacao):
        self.historico_de_transacoes.append(transacao)
        self.historico_de_transacoes.sort(key=lambda t: t.data_hora)

    def atualizar_saldo(self, valor: float):
        self.saldo_atual += valor
