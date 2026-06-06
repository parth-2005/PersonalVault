import sys
from typing import Optional

from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QCloseEvent, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

import config
import server
import tailscale

VERSION = "0.1.0"


class SignalBridge(QObject):
    status_changed = pyqtSignal(bool, object)


class SettingsDialog(QDialog):
    settings_saved = pyqtSignal(dict)

    def __init__(self, current_config: dict, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("ShulkerBox Settings")
        self.setModal(False)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)

        self.shared_folder_input = QLineEdit(self)
        self.port_input = QSpinBox(self)
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(int(current_config.get("port", 8765)))
        self.shared_folder_input.setText(current_config.get("shared_folder_path", ""))

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self._browse_folder)

        shared_row = QHBoxLayout()
        shared_row.addWidget(self.shared_folder_input)
        shared_row.addWidget(browse_button)

        form_layout = QFormLayout()
        form_layout.addRow("Shared Folder", self._wrap_layout(shared_row))
        form_layout.addRow("Port", self.port_input)

        button_row = QHBoxLayout()
        button_row.addStretch(1)

        save_button = QPushButton("Save", self)
        cancel_button = QPushButton("Cancel", self)
        save_button.clicked.connect(self._save)
        cancel_button.clicked.connect(self.hide)
        button_row.addWidget(save_button)
        button_row.addWidget(cancel_button)

        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addLayout(button_row)

        self.resize(520, 140)

    def _wrap_layout(self, layout: QHBoxLayout) -> QWidget:
        container = QWidget(self)
        container.setLayout(layout)
        return container

    def _browse_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Shared Folder", self.shared_folder_input.text())
        if folder:
            self.shared_folder_input.setText(folder)

    def _save(self) -> None:
        current_config = config.load_config()
        current_config["shared_folder_path"] = self.shared_folder_input.text().strip()
        current_config["port"] = int(self.port_input.value())
        self.settings_saved.emit(current_config)
        self.hide()

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.hide()


class ShulkerBoxApp(QObject):
    def __init__(self, qt_app: QApplication) -> None:
        super().__init__()
        self.qt_app = qt_app
        self.config = config.load_config()
        self.tailscale_ip: Optional[str] = None
        self.is_connected = False

        self.bridge = SignalBridge()
        self.bridge.status_changed.connect(self._apply_tailscale_status)

        self.tray_icon = QSystemTrayIcon(self._create_tray_icon(), self.qt_app)
        self.tray_icon.setToolTip("ShulkerBox")
        self.tray_icon.setContextMenu(self._build_menu())
        self.tray_icon.activated.connect(self._tray_activated)

        self.settings_window = SettingsDialog(self.config)
        self.settings_window.settings_saved.connect(self._save_settings)

    def _create_tray_icon(self) -> QIcon:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.GlobalColor.black)
        painter.drawRoundedRect(10, 12, 44, 40, 8, 8)
        painter.setBrush(Qt.GlobalColor.darkYellow)
        painter.drawRoundedRect(16, 18, 32, 28, 5, 5)
        painter.setBrush(Qt.GlobalColor.green if self.is_connected else Qt.GlobalColor.gray)
        painter.drawEllipse(42, 42, 12, 12)
        painter.end()

        return QIcon(pixmap)

    def _refresh_tray_icon(self) -> None:
        self.tray_icon.setIcon(self._create_tray_icon())

    def _build_menu(self) -> QMenu:
        menu = QMenu()

        settings_action = QAction("Settings", self.qt_app)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)

        copy_ip_action = QAction("Copy Tailscale IP", self.qt_app)
        copy_ip_action.triggered.connect(self.copy_tailscale_ip)
        menu.addAction(copy_ip_action)

        menu.addSeparator()

        quit_action = QAction("Quit", self.qt_app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        return menu

    def _tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_settings()

    def _apply_tailscale_status(self, active: bool, ip: Optional[str]) -> None:
        was_connected = self.is_connected
        self.is_connected = active
        self.tailscale_ip = ip
        self._refresh_tray_icon()

        if active and ip:
            self.start_webdav_server(ip)
        elif was_connected or server.is_server_running():
            server.stop_server()

    def _handle_tailscale_status_change(self, active: bool, ip: Optional[str]) -> None:
        self.bridge.status_changed.emit(active, ip)

    def _save_settings(self, new_config: dict) -> None:
        self.config = new_config
        config.save_config(new_config)
        if self.is_connected and self.tailscale_ip:
            server.stop_server()
            self.start_webdav_server(self.tailscale_ip)

    def start_webdav_server(self, ip: str) -> None:
        server.start_server(
            host=ip,
            port=int(self.config.get("port", 8765)),
            shared_folder=self.config.get("shared_folder_path", ""),
            username=self.config.get("webdav_username") or None,
            password=self.config.get("webdav_password") or None,
        )

    def open_settings(self) -> None:
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def copy_tailscale_ip(self) -> None:
        ip = self.tailscale_ip or tailscale.get_tailscale_ip()
        if not ip:
            QMessageBox.information(None, "ShulkerBox", "No Tailscale IP is currently available.")
            return

        self.qt_app.clipboard().setText(ip)
        self.tray_icon.showMessage("ShulkerBox", f"Copied {ip} to the clipboard.", QSystemTrayIcon.MessageIcon.Information, 2000)

    def quit_app(self) -> None:
        server.stop_server()
        self.tray_icon.hide()
        self.qt_app.quit()

    def run(self) -> int:
        if not tailscale.is_tailscale_installed():
            QMessageBox.warning(None, "ShulkerBox", "Tailscale is not installed. Install it from tailscale.com/download.")

        self.tray_icon.show()

        initial_ip = tailscale.get_tailscale_ip()
        self._handle_tailscale_status_change(initial_ip is not None, initial_ip)
        tailscale.poll_tailscale_status(self._handle_tailscale_status_change)

        return self.qt_app.exec()


def main() -> None:
    qt_app = QApplication(sys.argv)
    qt_app.setQuitOnLastWindowClosed(False)
    qt_app.setApplicationName("ShulkerBox")
    qt_app.setApplicationVersion(VERSION)

    app = ShulkerBoxApp(qt_app)
    sys.exit(app.run())


if __name__ == "__main__":
    main()
