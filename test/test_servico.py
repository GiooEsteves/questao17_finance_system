import pytest
from datetime import datetime
from src.servico import ServicoDeTransacoes
from src.entidades import Moeda, SaldoInsuficienteError

def test_credito_e_debito():
    s = ServicoDeTransacoes()
    conta = s.abrir_conta("001", "00001-1", Moeda.BRL)
    s.registrar_credito(conta.id_conta, 500, Moeda.BRL, datetime.now())
    assert s.consultar_saldo(conta.id_conta) == 500
    s.registrar_debito(conta.id_conta, 100, Moeda.BRL, datetime.now())
    assert s.consultar_saldo(conta.id_conta) == 400

def test_saldo_insuficiente():
    s = ServicoDeTransacoes()
    conta = s.abrir_conta("001", "00001-1", Moeda.BRL)
    with pytest.raises(SaldoInsuficienteError):
        s.registrar_debito(conta.id_conta, 100, Moeda.BRL, datetime.now())
