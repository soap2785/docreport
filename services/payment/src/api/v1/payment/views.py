from uuid import uuid4
from json import dumps

from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from yookassa import Configuration, Payment

from .models import PaymentSchema
from infrastructure.repositories.postgresql.request import (
    PostgreSQLRequestRepository
)

router = APIRouter(prefix='/payment')


@router.post("", response_model=PaymentSchema)
async def payment(payload: PaymentSchema) -> JSONResponse:
    if payload.testing or payload.from_bot:
        return JSONResponse({'access': True}, status.HTTP_200_OK)
    request = {
        "paymentSumma": payload.summa,
        "paymentCurrency": payload.currency
    }

    idempotence_key = str(uuid4())
    repo = PostgreSQLRequestRepository()
    await repo.add((payload.id, idempotence_key))
    paySum = str('{:.2f}'.format(request['paymentSumma']))
    description = f"Оплата по счету #{payload.id}"

    params_pay = {
        "amount": {
            "value": paySum,
            "currency": request['paymentCurrency']
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://docreportdev.ru/"
        },
        "capture": True,
        "description": description,
        "metadata": {
            'orderNumber': payload.id,
            'orderMerchNumber': idempotence_key,
        },
        "receipt": {
            "customer": {
                "full_name": (
                    f"{payload.surname} {payload.name} {payload.patronymic}"
                ), "email": payload.email,
            },
            "items": [
                {
                    "description": "Оплата запроса",
                    "quantity": "1.00",
                    "amount": {
                        "value": request['paymentSumma'],
                        "currency": request['paymentCurrency']
                    },
                    "vat_code": "1",
                    "payment_mode": "full_payment",
                    "payment_subject": "service",
                },
            ],
        }
    }

    payment = Payment.create(params_pay, idempotence_key)
    return payment.confirmation.confirmation_url
