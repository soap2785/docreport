from config import app, IP_site, PORT_site


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run(host = IP_site, port = PORT_site, debug = True))