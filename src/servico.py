from datetime import datetime
from typing import List, Optional, Dict
import uuid

from .entidades import *


class ServicoDeTransacoes:
    def __init__(self):
        self.contas: Dict[str, Conta] = {}
        self.transacoes_ids: set = set()

    def abrir_conta(self, numero_agencia, numero_conta, moeda_padrao, saldo_inicial=0.0, limite_cheque_especial=0.0):
        id_conta = str(uuid.uuid4())
        conta = Conta(id_conta, numero_agencia, numero_conta, saldo_inicial, moeda_padrao, limite_cheque_especial=limite_cheque_especial)
        self.contas[id_conta] = conta
        return conta

    def consultar_saldo(self, id_conta: str) -> float:
        return self._obter_conta(id_conta).saldo_atual

    def obter_extrato(self, id_conta: str, inicio: datetime, fim: datetime) -> List[Transacao]:
        conta = self._obter_conta(id_conta)
        return [t for t in conta.historico_de_transacoes if inicio <= t.data_hora <= fim]

    def registrar_credito(self, id_conta, valor, moeda, data_hora, descricao=None, categoria=None):
        conta = self._obter_conta(id_conta)
        self._validar_transacao(valor, moeda, conta)
        transacao = self._nova_transacao(TipoTransacao.CREDITO, valor, moeda, data_hora, descricao, categoria)
        conta.adicionar_transacao(transacao)
        conta.atualizar_saldo(valor)
        return transacao

    def registrar_debito(self, id_conta, valor, moeda, data_hora, descricao=None, categoria=None):
        conta = self._obter_conta(id_conta)
        self._validar_transacao(valor, moeda, conta)
        if conta.saldo_atual + conta.limite_cheque_especial < valor:
            raise SaldoInsuficienteError("Saldo insuficiente")
        transacao = self._nova_transacao(TipoTransacao.DEBITO, valor, moeda, data_hora, descricao, categoria)
        conta.adicionar_transacao(transacao)
        conta.atualizar_saldo(-valor)
        return transacao

    def realizar_transferencia(self, origem_id, destino_id, valor, moeda, data_hora, descricao=None):
        origem = self._obter_conta(origem_id)
        destino = self._obter_conta(destino_id)
        self._validar_transacao(valor, moeda, origem)
        self._validar_transacao(valor, moeda, destino)
        if origem.saldo_atual + origem.limite_cheque_especial < valor:
            raise SaldoInsuficienteError("Saldo insuficiente")
        t1 = self._nova_transacao(TipoTransacao.TRANSFERENCIA_ENVIADA, valor, moeda, data_hora, descricao)
        t2 = self._nova_transacao(TipoTransacao.TRANSFERENCIA_RECEBIDA, valor, moeda, data_hora, descricao)
        origem.adicionar_transacao(t1)
        origem.atualizar_saldo(-valor)
        destino.adicionar_transacao(t2)
        destino.atualizar_saldo(valor)
        return t1, t2

    # Métodos auxiliares

    def _nova_transacao(self, tipo, valor, moeda, data_hora, descricao, categoria=None):
        id_transacao = self._gerar_id_transacao_unico()
        return Transacao(id_transacao, data_hora, tipo, valor, moeda, descricao, categoria)

    def _gerar_id_transacao_unico(self):
        while True:
            tid = str(uuid.uuid4())
            if tid not in self.transacoes_ids:
                self.transacoes_ids.add(tid)
                return tid

    def _obter_conta(self, id_conta):
        if id_conta not in self.contas:
            raise ContaNaoEncontradaError("Conta não encontrada")
        return self.contas[id_conta]

    def _validar_transacao(self, valor, moeda, conta):
        if valor <= 0:
            raise TransacaoInvalidaError("Valor deve ser positivo")
        if moeda != conta.moeda_padrao:
            raise MoedaIncompativelError("Moeda incompatível com a conta")
