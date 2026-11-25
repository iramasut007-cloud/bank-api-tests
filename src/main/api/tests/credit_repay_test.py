import pytest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.requests.credit_repay_requester import CreditRepayRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.credit_requester import CreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs



@pytest.mark.api

class TestCreditRepay:
    def test_credit_repay_valid(self, api_manager, create_credit_secret_user_request):
        account_response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        assert account_response.balance == 0

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=5000,
            termMonths=12
        )

        credit_response = api_manager.user_steps.credit_request(
            create_credit_secret_user_request,
            credit_request
        )

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account_response.id,
            amount=credit_request.amount
        )

        credit_repay_response = api_manager.user_steps.credit_repay(
            create_credit_secret_user_request,
            credit_repay_request
        )

        assert credit_repay_response.creditId == credit_repay_request.creditId
        assert credit_repay_response.amountDeposited == credit_repay_request.amount


    @pytest.mark.parametrize(
        "amount",
        [
           (1000),
           (4999)

        ]
    )
    def test_credit_repay_invalid(self, api_manager, create_credit_secret_user_request, amount):
        account_response = api_manager.user_steps.create_account(create_credit_secret_user_request)

        assert account_response.balance == 0

        credit_request = CreditRequest(
            accountId=account_response.id,
            amount=5000,
            termMonths=12
        )

        credit_response = api_manager.user_steps.credit_request(
            create_credit_secret_user_request,
            credit_request
        )

        credit_repay_request = CreditRepayRequest(
            creditId=credit_response.creditId,
            accountId=account_response.id,
            amount=amount
        )

        api_manager.user_steps.credit_repay_invalid(
            create_credit_secret_user_request,
            credit_repay_request,
            expected_status=422
        )










