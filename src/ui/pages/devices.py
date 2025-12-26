"""
Devices Page - Smartwatch Management
File: src/ui/pages/devices.py

Notes:
- Database imports are deferred to runtime in on_device_added() and refresh_devices()
  to avoid SQLAlchemy typing/circular-import issues during module import.
- If database access fails, the UI falls back to in-memory sample devices.
"""

from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QWidget as QW
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class DeviceCard(QFrame):
    """Display card for connected device"""

    sync_requested = pyqtSignal(str)  # device_id

    def __init__(self, device_info: dict, parent=None):
        super().__init__(parent)
        self.device_info = device_info
        self.setup_ui()

    def setup_ui(self):
        """Setup device card UI"""
        self.setObjectName("deviceCard")
        self.setStyleSheet("""
            #deviceCard {
                background-color: #1E1E1E;
                border: 2px solid #2D2D2D;
                border-radius: 15px;
                padding: 20px;
            }
            #deviceCard:hover {
                border-color: #00BFA5;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header: Icon + Name
        header = QHBoxLayout()

        icon = QLabel("⌚")
        icon.setFont(QFont("Segoe UI Emoji", 32))
        header.addWidget(icon)

        name_layout = QVBoxLayout()
        name = QLabel(self.device_info.get("name", "Unknown Device"))
        name.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        name.setStyleSheet("color: white;")
        name_layout.addWidget(name)

        model = QLabel(self.device_info.get("model", ""))
        model.setFont(QFont("Segoe UI", 10))
        model.setStyleSheet("color: #888;")
        name_layout.addWidget(model)

        header.addLayout(name_layout)
        header.addStretch()

        # Battery
        battery = self.device_info.get("battery", 0)
        battery_label = QLabel(f"🔋 {battery}%")
        battery_label.setFont(QFont("Segoe UI", 12))
        battery_label.setStyleSheet("color: #00BFA5;")
        header.addWidget(battery_label)

        layout.addLayout(header)

        # Status
        status = self.device_info.get("status", "disconnected")
        status_colors = {
            "connected": "#00BFA5",
            "disconnected": "#666",
            "syncing": "#FFD54F",
            "error": "#FF5252"
        }

        status_label = QLabel(f"● {status.title()}")
        status_label.setStyleSheet(f"color: {status_colors.get(status, '#666')};")
        layout.addWidget(status_label)

        # Last sync
        last_sync = self.device_info.get("last_sync", "Never")
        sync_label = QLabel(f"Last sync: {last_sync}")
        sync_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(sync_label)

        # Sync button
        sync_btn = QPushButton("🔄 Sync Now")
        sync_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        sync_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00E5CC;
            }
        """)
        sync_btn.clicked.connect(
            lambda: self.sync_requested.emit(self.device_info.get("id", ""))
        )
        layout.addWidget(sync_btn)


