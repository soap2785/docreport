import json
from sqlite3 import connect

from flask import request


async def fuse():
    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        idDocument = data['id_document'].replace('Заказ №','')
        idOrder = data['id_order']
        with connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("UPDATE orders SET idForOrder = ? WHERE id = ?", (idOrder, idDocument))
        return "ID платежа успешно привязан"
    except:
        return "Ошибка при установке ID платежа"