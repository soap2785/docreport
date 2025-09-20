import json
from sqlite3 import connect

from flask import request


async def getData():
    page = int(json.loads(request.data)['page'])
    with connect('databaseSITE.db', timeout=300) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders ORDER BY id DESC")
        data = cur.fetchall()
    result = []
    last_page = page // 20 + 2
    if page > last_page or page < 1:
        return []
    try:
        if last_page == page:
            for i in range(page * 20 - 20, len(data)):
                result.append(data[i])
        else:
            for i in range(page*20-20,page*20):
                result.append(data[i])
    except IndexError:
        pass

    result = json.dumps(result, ensure_ascii=False).encode('utf8')
    return result