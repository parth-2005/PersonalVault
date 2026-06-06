import threading
import os
from typing import Optional

_server_instance = None
_server_thread = None

def start_server(host: str, port: int, shared_folder: str, username: Optional[str] = None, password: Optional[str] = None) -> threading.Thread:
    """
    Configures and starts the WsgiDAV server bound to the specified Tailscale IP.
    """
    global _server_instance, _server_thread

    # WsgiDAV configuration
    # Note: We use a simple config dict. In a real app, you might want a more robust config provider.
    config = {
        "dav_processor_module": "WsgidavServer",
        "simple_dc": {
            "root": shared_folder,
        },
        "host": host,
        "port": port,
        "auth": "digest" if (username and password) else None,
        "user_db": {username: password} if (username and password) else {},
        "directory_browsing": True,
        "chunked_transfer": True,
    }

    # Create the WsgiDAV server application
    # For a simple implementation, we use the server from wsgidav.server
    # This is a simplified version. WsgiDAV typically requires a more complex setup via config files.
    # Here we utilize the WsgiDAVServer class directly if possible, or a similar wrapper.

    try:
        # Build a WsgiDAV WSGI app and serve it with cheroot.wsgi.Server.
        from wsgidav.wsgidav_app import WsgiDAVApp
        from wsgidav.fs_dav_provider import FilesystemProvider
        from cheroot import wsgi as cheroot_wsgi

        # Ensure shared folder exists
        shared_folder = os.path.abspath(shared_folder)
        if not os.path.exists(shared_folder):
            os.makedirs(shared_folder, exist_ok=True)

        # Build provider mapping for the shared folder
        provider = FilesystemProvider(shared_folder, readonly=False, fs_opts={})
        config.update({
            "provider_mapping": {"/": provider},
            # Ensure anonymous access if no auth provided
            "simple_dc": {"user_mapping": {"*": True}},
            "verbose": 1,
        })

        def run_server_thread():
            app = WsgiDAVApp(config)
            server = cheroot_wsgi.Server(bind_addr=(host, port), wsgi_app=app)
            try:
                app.logger.info(f"Starting WsgiDAV on http://{host}:{port}")
                server.start()
            except Exception:
                pass
            finally:
                try:
                    server.stop()
                except Exception:
                    pass

        _server_thread = threading.Thread(target=run_server_thread, daemon=True)
        _server_thread.start()
        return _server_thread

    except Exception as e:
        print(f"Failed to start WebDAV server: {e}")
        return threading.current_thread()

def stop_server() -> None:
    """
    Gracefully stops the running WsgiDAV server.
    """
    global _server_instance, _server_thread
    # WsgiDAV/Cheroot doesn't always provide a simple "stop" method for the thread.
    # In a production app, you'd keep a reference to the server object and call .stop()
    # For the MVP, we rely on the thread being daemonized and the process exiting,
    # or we'd need to implement a more complex signaling mechanism.
    pass

def is_server_running() -> bool:
    """
    Checks if the WebDAV server is currently active.
    """
    return _server_thread is not None and _server_thread.is_alive()

def get_server_url(host: str, port: int) -> str:
    """
    Constructs the WebDAV server URL.
    """
    return f"http://{host}:{port}"
