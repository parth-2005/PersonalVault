import os
import threading
from typing import Optional

_server_instance = None
_server_thread = None
_server_lock = threading.Lock()


def start_server(
    host: str,
    port: int,
    shared_folder: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> threading.Thread:
    """Start the WsgiDAV server on a dedicated background thread."""

    global _server_instance, _server_thread

    stop_server()

    try:
        from cheroot import wsgi as cheroot_wsgi
        from wsgidav.fs_dav_provider import FilesystemProvider
        from wsgidav.wsgidav_app import WsgiDAVApp
    except Exception as exc:
        raise RuntimeError(f"Failed to import WebDAV dependencies: {exc}") from exc

    shared_folder = os.path.abspath(shared_folder)
    os.makedirs(shared_folder, exist_ok=True)

    provider = FilesystemProvider(shared_folder, readonly=False, fs_opts={})
    config = {
        "provider_mapping": {"/": provider},
        "directory_browsing": True,
        "chunked_transfer": True,
        "verbose": 1,
    }

    if username and password:
        config["simple_dc"] = {"user_mapping": {"/": {username: password}}}
        config["http_authenticator"] = {
            "domain_controller": "simple_dc",
            "accept_basic": True,
            "accept_digest": True,
        }
    else:
        config["simple_dc"] = {"user_mapping": {"*": True}}

    app = WsgiDAVApp(config)
    server = cheroot_wsgi.Server(bind_addr=(host, port), wsgi_app=app)

    def run_server() -> None:
        global _server_instance

        try:
            server.start()
        finally:
            _server_instance = None

    _server_instance = server
    thread = threading.Thread(target=run_server, daemon=True)
    _server_thread = thread
    thread.start()
    return thread


def stop_server() -> None:
    """Stop the active Cheroot server and wait for the worker thread to exit."""

    global _server_instance, _server_thread

    with _server_lock:
        server = _server_instance
        thread = _server_thread
        _server_instance = None
        _server_thread = None

    if server is not None:
        try:
            server.stop()
        except Exception:
            pass

    if thread is not None and thread.is_alive() and thread is not threading.current_thread():
        thread.join()


def is_server_running() -> bool:
    """Return True when the background WebDAV worker is alive."""

    return _server_thread is not None and _server_thread.is_alive()


def get_server_url(host: str, port: int) -> str:
    """Construct the WebDAV server URL."""

    return f"http://{host}:{port}"