class DevicesPage(QWidget):
    """Devices management page"""

    def __init__(self):
        super().__init__()
        # in-memory fallback devices until DB can be loaded
        self.devices: List[Dict] = [
            {"id": "1", "name": "Mi Band 7", "model": "Xiaomi", "battery": 85, "status": "connected", "last_sync": "5 minutes ago"},
            {"id": "2", "name": "Fitbit Charge 5", "model": "Fitbit", "battery": 62, "status": "connected", "last_sync": "1 hour ago"},
        ]
        # UI references we will need later
        self._scroll_layout = None  # type: Optional[QVBoxLayout]
        self._scroll_content = None  # type: Optional[QW]
        self.setup_ui()
        # Try to load real devices from DB at runtime (deferred)
        self.refresh_devices()

    def setup_ui(self):
        """Setup devices page UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Connected Devices")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Add device button
        add_btn = QPushButton("➕ Add Device")
        add_btn.setFixedSize(150, 50)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00E5CC;
            }
        """)
        add_btn.clicked.connect(self.show_add_device_dialog)
        header_layout.addWidget(add_btn)

        main_layout.addLayout(header_layout)

        # Devices grid (scrollable)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QW()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Save references for later refresh
        self._scroll_layout = scroll_layout
        self._scroll_content = scroll_content

        # Initially populate with in-memory sample devices; refresh_devices() will replace if DB available
        for device in self.devices:
            card = DeviceCard(device)
            card.sync_requested.connect(self.sync_device)
            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

    def show_add_device_dialog(self):
        """Show add device dialog

        The dialog should emit a 'device_added' signal with a dict payload when the user
        completes pairing. Connect that signal to self.on_device_added(dialog_payload).
        """
        # TODO: Replace this with your actual AddDeviceDialog creation/logic.
        # Example usage:
        # dialog = AddDeviceDialog(self)
        # dialog.device_added.connect(self.on_device_added)
        # dialog.exec()
        print("Add device dialog (open your actual dialog here)")

    def on_device_added(self, device_info: dict):
        """
        Slot called when AddDeviceDialog emits device_added.

        Defer database imports and operations to runtime to avoid SQLAlchemy typing
        errors at module import time. If DB operations fail, fall back to the in-memory list
        and update UI so user sees the newly added device.
        """
        # Defensive check
        if not isinstance(device_info, dict):
            print("on_device_added: invalid payload, expected dict")
            return

        # Attempt to add to DB (deferred import)
        added_to_db = False
        try:
            # Import inside function to avoid SQLAlchemy typing/circular imports at module import
            from ...database.device_repository import DeviceRepository  # adjust path if needed
            repo = DeviceRepository()
            # expected repository method; adjust to your actual signature
            repo.add_device(device_info)
            added_to_db = True
        except Exception as e:
            # Log and continue with fallback
            print(f"DB add device failed (deferred import): {e}")

        # Update UI (always)
        try:
            # Update in-memory list so refresh works even if DB failed
            self.devices.append(device_info)
            # Add a new card at the top of the list
            card = DeviceCard(device_info)
            card.sync_requested.connect(self.sync_device)
            # Insert before the stretch at end; layout insert position 0 inserts at top
            if self._scroll_layout:
                # Remove the stretch at the end temporarily if present
                # (we'll just insert before index 0 to keep newest at top)
                self._scroll_layout.insertWidget(0, card)
            else:
                print("Warning: scroll layout not initialized; new device will not be visible until refresh.")
        except Exception as e:
            print(f"UI update after device add failed: {e}")

        if added_to_db:
            print("Device added to database and UI updated.")
        else:
            print("Device added to UI (DB add failed or skipped).")

    def refresh_devices(self):
        """
        Load devices from the database (deferred import). If DB fails, use in-memory fallback.
        Rebuilds the devices list in the UI.
        """
        devices_to_show = self.devices
        try:
            from ...database.device_repository import DeviceRepository  # adjust path if needed
            repo = DeviceRepository()
            devices_to_show = repo.list_devices()  # expected to return list[dict]
        except Exception as e:
            # Log and use fallback
            print(f"Could not load devices from DB (deferred import): {e}")
            devices_to_show = self.devices

        # Rebuild UI list
        if not self._scroll_layout:
            print("refresh_devices: scroll layout not ready")
            return

        # Clear layout items except the stretch at end
        self._clear_layout(self._scroll_layout)

        for device in devices_to_show:
            try:
                card = DeviceCard(device)
                card.sync_requested.connect(self.sync_device)
                self._scroll_layout.addWidget(card)
            except Exception as e:
                print(f"Failed to create device card for {device}: {e}")

        self._scroll_layout.addStretch()

    def sync_device(self, device_id: str):
        """Sync specific device"""
        print(f"Syncing device: {device_id}")
        # TODO: Implement actual sync wiring to SyncManager / device connectors

    @staticmethod
    def _clear_layout(layout):
        """Remove all widgets from a layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
