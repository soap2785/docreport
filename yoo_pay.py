#https://docreport.ru/yookassa/alert
import uuid
from yookassa import Configuration, Payment

from mainDIR.config import yooPayAccountId, yooPaySecretKey

from command_to_db import set_id_order

Configuration.account_id = yooPayAccountId
Configuration.secret_key = yooPayAccountId



def addYooKassaPay(summa, currency, id_document, data):
    request = {
        "paymentSumma": summa,
        "paymentCurrency": currency
    }

    
    idempotence_key = str(uuid.uuid4())
    set_id_order(id_document, idempotence_key)
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
                    "full_name": data.get('surname')+" "+data.get('name')+" "+data.get('patronymic'),
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




