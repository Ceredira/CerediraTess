import base64
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from CerediraTess import request_processor_get, request_processor_post

WEB_ROOT = os.getcwd()


class Handler(BaseHTTPRequestHandler):
    """Главный класс для веб-сервера.

    Класс перехватывает все GET и POST запросы приходящие в сервер по
    указанному порту.
    """

    def __init__(self, list_of_agents, list_of_users, agents_locker, *args, **kwargs):
        """Конструктор класса, нужен для инициализации словаря с результатами запросов SQL."""

        self.list_of_agents = list_of_agents
        self.list_of_users = list_of_users
        self.agents_locker = agents_locker
        logger = logging.getLogger("CerediraTess.Handler.__init__")
        logger.info("Initialize handler")

        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        return

    def do_GET(self):
        """
        Метод обрабатывает все входящие GET запросы. Сделан в виде диспетчера - дерево условий, который в
        зависимости от пути GET запроса, выполняет необходимую обработку, если необходимой обработки нет,
        то возвращаем в ответ файл, которй лежит по указанному пути относительно директории сайта.
        На текущий момент определена следующая логика:
            * если путь запроса "/" или корень (адрес сайта без пути), то возвращаем файл, который лежит в
            views/index.html
            * если путь запроса все что угодно другое, то пытаемся найти этот файл по пути корень проекта + путь запроса
            * если необходимо реализовать какие либо методы, их нужно добавить перед последним else
            с произвольным путем, например /api/methodName.
        Всю логику выполняемую по определенному пути необходимо реализовать в файле get_request_processor. Каждый такой
        метод должен возвращать HTTP код ответа, заголовки ответа и тело ответа.
        В случае, если во время работы запроса, произойдет ошибка, то в ответ на запрос вернется 500 HTTP код ошибки
        и тест ошибки.
        """
        logger = logging.getLogger("CerediraTess.Handler.do_GET")
        logger.info(f'Request URL {self.path}')
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(b'Hello world\t' + threading.currentThread().getName().encode() +
        # b'\t' + str(threading.active_count()).encode() + b'\n')
        try:
            if self.path == "/":  # Запрос корня сайта
                resp_code, resp_headers, body = request_processor_get.get_file_from_server(
                    os.path.join(WEB_ROOT, '\\www\\index.html'))
            else:  # Запрос любой другой страницы
                resp_code, resp_headers, body = request_processor_get.get_file_from_server(os.path.join(
                    WEB_ROOT, self.path))

            self.make_response(resp_code, body, **resp_headers)
        except Exception as e:  # Вылетим сюда при возникновении любой ошибки
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error(f'GET: raised exception: {e}', exc_info=True)
            # logger.error(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self.send_error(500, explain=str(e))

    def do_POST(self):
        logger = logging.getLogger("CerediraTess.Handler.do_POST")
        logger.info(f'Request URL {self.path}')

        try:
            # Получить тело запроса, для использования далее
            content_len = int(self.headers.get_all('Content-Length', 0)[0])
            post_body = self.rfile.read(content_len)
            logger.info(f'Request body:\n{post_body}')
            auth = self.headers.get('Authorization', None)

            if auth is None:
                self.send_error(401, message=str(
                    'Authorization header expected. Authorization must be base64(username:password).'))
                return

            decoded_auth = base64.b64decode(auth).decode()
            if ':' in decoded_auth:
                username, password = decoded_auth.split(':', maxsplit=1)
                user = next((x for x in self.list_of_users if x.username == username), None)

                if not user:
                    self.send_error(403, message=str(f'User {username} does not exists in service.'))
                    return
                if not user.check_password(password):
                    self.send_error(401, message=str(f'Wrong password used. Authorization failed.'))
                    return

                logger.info(f'User: {user.username}')
            else:
                self.send_error(401, message=str(
                    'Error in Authorization header (expected :). Authorization must be base64(username:password).'))
                return

            if self.path == '/post_response':
                resp_code, resp_headers, body = request_processor_post.post_response(post_body)
                # threading.currentThread().getName().encode() + b'\t' + str(threading.active_count()).encode() + b'\n')
            elif self.path.startswith('/executeScript/'):
                script_name = self.path[15:]
                resp_code, resp_headers, body = request_processor_post.execute_script(user, self.list_of_agents,
                                                                                      script_name, post_body)
            elif self.path.startswith('/agentsLock'):
                resp_code, resp_headers, body = request_processor_post.agents_lock(self.agents_locker, user.username,
                                                                                   post_body)
            elif self.path.startswith('/agentsUnlock'):
                resp_code, resp_headers, body = request_processor_post.agents_unlock(self.agents_locker, user.username,
                                                                                     post_body)
            elif self.path.startswith('/agentsStatus'):
                resp_code, resp_headers, body = request_processor_post.agents_status(self.agents_locker, user.username,
                                                                                     post_body)
            else:
                self.send_error(404, message=str(self.path))
                return

            self.make_response(resp_code, body, **resp_headers)

        # Вылетим сюда при возникновении любой ошибки
        except Exception as e:
            logger.error(f'POST: raised exception: {e}', exc_info=True)
            # logger.error(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            self.send_error(500, explain=str(e))

    def make_response(self, code, body, **kwargs):
        """Метод формирования ответа на запрос к серверу"""
        self.send_response(code)
        for key in kwargs:
            self.send_header(key, kwargs[key])
        self.end_headers()
        self.wfile.write(body)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    """Класс для обработки запросов в параллельных патоках."""
    pass
