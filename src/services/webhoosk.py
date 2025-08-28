import hashlib
import logging

from fastapi import HTTPException, status

from config.config import SECRET_KEY
from schemas import webhooks as webhooks_schema, users as users_scheme
from repositories import webhooks as webhooks_repository
from models.users import Accounts


class ProcessPayment:
    """Класс обработки вебхука"""

    async def create_signature(self, data: webhooks_schema.ReceivePayment) -> str:
        """Создать подпись, чтобы проверить транзакцию"""

        concat_str = f"{data.account_id}{data.amount}{data.transaction_id}{data.user_id}{SECRET_KEY}"
        signature = hashlib.sha256(concat_str.encode()).hexdigest()

        logging.info(f"------------------{signature}---------------")

        return signature
    
    async def is_signature_valid(self, data: webhooks_schema.ReceivePayment) -> bool:
        """Проверить валидность подписи"""

        test_signature = await self.create_signature(data)
        return test_signature == data.signature
    
    async def get_user_account(self, user_id: int, account_id: int) -> Accounts:
        """
        Получить счет пользователя.
        Если его нет - создать
        """

        user_account = await webhooks_repository.get_user_account(account_id)

        if user_account is None:
            user_account = await webhooks_repository.create_user_account(user_id)
            logging.info(f"Account of user {user_id} was created!")
        else:
            if user_account.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The user does not own this account!",
                )

        return user_account
    
    async def is_payment_not_exists(self, transaction_id: id) -> bool:
        """Проверить есть ли платеж с такой транзакцией"""

        payment = await webhooks_repository.get_payment(transaction_id)
        return payment is None
    
    async def create_payment(self, account_id: int, transaction_id: int, amount: int) -> None:
        """Создать новый платеж"""

        await webhooks_repository.create_payment(account_id, transaction_id, amount)
    
    async def update_amount_of_user_account(self, user_account: Accounts, amount: int) -> Accounts:
        """Добавить сумму транзакции на счет пользователя"""

        user_account.balance += amount
        await webhooks_repository.update_amount_of_user_account(user_account)
        # return user_account
    
    async def process_payment(self, data: webhooks_schema.ReceivePayment) -> users_scheme.UserPaymentSchema:
        """Обработать вебхук"""

        if await self.is_signature_valid(data):
            if await self.is_payment_not_exists(data.transaction_id):
                # Получить счет пользователя.
                # Если его нет - создать
                user_account = await self.get_user_account(data.user_id, data.account_id)
                await self.create_payment(user_account.id, data.transaction_id, data.amount)
                await self.update_amount_of_user_account(user_account, data.amount)
                return user_account
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A payment with such transaction already exists!",
            )
        
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The signature doesn't valid!",
            )
