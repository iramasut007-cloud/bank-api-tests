import pytest
from src.main.api.models.credit_request import CreditRequest


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(self, api_manager, create_credit_secret_user_request):
        account_response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        assert account_response.balance == 0

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=5000,
            termMonths=12
        )

        credit_response = api_manager.user_steps.credit_request(create_credit_secret_user_request, credit_request)

        assert credit_response.id == credit_request.accountId
        assert credit_response.amount == credit_request.amount
        assert credit_response.balance == credit_request.amount

    @pytest.mark.parametrize(
        "amount",
        [
            (4999),
            (15001),
        ]
    )
    def test_credit_request_invalid_amount(self, api_manager, create_credit_secret_user_request, amount):
        account_response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        assert account_response.balance == 0

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=amount,
            termMonths=12
        )

        api_manager.user_steps.credit_invalid_request(
            create_credit_secret_user_request,
            credit_request,
            expected_status=400
        )



