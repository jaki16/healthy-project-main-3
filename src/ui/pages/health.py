"""
Health Page

Fitur:
- Form input data kesehatan (berat, tekanan darah, detak jantung, gula darah, catatan)
- Validasi input
- Simpan ke database SQLite (tabel health_entries lokal)
- Riwayat data (tabel)
- Grafik tren sederhana (berat)
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import sqlite3

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QDoubleSpinBox,
    QSpinBox,
    QPushButton,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis


class HealthPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # DB path (pakai file healthtrack.db yang sudah ada)
        self.db_path = (
            Path(__file__).parent.parent.parent.parent / "data" / "healthtrack.db"
        )
        self.init_db()
        self.records: List[Dict[str, Any]] = []
        self.series = QLineSeries()
        self.axis_x = None
        self.axis_y = None
        self.setup_ui()
        self.load_data()

    # ------------------------------------------------------------------ UI
    def setup_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(
            """
            QScrollArea { background-color: #121212; border: none; }
            QScrollBar:vertical {
                background-color: #1E1E1E;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #3D3D3D;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover { background-color: #00BFA5; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """
        )

        container = QWidget()
        scroll.setWidget(container)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = self.build_header()
        layout.addWidget(header)

        summary_row = self.build_summary_cards()
        layout.addWidget(summary_row)

        form_card = self.build_form()
        layout.addWidget(form_card)

        chart_card = self.build_chart_card()
        layout.addWidget(chart_card)

        table_card = self.build_table()
        layout.addWidget(table_card)

        layout.addStretch()
        root_layout.addWidget(scroll)

    def build_header(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)

        title = QLabel("Health Monitor")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: white; letter-spacing: 0.2px;")

        subtitle = QLabel("Catat vitals harian dan pantau trennya")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #888;")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        layout.addLayout(text_layout)
        layout.addStretch()
        return container

    def build_summary_cards(self):
        wrap = QFrame()
        wrap.setStyleSheet("QFrame { background: transparent; border: none; }")
        row = QHBoxLayout(wrap)
        row.setSpacing(12)

        latest = self.get_latest_values()
        cards = [
            ("Berat", f"{latest.get('weight', '-')}", "kg", "#22c55e"),
            (
                "Tekanan Darah",
                f"{latest.get('systolic', '-')}/{latest.get('diastolic', '-')}",
                "mmHg",
                "#60a5fa",
            ),
            ("Detak Jantung", f"{latest.get('heart_rate', '-')}", "bpm", "#f97316"),
            ("Gula Darah", f"{latest.get('blood_sugar', '-')}", "mg/dL", "#a855f7"),
        ]
        for title, value, unit, color in cards:
            row.addWidget(self.create_stat_card(title, value, unit, color))
        row.addStretch()
        return wrap

    def create_stat_card(self, title: str, value: str, unit: str, color: str):
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background: #1b1b1b;
                border-radius: 14px;
                border: 1px solid #2a2a2a;
            }}
            QFrame:hover {{
                border-color: {color};
                background: #1f1f1f;
            }}
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Segoe UI", 10))
        title_lbl.setStyleSheet("color: #9ca3af;")

        val_row = QHBoxLayout()
        val_lbl = QLabel(value)
        val_lbl.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        val_lbl.setStyleSheet(f"color: {color};")
        unit_lbl = QLabel(unit)
        unit_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        unit_lbl.setStyleSheet("color: #6b7280; margin-top: 6px;")
        val_row.addWidget(val_lbl)
        val_row.addWidget(unit_lbl)
        val_row.addStretch()

        layout.addWidget(title_lbl)
        layout.addLayout(val_row)
        return card

    def build_form(self):
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background: #1b1b1b;
                border-radius: 16px;
                border: 1px solid #262626;
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        title = QLabel("Tambah Data Kesehatan")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setVerticalSpacing(10)
        grid.setHorizontalSpacing(16)

        self.weight = QDoubleSpinBox()
        self.weight.setRange(20, 300)
        self.weight.setSuffix(" kg")
        self.weight.setDecimals(1)
        self.weight.setValue(70.0)

        self.sys = QSpinBox()
        self.sys.setRange(70, 250)
        self.sys.setSuffix(" mmHg")
        self.sys.setValue(120)

        self.dia = QSpinBox()
        self.dia.setRange(40, 200)
        self.dia.setSuffix(" mmHg")
        self.dia.setValue(80)

        self.hr = QSpinBox()
        self.hr.setRange(30, 220)
        self.hr.setSuffix(" bpm")
        self.hr.setValue(75)

        self.sugar = QDoubleSpinBox()
        self.sugar.setRange(40, 400)
        self.sugar.setDecimals(1)
        self.sugar.setSuffix(" mg/dL")
        self.sugar.setValue(95.0)

        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Catatan (opsional)")

        inputs = [
            ("Berat", self.weight),
            ("Sistolik", self.sys),
            ("Diastolik", self.dia),
            ("Detak Jantung", self.hr),
            ("Gula Darah", self.sugar),
            ("Catatan", self.notes),
        ]

        row = 0
        for label_text, widget in inputs:
            label = QLabel(label_text)
            label.setStyleSheet("color: #bbb;")
            label.setFont(QFont("Segoe UI", 10))
            grid.addWidget(label, row, 0)
            grid.addWidget(widget, row, 1)
            row += 1

        for w in [self.weight, self.sys, self.dia, self.hr, self.sugar, self.notes]:
            w.setStyleSheet(
                """
                QLineEdit, QDoubleSpinBox, QSpinBox {
                    background: #202020;
                    border: 1px solid #2f2f2f;
                    border-radius: 8px;
                    padding: 8px 10px;
                    color: white;
                }
                QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {
                    border-color: #00BFA5;
                }
            """
            )

        layout.addLayout(grid)

        btn_save = QPushButton("Simpan")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setFixedHeight(42)
        btn_save.setStyleSheet(
            """
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #00E5CC; }
        """
        )
        btn_save.clicked.connect(self.submit_form)
        layout.addWidget(btn_save)

        return card

    def build_chart_card(self):
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background: #1b1b1b;
                border-radius: 16px;
                border: 1px solid #262626;
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        title = QLabel("Tren Berat")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        self.chart_view = self.create_weight_chart()
        layout.addWidget(self.chart_view)

        return card

    def build_table(self):
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background: #1b1b1b;
                border-radius: 16px;
                border: 1px solid #262626;
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        title = QLabel("Riwayat Data Kesehatan")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Waktu", "Berat (kg)", "BP (mmHg)", "HR (bpm)", "Gula (mg/dL)", "Catatan"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet(
            """
            QTableWidget { background: #1b1b1b; border: none; color: #d1d5db; }
            QHeaderView::section {
                background: #202020; color: #e5e7eb; padding: 10px;
                border: none; font-weight: bold; font-size: 12px;
            }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #262626; }
            QTableWidget::item:selected { background: rgba(0,191,165,0.16); color: #fff; }
        """
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)
        return card

    # ------------------------------------------------------------------ Data
    def init_db(self):
        """Pastikan tabel health_entries ada."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS health_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recorded_at TEXT NOT NULL,
                    weight REAL NOT NULL,
                    systolic INTEGER NOT NULL,
                    diastolic INTEGER NOT NULL,
                    heart_rate INTEGER NOT NULL,
                    blood_sugar REAL NOT NULL,
                    notes TEXT
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def load_data(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute(
                "SELECT * FROM health_entries ORDER BY datetime(recorded_at) DESC LIMIT 50"
            ).fetchall()
            self.records = [dict(r) for r in rows]
        finally:
            conn.close()
        self.populate_table()
        self.update_chart()

    def populate_table(self):
        self.table.setRowCount(0)
        for record in self.records:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [
                record["recorded_at"],
                f"{record['weight']:.1f}",
                f"{record['systolic']} / {record['diastolic']}",
                record["heart_rate"],
                f"{record['blood_sugar']:.1f}",
                record.get("notes") or "-",
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

    def create_weight_chart(self):
        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Tren Berat (kg)")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().hide()
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        chart.setTitleFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Entry")
        self.axis_x.setLabelFormat("%d")
        self.axis_x.setLabelsColor(QColor("#888"))
        self.axis_x.setGridLineColor(QColor("#2D2D2D"))

        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("kg")
        self.axis_y.setLabelFormat("%.1f")
        self.axis_y.setLabelsColor(QColor("#888"))
        self.axis_y.setGridLineColor(QColor("#2D2D2D"))

        chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 12px;")
        chart_view.setMinimumHeight(260)
        return chart_view

    def update_chart(self):
        self.series.clear()
        if not self.records:
            return
        weights = []
        for idx, rec in enumerate(reversed(self.records)):  # oldest to newest
            w = float(rec["weight"])
            self.series.append(idx, w)
            weights.append(w)
        if weights:
            min_w = min(weights)
            max_w = max(weights)
            span = max(max_w - min_w, 5)
            if self.axis_x and self.axis_y:
                self.axis_x.setRange(0, len(weights) - 1)
                self.axis_y.setRange(min_w - 1, min_w + span + 1)

    def get_latest_values(self):
        """Return latest record dict or defaults if none."""
        if not self.records:
            return {
                "weight": "-",
                "systolic": "-",
                "diastolic": "-",
                "heart_rate": "-",
                "blood_sugar": "-",
            }
        return self.records[0]

    # ------------------------------------------------------------------ Actions
    def submit_form(self):
        # Basic validation
        if self.sys.value() < self.dia.value():
            QMessageBox.warning(self, "Validasi", "Sistolik harus >= Diastolik.")
            return
        weight = self.weight.value()
        if weight <= 0:
            QMessageBox.warning(self, "Validasi", "Berat harus lebih dari 0.")
            return

        conn = sqlite3.connect(self.db_path)
        try:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            note = self.notes.text().strip() or None
            conn.execute(
                """
                INSERT INTO health_entries
                (recorded_at, weight, systolic, diastolic, heart_rate, blood_sugar, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now_str,
                    weight,
                    self.sys.value(),
                    self.dia.value(),
                    self.hr.value(),
                    self.sugar.value(),
                    note,
                ),
            )
            conn.commit()
            self.load_data()
            self.notes.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data: {e}")
        finally:
            conn.close()


