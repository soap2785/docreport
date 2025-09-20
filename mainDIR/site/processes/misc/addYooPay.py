# https://docreport.ru/yookassa/alert
import uuid
from sqlite3 import connect

from yookassa import Configuration, Payment

Configuration.account_id = '294785'
Configuration.secret_key = 'live_vZqtsQ7vFu97dm9C9St9xEOH0d_YY7NaURuhCAB7qCY'


def addYooPay(summa, currency, id_document, data):
    request = {
        "paymentSumma": summa,
        "paymentCurrency": currency
    }

    idempotence_key = str(uuid.uuid4())
    with connect('databaseSITE.db') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE orders SET idForOrder = ? WHERE id = ?", (idempotence_key, id_document))
        conn.commit()
    paySum = str('{:.2f}'.format(request['paymentSumma']))
    description = "Оплата по счету #" + id_document

    params_pay = {
        "amount": {
            "value": paySum,
            "currency": request['paymentCurrency']
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://docreport.ru/"
        },
        "capture": True,
        "description": description,
        "metadata": {
            'orderNumber': id_document,
            'orderMerchNumber': idempotence_key,
        },
        "receipt": {
            "customer": {
                "full_name": data.get('surname') + " " + data.get('name') + " " + data.get('patronymic'),
                "email": data.get('email'),
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




