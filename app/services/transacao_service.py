from datetime import datetime, date
from decimal import Decimal

from fastapi import status, HTTPException

from app.repositories.transacao_repository import TransacaoRepository
from app.schemas.conta_in import ContaUnicaIn
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

    async def create_transacao(self, post: TransacaoIn):

        if not post.numero_conta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Para efetuar uma transferência informe o número da sua conta - numero_conta.")

        if post.valor <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="O valor do depósito deve ser positivo.")

        conta_origem = await self.conta_service.obter_conta(
            numero=post.numero_conta
        )

        if not conta_origem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")

        if post.tipo == "deposito":

            novo_saldo = conta_origem["saldo"] + Decimal(post.valor)

            await self.repository.update_saldo(novo_saldo, conta_origem["id"])
            resultado_transacao = await self.repository.create_transacao(post, conta_origem)

        if post.tipo == "transferencia":

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

            resultado_transacao = await self.repository.create_transacao(
                TransacaoIn(
                    tipo=post.tipo,
                    valor=post.valor,
                    numero_conta=post.numero_conta,
                    conta_id_origem=conta_origem["id"],
                    conta_id_destino=conta_destino["id"],
                    conta_id=conta_origem["id"],
                ),
                conta_origem
            )

            await self.conta_service.update_saldo(novo_saldo, conta_origem["id"])







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