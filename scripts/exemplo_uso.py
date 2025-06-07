from datetime import datetime
from src.servico import ServicoDeTransacoes
from src.entidades import Moeda

servico = ServicoDeTransacoes()

conta_a = servico.abrir_conta("001", "12345-6", Moeda.BRL)
servico.registrar_credito(conta_a.id_conta, 1000.0, Moeda.BRL, datetime.now(), "Depósito Inicial")
servico.registrar_debito(conta_a.id_conta, 50.0, Moeda.BRL, datetime.now(), "Conta de Luz")

conta_b = servico.abrir_conta("002", "98765-4", Moeda.BRL)
servico.realizar_transferencia(conta_a.id_conta, conta_b.id_conta, 200.0, Moeda.BRL, datetime.now(), "Presente")

print("Saldo Conta A:", servico.consultar_saldo(conta_a.id_conta))
print("Saldo Conta B:", servico.consultar_saldo(conta_b.id_conta))
