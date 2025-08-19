from datetime import datetime, date
from decimal import Decimal

from fastapi import status, HTTPException

from app.repositories.transacao_repository import TransacaoRepository
from app.schemas.transacao_in import TransacaoIn
from app.services.conta_service import ContaService
from app.views.agencia_out import AgenciaOut
from app.views.cliente_out import ClienteOut
from app.views.conta_out import ContaOut
from app.views.transacao_out import TransacaoOut, TransacaoHistoricoOut


class TransacaoService:
    def __init__(self, repository: TransacaoRepository, conta_service: ContaService):
        self.repository = repository
        self.conta_service = conta_service

    async def _valida_conta_origem(self, numero_conta: int):
        conta_origem = await self.conta_service.obter_conta(
            numero=numero_conta
        )

        if not conta_origem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")

        return conta_origem

    async def get_historico(self, data, conta_id, numero_conta, limit, skip) -> TransacaoOut | list[TransacaoOut]:

        if data:
            data_convertida = datetime.strptime(data, "%d/%m/%Y").date()
            transacoes = await self.repository.get_historico(filtro=data_convertida, tipo_filtro="data", limit=limit, skip=skip)
        elif conta_id:
            transacoes = await self.repository.get_historico(filtro=conta_id, tipo_filtro="conta_id", limit=limit, skip=skip)
        elif numero_conta:
            transacoes = await self.repository.get_historico(filtro=numero_conta, tipo_filtro="numero_conta", limit=limit, skip=skip)
        else:
            transacoes = await self.repository.get_historico(filtro=date.today(), tipo_filtro="data", limit=limit, skip=skip)

        transacao_historico_out = []

        for transacao in transacoes:
            r_dict = dict(transacao)

            transacao_historico_out.append(
                TransacaoHistoricoOut(
                    id=r_dict["transacoes_id"],
                    tipo=r_dict["transacoes_tipo"],
                    valor=float(r_dict["transacoes_valor"]),
                    numero_conta=r_dict["transacoes_numero_conta"],
                    data=r_dict["transacoes_data"],
                    hora=r_dict["transacoes_hora"],
                    created_at=r_dict["transacoes_created_at"],
                    conta_id_origem=r_dict["transacoes_conta_id_origem"],
                    conta_id_destino=r_dict["transacoes_conta_id_destino"],
                    conta=ContaOut(
                        id=r_dict["contas_id"],
                        numero=r_dict["contas_numero"],
                        saldo=float(r_dict["contas_saldo"]),
                        created_at=r_dict["contas_created_at"],
                    ),
                    cliente=ClienteOut(
                        id=r_dict["clientes_id"],
                        nome=r_dict["clientes_nome"],
                        sobrenome=r_dict["clientes_sobrenome"],
                        data_nascimento=r_dict["clientes_data_nascimento"],
                        cpf=r_dict["clientes_cpf"],
                    ),
                    agencia=AgenciaOut(
                        id=r_dict["agencias_id"],
                        nome=r_dict["agencias_nome"],
                        numero=r_dict["agencias_numero"],
                        cidade=r_dict["agencias_cidade"],
                        estado=r_dict["agencias_estado"],
                    )
                )
            )

        return transacao_historico_out

    async def _atualiza_saldo_insere_transacao(self):
        pass

    async def create_transacao(self, post: TransacaoIn):

        if post.tipo not in ('deposito', 'saque', 'transferencia'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Tipo de opreação inválida!")

        if post.valor <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O valor do depósito deve ser positivo.")

        try:
            conta_origem = await self._valida_conta_origem(post.numero_conta)

            if post.tipo == 'deposito':
                return await self._efetua_deposito(post, conta_origem)
            elif post.tipo == 'saque':
                return await self._efetua_saque(post, conta_origem)
            else:
                return await self._efetua_transferencia(post, conta_origem)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    async def _efetua_deposito(self, post: TransacaoIn, conta_origem):
        novo_saldo = conta_origem["saldo"] + Decimal(post.valor)

        await self.conta_service.update_saldo(novo_saldo, conta_origem["id"])
        resultado_transacao = await self.repository.create_transacao(post, conta_origem)

        return await self._mapear_transacao_out(resultado_transacao, conta_origem, novo_saldo)

    async def _efetua_saque(self, post: TransacaoIn, conta_origem):

        saldo_atual = Decimal(conta_origem["saldo"])
        valor_saque = Decimal(str(post.valor))

        if saldo_atual <= 0 or valor_saque > saldo_atual:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Não foi possível realizar o saque. Saldo onsuficiente: R$ {saldo_atual:.2f}.")

        novo_saldo = saldo_atual - valor_saque

        await self.conta_service.update_saldo(novo_saldo, conta_origem["id"])

        resultado_transacao = await self.repository.create_transacao(post, conta_origem)

        return await self._mapear_transacao_out(
            resultado_transacao, conta_origem, novo_saldo
        )

    async def _efetua_transferencia(self, post: TransacaoIn, conta_origem):
        if post.conta_id_destino is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Para efetuar uma transferência informe o ID da conta de destino.")

        valor_conta_origem = Decimal(str(conta_origem["saldo"]))

        if valor_conta_origem <= 0 or post.valor > valor_conta_origem:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Você não tem saldo suficiente.")

        conta_destino = await self.conta_service.obter_conta(
            conta_id_destino=post.conta_id_destino,
            tipo=post.tipo
        )

        if not conta_destino:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta de destino não encontrada.")

        novo_saldo = valor_conta_origem - Decimal(str(post.valor))
        novo_saldo_conta_destino = conta_destino["saldo"] + Decimal(str(post.valor))

        await self.conta_service.update_saldo(
            novo_saldo=novo_saldo_conta_destino,
            conta_id=conta_destino["id"]
        )

        await self.conta_service.update_saldo(novo_saldo, conta_origem["id"])

        resultado_transacao = await self.repository.create_transacao(post, conta_origem)

        return await self._mapear_transacao_out(resultado_transacao, conta_origem, novo_saldo)

    async def _mapear_transacao_out(self, resultado_transacao, conta_origem, novo_saldo):
        resultado_transacao_dict = dict(resultado_transacao)

        return TransacaoOut(
            id=resultado_transacao_dict["id"],
            tipo=resultado_transacao_dict["tipo"],
            valor=resultado_transacao_dict["valor"],
            numero_conta=resultado_transacao_dict["numero_conta"],
            data=resultado_transacao_dict["data"],
            hora=resultado_transacao_dict["hora"],
            conta_id_origem=conta_origem["id"],
            conta_id_destino=conta_origem["id"],
            conta=ContaOut(
                id=conta_origem["id"],
                numero=conta_origem["numero"],
                saldo=novo_saldo,
                created_at=conta_origem["created_at"],
                updated_at=conta_origem["updated_at"],
            )
        )