"""
Dashboard Page - Health Metrics Overview
HealthTrack AI Pro - Final Project Version
File: src/ui/pages/dashboard.py

Author: [Your Name]
Created: December 2024
Description: Main dashboard displaying real-time health metrics,
             activity charts, and weekly progress visualization
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QProgressBar, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtCharts import (QChart, QChartView, QLineSeries, QPieSeries, 
                           QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis)
import random


class HealthMetricCard(QFrame):
    """
    Individual health metric card with progress visualization
    
    Features:
    - Icon and title display
    - Large value display with color coding
    - Progress bar with target tracking
    - Hover effects
    - Real-time value updates
    """
    
    def __init__(self, icon: str, title: str, value: str, unit: str, 
                 progress: int, target: str, color: str = "#00BFA5"):
        super().__init__()
        self.icon = icon
        self.title = title
        self.value = value
        self.unit = unit
        self.progress_value = progress
        self.target = target
        self.color = color
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup card UI components"""
        self.setObjectName("metricCard")
        self.setStyleSheet(f"""
            #metricCard {{
                background-color: #1E1E1E;
                border-radius: 15px;
                border: 2px solid #2D2D2D;
                padding: 20px;
                min-width: 200px;
                min-height: 180px;
            }}
            #metricCard:hover {{
                border-color: {self.color};
                background-color: #252525;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Header: Icon and Title
        header = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 28))
        header.addWidget(icon_label)
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 10))
        title_label.setStyleSheet("color: #888;")
        header.addWidget(title_label, 1)
        
        layout.addLayout(header)
        
        # Value Display
        self.value_label = QLabel(self.value)
        self.value_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: {self.color};")
        layout.addWidget(self.value_label)
        
        # Unit Label
        unit_label = QLabel(self.unit)
        unit_label.setFont(QFont("Segoe UI", 9))
        unit_label.setStyleSheet("color: #666;")
        layout.addWidget(unit_label)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(self.progress_value)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #2D2D2D;
                border-radius: 4px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {self.color};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Target Label
        target_label = QLabel(f"Target: {self.target}")
        target_label.setFont(QFont("Segoe UI", 8))
        target_label.setStyleSheet("color: #555;")
        layout.addWidget(target_label)
        
        layout.addStretch()
    
    def update_value(self, new_value: str, new_progress: int):
        """
        Update card value and progress
        
        Args:
            new_value: New value to display
            new_progress: New progress percentage (0-100)
        """
        self.value_label.setText(new_value)
        self.progress_bar.setValue(new_progress)


class DashboardPage(QWidget):
    """
    Main dashboard page displaying health overview
    
    Features:
    - Real-time health metric cards (Steps, Calories, Heart Rate, Sleep)
    - Live heart rate chart with color coding
    - Activity distribution pie chart
    - Weekly progress bar chart
    - Auto-updating data simulation
    
    Data Updates:
    - Steps: Every 3 seconds
    - Heart Rate: Every 1 second
    - Charts: Real-time based on data
    """
    
    def __init__(self):
        super().__init__()
        
        # Data variables
        self.steps = 5420
        self.heart_rate = 72
        self.heart_rate_data = [72] * 20  # Last 20 readings
        
        self.setup_ui()
        self.setup_timers()
        
    def setup_ui(self):
        """Setup dashboard UI components"""
        # Gunakan scroll area agar konten tidak terpotong di layar kecil
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #121212;
                border: none;
            }
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
            QScrollBar::handle:vertical:hover {
                background-color: #00BFA5;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        container = QWidget()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header Section
        header_layout = QHBoxLayout()
        
        # Title and Date
        title_layout = QVBoxLayout()
        
        title = QLabel("Dashboard")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title_layout.addWidget(title)
        
        date_label = QLabel(QDateTime.currentDateTime().toString("dddd, MMMM d, yyyy"))
        date_label.setFont(QFont("Segoe UI", 11))
        date_label.setStyleSheet("color: #888;")
        title_layout.addWidget(date_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Health Score Badge
        score_widget = self.create_health_score_badge()
        header_layout.addWidget(score_widget)
        
        main_layout.addLayout(header_layout)
        
        # Metric Cards Row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        self.steps_card = HealthMetricCard(
            "👣", "Steps", "5,420", "steps today",
            54, "10,000 steps", "#00BFA5"
        )
        cards_layout.addWidget(self.steps_card)
        
        self.calories_card = HealthMetricCard(
            "🔥", "Calories", "217", "kcal burned",
            22, "1,000 kcal", "#FF6B6B"
        )
        cards_layout.addWidget(self.calories_card)
        
        self.heart_card = HealthMetricCard(
            "❤️", "Heart Rate", "72", "bpm (Live)",
            72, "60-100 bpm", "#FF4081"
        )
        cards_layout.addWidget(self.heart_card)
        
        self.sleep_card = HealthMetricCard(
            "😴", "Sleep", "7.5", "hours",
            94, "8 hours", "#9C27B0"
        )
        cards_layout.addWidget(self.sleep_card)
        
        main_layout.addLayout(cards_layout)
        
        # Charts Section
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Heart Rate Chart (larger, left)
        heart_chart_widget = self.create_heart_rate_chart()
        charts_layout.addWidget(heart_chart_widget, 2)
        
        # Activity Pie Chart (smaller, right)
        activity_chart_widget = self.create_activity_pie_chart()
        charts_layout.addWidget(activity_chart_widget, 1)
        
        main_layout.addLayout(charts_layout)
        
        # Weekly Progress Chart
        weekly_chart_widget = self.create_weekly_chart()
        main_layout.addWidget(weekly_chart_widget)
        
        main_layout.addStretch()
        root_layout.addWidget(scroll)
    
    def create_health_score_badge(self):
        """Create circular health score badge"""
        badge = QFrame()
        badge.setFixedSize(100, 100)
        badge.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border: 3px solid #00BFA5;
                border-radius: 50px;
            }
        """)
        
        layout = QVBoxLayout(badge)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        score_label = QLabel("85")
        score_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        score_label.setStyleSheet("color: #00BFA5; border: none;")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(score_label)
        
        text_label = QLabel("Health\nScore")
        text_label.setFont(QFont("Segoe UI", 8))
        text_label.setStyleSheet("color: #888; border: none;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label)
        
        return badge
    
    def create_heart_rate_chart(self):
        """Create real-time heart rate line chart"""
        # Create series
        self.heart_series = QLineSeries()
        for i, hr in enumerate(self.heart_rate_data):
            self.heart_series.append(i, hr)
        
        # Create chart
        chart = QChart()
        chart.addSeries(self.heart_series)
        chart.setTitle("Real-Time Heart Rate")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().hide()
        
        # Style chart
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        chart.setTitleFont(title_font)
        
        # Configure axes
        axis_x = QValueAxis()
        axis_x.setRange(0, 19)
        axis_x.setLabelsVisible(False)
        axis_x.setGridLineVisible(False)
        axis_x.setLabelsColor(QColor("#888"))
        
        axis_y = QValueAxis()
        axis_y.setRange(50, 110)
        axis_y.setLabelFormat("%d")
        axis_y.setTickCount(7)
        axis_y.setLabelsColor(QColor("#888"))
        axis_y.setGridLineColor(QColor("#2D2D2D"))
        
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        self.heart_series.attachAxis(axis_x)
        self.heart_series.attachAxis(axis_y)
        
        # Style series line
        pen = self.heart_series.pen()
        pen.setWidth(3)
        pen.setColor(QColor("#FF4081"))
        self.heart_series.setPen(pen)
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")
        chart_view.setMinimumHeight(300)
        
        return chart_view
    
    def create_activity_pie_chart(self):
        """Create activity distribution pie chart"""
        # Create series
        series = QPieSeries()
        series.append("Walking", 45)
        series.append("Running", 25)
        series.append("Cycling", 20)
        series.append("Other", 10)
        
        # Style slices
        colors = ["#00BFA5", "#FF4081", "#FFD54F", "#7C4DFF"]
        for i, slice in enumerate(series.slices()):
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("white"))
            slice.setColor(QColor(colors[i]))
            slice.setLabelFont(QFont("Segoe UI", 9))
        
        # Create chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Activity Distribution")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart.legend().setFont(QFont("Segoe UI", 9))
        chart.legend().setLabelColor(QColor("white"))
        
        # Style chart
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        chart.setTitleFont(title_font)
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")
        chart_view.setMinimumHeight(300)
        
        return chart_view
    
    def create_weekly_chart(self):
        """Create weekly steps bar chart"""
        # Create bar set
        bar_set = QBarSet("Steps")
        bar_set.append([8500, 9200, 7800, 10500, 9800, 5420, 0])
        bar_set.setColor(QColor("#00BFA5"))
        
        # Create series
        series = QBarSeries()
        series.append(bar_set)
        
        # Create chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Weekly Steps Progress")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().hide()
        
        # Style chart
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        chart.setTitleFont(title_font)
        
        # Configure axes
        categories = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#888"))
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 12000)
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(QColor("#888"))
        axis_y.setGridLineColor(QColor("#2D2D2D"))
        
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        
        # Create chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")
        chart_view.setFixedHeight(250)
        
        return chart_view
    
    def setup_timers(self):
        """Setup auto-update timers for real-time data"""
        # Update steps every 3 seconds
        self.steps_timer = QTimer()
        self.steps_timer.timeout.connect(self.update_steps)
        self.steps_timer.start(3000)
        
        # Update heart rate every second
        self.heart_timer = QTimer()
        self.heart_timer.timeout.connect(self.update_heart_rate)
        self.heart_timer.start(1000)
    
    def update_steps(self):
        """Update steps count with random increment"""
        self.steps += random.randint(5, 50)
        steps_str = f"{self.steps:,}"
        progress = min(int((self.steps / 10000) * 100), 100)
        
        self.steps_card.update_value(steps_str, progress)
        
        # Update calories (approximately 0.04 kcal per step)
        calories = int(self.steps * 0.04)
        calories_progress = min(int((calories / 1000) * 100), 100)
        self.calories_card.update_value(str(calories), calories_progress)
    
    def update_heart_rate(self):
        """Update heart rate with simulated variation"""
        # Simulate heart rate variation (60-100 bpm)
        change = random.randint(-3, 3)
        self.heart_rate = max(60, min(100, self.heart_rate + change))
        
        # Update card
        progress = int(((self.heart_rate - 60) / 40) * 100)
        self.heart_card.update_value(str(self.heart_rate), progress)
        
        # Update chart data
        self.heart_rate_data.append(self.heart_rate)
        if len(self.heart_rate_data) > 20:
            self.heart_rate_data.pop(0)
        
        # Update chart series
        self.heart_series.clear()
        for i, hr in enumerate(self.heart_rate_data):
            self.heart_series.append(i, hr)
        
        # Dynamic color based on heart rate
        if self.heart_rate > 85:
            color = QColor("#FF4081")  # Pink - high
        elif self.heart_rate < 65:
            color = QColor("#64B5F6")  # Blue - low
        else:
            color = QColor("#00BFA5")  # Green - normal
        
        pen = self.heart_series.pen()
        pen.setColor(color)
        self.heart_series.setPen(pen)