"""
AI Assistant Page

Tahap ini:
- Panel chat sederhana
- Jika OPENAI_API_KEY tersedia -> panggil OpenAI ChatCompletion
- Jika tidak ada key / error -> fallback ke mock response
"""

import os

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QLineEdit,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except Exception:
    OpenAI = None  # type: ignore
    _OPENAI_AVAILABLE = False


class _AIWorker(QThread):
    """Background worker untuk memanggil OpenAI agar UI tidak nge-freeze."""

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt: str, parent=None):
        super().__init__(parent)
        self.prompt = prompt

    def run(self):
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not (_OPENAI_AVAILABLE and api_key):
            self.error.emit("API belum dikonfigurasi. Menggunakan mode mock.")
            return
        try:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Kamu adalah asisten kesehatan yang ramah dan hati-hati. "
                            "Berikan saran umum, jangan menggantikan dokter, "
                            "dan selalu sarankan konsultasi profesional untuk hal serius."
                        ),
                    },
                    {"role": "user", "content": self.prompt},
                ],
                temperature=0.7,
                max_tokens=600,
            )
            content = resp.choices[0].message.content or ""
            self.finished.emit(content.strip())
        except Exception as e:
            self.error.emit(f"Gagal memanggil OpenAI: {e}")


class AIAssistantPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(30, 30, 30, 30)
        root.setSpacing(16)

        header = QLabel("AI Health Assistant")
        header.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        header.setStyleSheet("color: white;")
        sub = QLabel("Tanya apa saja seputar kesehatan. (Saat ini mock response)")
        sub.setFont(QFont("Segoe UI", 11))
        sub.setStyleSheet("color: #888;")

        root.addWidget(header)
        root.addWidget(sub)

        chat_card = QFrame()
        chat_card.setStyleSheet("""
            QFrame {
                background: #1b1b1b;
                border: 1px solid #262626;
                border-radius: 14px;
            }
        """)
        chat_layout = QVBoxLayout(chat_card)
        chat_layout.setContentsMargins(14, 14, 14, 14)
        chat_layout.setSpacing(10)

        # Scrollable history
        self.history_view = QTextEdit()
        self.history_view.setReadOnly(True)
        self.history_view.setStyleSheet("""
            QTextEdit {
                background: #111;
                color: #e5e7eb;
                border: 1px solid #1f1f1f;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.history_view.setMinimumHeight(260)
        chat_layout.addWidget(self.history_view)

        # Input row
        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Tulis pertanyaan Anda...")
        self.input.setStyleSheet("""
            QLineEdit {
                background: #111;
                color: #e5e7eb;
                border: 1px solid #1f1f1f;
                border-radius: 10px;
                padding: 12px;
            }
            QLineEdit:focus {
                border-color: #00BFA5;
            }
        """)

        send_btn = QPushButton("Kirim")
        send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        send_btn.setFixedWidth(100)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #00E5CC; }
        """)
        send_btn.clicked.connect(self.on_send)

        input_row.addWidget(self.input, 1)
        input_row.addWidget(send_btn)
        chat_layout.addLayout(input_row)

        root.addWidget(chat_card)
        root.addStretch()

        self._current_worker: _AIWorker | None = None

    # ------------------------------------------------------------------ actions
    def on_send(self):
        text = self.input.text().strip()
        if not text:
            return
        self.append_chat("Anda", text)
        self.input.clear()

        # Tampilkan status sementara
        self.append_chat("AI", "<i>Sedang memikirkan jawaban...</i>")

        # Jika tidak ada API key / library, langsung mock
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not (_OPENAI_AVAILABLE and api_key):
            reply = self.mock_reply(text)
            self.append_chat("AI", reply)
            return

        # Jalankan worker di background
        if self._current_worker and self._current_worker.isRunning():
            return  # hindari spam
        self._current_worker = _AIWorker(text, self)
        self._current_worker.finished.connect(self.on_ai_finished)
        self._current_worker.error.connect(self.on_ai_error)
        self._current_worker.start()

    def on_ai_finished(self, reply: str):
        self.append_chat("AI", reply)

    def on_ai_error(self, msg: str):
        self.append_chat("AI", self.mock_reply(msg))

    def append_chat(self, sender: str, message: str):
        self.history_view.append(f"<b>{sender}:</b> {message}")

    def mock_reply(self, user_text: str) -> str:
        return (
            "Saat ini AI Assistant berjalan dalam mode demo.\n"
            "Tambahkan OPENAI_API_KEY di file .env untuk mengaktifkan jawaban AI sesungguhnya."
        )

