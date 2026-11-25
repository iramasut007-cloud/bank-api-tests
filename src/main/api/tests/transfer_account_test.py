import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session  ):
        from_account_response = api_manager.user_steps.create_account(create_user_request)
        to_account_response = api_manager.user_steps.create_account(create_user_request)

        assert from_account_response.balance == 0
        assert to_account_response.balance == 0

        deposit_request = DepositAccountRequest(
            accountId=from_account_response.id,
            amount=1000.5
        )

        deposit_response = api_manager.user_steps.deposit_account(create_user_request, deposit_request)

        assert deposit_response.balance == deposit_request.amount

        transfer_request = TransferAccountRequest(
            fromAccountId=from_account_response.id,
            toAccountId=to_account_response.id,
            amount=500
        )

        transfer_response = api_manager.user_steps.transfer_account(
            create_user_request,
            transfer_request
        )

        assert transfer_response.fromAccountId == transfer_request.fromAccountId
        assert transfer_response.toAccountId == transfer_request.toAccountId
        assert (transfer_response.fromAccountIdBalance == deposit_request.amount - transfer_request.amount)


        from_account_db = Account.get_account_by_id(db_session, from_account_response.id)
        to_account_db = Account.get_account_by_id(db_session, to_account_response.id)

        assert from_account_db is not None, 'Счёт отправителя не найден в БД'
        assert to_account_db is not None, 'Счёт получателя не найден в БД'
        assert from_account_db.balance == deposit_request.amount - transfer_request.amount, (
            f"Неверный баланс отправителя в БД: ожидали {deposit_request.amount - transfer_request.amount}, "
            f"получили {from_account_db.balance}"
        )
        assert to_account_db.balance == to_account_response.balance + transfer_request.amount, (
            f"Неверный баланс получателя в БД: ожидали {to_account_response.balance + transfer_request.amount}, "
            f"получили {to_account_db.balance}"
        )



    @pytest.mark.parametrize(
    "amount",
    [
        (499),
        (10001),
        (10100)
        ]
    )
    def test_transfer_account_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session, amount: int):
        from_account_response = api_manager.user_steps.create_account(create_user_request)
        to_account_response = api_manager.user_steps.create_account(create_user_request)

        deposit_from_request = DepositAccountRequest(
            accountId=from_account_response.id,
            amount=3000
        )
        deposit_from_response = api_manager.user_steps.deposit_account(create_user_request, deposit_from_request)
        assert deposit_from_response.balance == 3000

        deposit_to_request = DepositAccountRequest(
            accountId=to_account_response.id,
            amount=1000
        )
        deposit_to_response = api_manager.user_steps.deposit_account(create_user_request, deposit_to_request)
        assert deposit_to_response.balance == 1000

        from_account_db_before = Account.get_account_by_id(db_session, from_account_response.id)
        to_account_db_before = Account.get_account_by_id(db_session, to_account_response.id)
        from_balance_before = from_account_db_before.balance
        to_balance_before = to_account_db_before.balance

        transfer_request = TransferAccountRequest(
            fromAccountId=from_account_response.id,
            toAccountId=to_account_response.id,
            amount=amount
        )
        api_manager.user_steps.transfer_invalid_account(create_user_request, transfer_request)

        from_account_after = api_manager.user_steps.get_account_transactions(
            create_user_request, from_account_response.id
        )
        to_account_after = api_manager.user_steps.get_account_transactions(
            create_user_request, to_account_response.id
        )

        assert from_account_after.balance == 3000
        assert to_account_after.balance == 1000

        db_session.expire_all()
        from_account_db_after = Account.get_account_by_id(db_session, from_account_response.id)
        to_account_db_after = Account.get_account_by_id(db_session, to_account_response.id)

        assert from_account_db_after.balance == from_balance_before, (
            f"Баланс отправителя в БД изменился после отказа: было {from_balance_before}, "
            f"стало {from_account_db_after.balance}"
        )
        assert to_account_db_after.balance == to_balance_before, (
            f"Баланс получателя в БД изменился после отказа: было {to_balance_before}, "
            f"стало {to_account_db_after.balance}"
        )
