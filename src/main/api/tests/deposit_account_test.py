import pytest
from src.main.api.models.deposit_account_request import DepositAccountRequest


@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, api_manager, create_user_request):
        account_response = api_manager.user_steps.create_account(create_user_request)

        assert account_response.balance == 0

        deposit_request = DepositAccountRequest(
            accountId=account_response.id,
            amount=1000.5
        )

        deposit_response = api_manager.user_steps.deposit_account(
            create_user_request,
            deposit_request
        )

        assert deposit_response.id == deposit_request.accountId
        assert deposit_response.balance == deposit_request.amount

    @pytest.mark.parametrize(
        "amount",
        [
            (999),
            (9001)
        ]
    )
    def test_deposit_account_invalid(self, api_manager, create_user_request, amount):
        account_response = api_manager.user_steps.create_account(
            create_user_request
        )

        assert account_response.balance == 0

        deposit_request = DepositAccountRequest(
            accountId=account_response.id,
            amount=amount
        )

        api_manager.user_steps.deposit_invalid_account(
            create_user_request,
            deposit_request
        )