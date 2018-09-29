from server import create_app


app = create_app()

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000),
                               app,
                               handler_class=WebSocketHandler)
    server.serve_forever()
