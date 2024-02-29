import pytest
import schemathesis
from ddf import G
from django.contrib.auth import get_user_model
from django.core.wsgi import get_wsgi_application
from django.db import connection
from rest_framework.authtoken.models import Token

application = get_wsgi_application()
schema = schemathesis.from_wsgi(
    "/swagger/?format=openapi",
    application,
    validate_schema=True,
    data_generation_methods=[
        schemathesis.DataGenerationMethod.positive,
        schemathesis.DataGenerationMethod.negative,
    ],
    sanitize_output=False,
)

User = get_user_model()


@pytest.mark.skipif(
    connection.vendor == "sqlite", reason="broken on sqlite due to bigint issues"
)
@pytest.mark.django_db(transaction=True)
@schema.parametrize()
def test_api_stateless(case):
    user = G(User)
    token = G(Token, user=user)
    response = case.call_wsgi(
        app=application, headers={"Authorization": f"Bearer {token.key}"}
    )
    case.validate_response(
        response,
    )
