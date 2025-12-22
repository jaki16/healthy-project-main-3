"""
Activity Tracker Page

Tujuan:
- Desain konsisten dengan Dashboard & Nutrition (dark theme, padding 30px)
- Fokus pada keterbacaan data dan kemudahan logging aktivitas
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QScrollArea, QDialog,
    QFormLayout, QLineEdit, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtCharts import (
    QChart, QChartView, QPieSeries,
    QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
)

class LogActivityDialog(QDialog):
    """Dialog untuk menambah aktivitas baru"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log New Activity")
        self.setFixedWidth(480)
        self.init_ui()

    def init_ui(self):
        # Konsisten dengan dialog Nutrition (dark, clean)
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #2D2D2D;
                color: white;
                border: 2px solid #3D3D3D;
                border-radius: 8px;
                padding: 8px 10px;
                min-height: 32px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #00BFA5;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = QLabel("Add Activity")
        header.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: #00BFA5; margin-bottom: 10px;")
        layout.addWidget(header)

        form = QFormLayout()
        form.setSpacing(18)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.type_input = QComboBox()
        self.type_input.addItems(["Running", "Cycling", "Gym", "Walking", "Swimming", "Yoga", "Other"])
        
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 500)
        self.duration_input.setSuffix(" min")
        self.duration_input.setValue(30)
        
        self.dist_input = QLineEdit()
        self.dist_input.setPlaceholderText("e.g. 5.0")
        
        self.calories_input = QSpinBox()
        self.calories_input.setRange(1, 3000)
        self.calories_input.setSuffix(" kcal")
        self.calories_input.setValue(200)
        
        self.hr_input = QSpinBox()
        self.hr_input.setRange(0, 220)
        self.hr_input.setSuffix(" bpm")
        self.hr_input.setValue(0)
        
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("How was your session?")

        form.addRow("Activity Type:", self.type_input)
        form.addRow("Duration:", self.duration_input)
        form.addRow("Distance (km):", self.dist_input)
        form.addRow("Calories:", self.calories_input)
        form.addRow("Heart Rate:", self.hr_input)
        form.addRow("Notes:", self.note_input)
        
        layout.addLayout(form)
        layout.addSpacing(25)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedHeight(40)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #3D3D3D;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 22px;
            }
            QPushButton:hover {
                background-color: #4D4D4D;
            }
        """)
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QPushButton("Save Activity")
        btn_save.setFixedHeight(40)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 24px;
            }
            QPushButton:hover {
                background-color: #00E5CC;
            }
        """)
        btn_save.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

class ActivityPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Main layout dengan margin seperti Dashboard/Nutrition
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Scroll Area Setup
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Content Container
        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)

        # 1. HEADER
        header = self.create_header()
        content_layout.addWidget(header)

        # 2. STATS + SUMMARY (row)
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setSpacing(20)

        stats = self.create_stats_section()
        summary = self.create_summary_section()
        top_layout.addWidget(stats, 2)
        top_layout.addWidget(summary, 1)

        content_layout.addWidget(top_row)

        # 3. CHARTS SECTION
        charts = self.create_charts_section()
        content_layout.addWidget(charts)

        # 4. ACTIVITY TABLE
        table = self.create_table_section()
        content_layout.addWidget(table)

        content_layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def create_header(self):
        """Create header section"""
        header = QFrame()
        header.setObjectName("activityHeader")
        header.setStyleSheet("""
            #activityHeader {
                background-color: transparent;
                border: none;
            }
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title section (selaras dengan Dashboard/Nutrition)
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)

        title = QLabel("Activity Tracker")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")

        subtitle = QLabel("Monitor your daily movement, calories, and performance")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #888; background: transparent;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        # Button
        btn_log = QPushButton("➕ Log Activity")
        btn_log.setFixedSize(160, 48)
        btn_log.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_log.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        btn_log.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #00E5CC;
            }
        """)
        btn_log.clicked.connect(self.open_log_dialog)

        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addWidget(btn_log)

        return header

    def create_stats_section(self):
        """Create stats cards section"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(15)
        
        stats = [
            ("🔥", "Total Burned", "1,240", "kcal", "#ef4444"),
            ("⏱️", "Active Time", "85", "min", "#10b981"),
            ("🏃", "Distance", "12.4", "km", "#3b82f6"),
            ("⚡", "Streak", "12", "days", "#f59e0b")
        ]
        
        for icon, title, value, unit, color in stats:
            card = self.create_stat_card(icon, title, value, unit, color)
            layout.addWidget(card)
        
        return container

    def create_stat_card(self, icon, title, value, unit, color):
        """Create individual stat card"""
        card = QFrame()
        card.setObjectName("activityStatCard")
        card.setStyleSheet(f"""
            #activityStatCard {{
                background-color: #1E1E1E;
                border-radius: 15px;
                border: 2px solid #2D2D2D;
            }}
            #activityStatCard:hover {{
                border-color: {color};
                background-color: #252525;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10))
        title_label.setStyleSheet("color: #888; background: transparent;")
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 22))
        icon_label.setStyleSheet("background: transparent;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(icon_label)
        
        # Value
        value_layout = QHBoxLayout()
        value_layout.setSpacing(6)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color}; background: transparent;")
        
        unit_label = QLabel(unit)
        unit_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        unit_label.setStyleSheet("color: #666; background: transparent; margin-top: 6px;")
        
        value_layout.addWidget(value_label)
        value_layout.addWidget(unit_label)
        value_layout.addStretch()
        
        layout.addLayout(header_layout)
        layout.addLayout(value_layout)
        
        return card

    def create_charts_section(self):
        """Create charts section with real charts"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(20)

        # Left: Activity distribution pie chart
        dist_chart = self._create_activity_distribution_chart()
        layout.addWidget(dist_chart, 1)

        # Right: Weekly performance bar chart
        weekly_chart = self._create_weekly_performance_chart()
        layout.addWidget(weekly_chart, 1)

        return container

    def _create_activity_distribution_chart(self):
        """Pie chart: distribution of activity types"""
        series = QPieSeries()
        # Sample distribution data (can dikaitkan ke data nyata nanti)
        series.append("Running", 30)
        series.append("Cycling", 20)
        series.append("Gym", 25)
        series.append("Walking", 15)
        series.append("Other", 10)

        colors = [
            QColor("#00BFA5"),
            QColor("#FF6B6B"),
            QColor("#FFD54F"),
            QColor("#42A5F5"),
            QColor("#7C4DFF"),
        ]
        for i, slice_ in enumerate(series.slices()):
            slice_.setLabelVisible(True)
            slice_.setLabelColor(QColor("white"))
            slice_.setColor(colors[i % len(colors)])
            slice_.setLabelFont(QFont("Segoe UI", 9))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Activity Distribution")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart.legend().setFont(QFont("Segoe UI", 9))
        chart.legend().setLabelColor(QColor("white"))
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        chart.setTitleFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")
        chart_view.setMinimumHeight(280)

        return chart_view

    def _create_weekly_performance_chart(self):
        """Bar chart: weekly total duration (minutes)"""
        bar_set = QBarSet("Minutes")
        # Sample weekly durations (Mon-Sun)
        bar_set.append([45, 30, 60, 50, 40, 35, 20])
        bar_set.setColor(QColor("#00BFA5"))

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Weekly Performance")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().hide()
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        chart.setTitleFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        categories = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#888"))

        axis_y = QValueAxis()
        axis_y.setRange(0, 80)
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(QColor("#888"))
        axis_y.setGridLineColor(QColor("#2D2D2D"))

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")
        chart_view.setMinimumHeight(280)

        return chart_view

    def create_table_section(self):
        """Create activity history table"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: #2d2d2d;
                border-radius: 16px;
                border: 2px solid #3d3d3d;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        title = QLabel("📋 Recent Activity History")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #FFFFFF; background: transparent;")
        layout.addWidget(title)
        
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["TIME", "ACTIVITY", "DURATION", "DISTANCE", "CALORIES", "HR"])
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setMinimumHeight(400)
        self.table.setStyleSheet("""
            QTableWidget { 
                background: #2d2d2d; 
                border: none; 
                color: #CCCCCC; 
                font-size: 13px;
            }
            QHeaderView::section { 
                background: #252525; 
                color: #FFFFFF; 
                padding: 14px; 
                border: none; 
                font-weight: bold; 
                font-size: 12px;
                border-bottom: 2px solid #3d3d3d;
            }
            QTableWidget::item { 
                border-bottom: 1px solid #3d3d3d; 
                padding: 16px; 
            }
            QTableWidget::item:selected { 
                background-color: rgba(0, 191, 165, 0.2); 
                color: #FFFFFF; 
            }
            QTableWidget::item:hover {
                background-color: #333333;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # Add sample data
        sample_data = [
            ("08:30", "Running", "45 min", "5.2 km", "450 kcal", "145 bpm"),
            ("12:15", "Walking", "20 min", "1.8 km", "95 kcal", "98 bpm"),
            ("17:00", "Gym", "60 min", "-", "320 kcal", "128 bpm"),
            ("19:15", "Cycling", "30 min", "8.5 km", "280 kcal", "132 bpm"),
            ("06:00", "Yoga", "40 min", "-", "120 kcal", "85 bpm"),
            ("20:30", "Swimming", "35 min", "1.2 km", "310 kcal", "118 bpm"),
        ]
        
        for time, activity, duration, distance, calories, hr in sample_data:
            self.add_table_row(time, activity, duration, distance, calories, hr)
        
        return container

    def create_summary_section(self):
        """Create weekly summary"""
        container = QFrame()
        container.setFixedHeight(180)
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("🎯 This Week's Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        
        stats_text = QLabel("✓ 6 workouts completed\n✓ 4.5 hours active time\n✓ 2,450 calories burned\n✓ 32.5 km distance covered")
        stats_text.setFont(QFont("Segoe UI", 14))
        stats_text.setStyleSheet("color: rgba(255, 255, 255, 0.95); background: transparent; line-height: 1.8;")
        
        layout.addWidget(title)
        layout.addSpacing(15)
        layout.addWidget(stats_text)
        layout.addStretch()
        
        return container

    def add_table_row(self, time, activity, duration, distance, calories, hr):
        """Add row to activity table"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        items = [time, activity, duration, distance, calories, hr]
        for col, value in enumerate(items):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, col, item)

    def open_log_dialog(self):
        """Open activity logging dialog"""
        dialog = LogActivityDialog(self)
        if dialog.exec():
            from datetime import datetime
            now = datetime.now().strftime("%H:%M")
            
            act_type = dialog.type_input.currentText()
            dur = f"{dialog.duration_input.value()} min"
            dist = f"{dialog.dist_input.text()} km" if dialog.dist_input.text() else "-"
            cal = f"{dialog.calories_input.value()} kcal"
            hr = f"{dialog.hr_input.value()} bpm" if dialog.hr_input.value() > 0 else "-"
            
            # Insert to top of table
            self.table.insertRow(0)
            items = [now, act_type, dur, dist, cal, hr]
            for col, value in enumerate(items):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, col, item)