"""
Activity Logging Dialog
Add or edit activity/exercise entries
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QComboBox, QTextEdit,
                             QSpinBox, QDoubleSpinBox, QDateTimeEdit,
                             QFrame, QGridLayout, QScrollArea, QWidget, QCheckBox)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont
from datetime import datetime

class ActivityLoggingDialog(QDialog):
    """Dialog for adding or editing activity entries"""
    activity_logged = pyqtSignal(dict)
    
    def __init__(self, parent=None, activity_data=None):
        super().__init__(parent)
        self.activity_data = activity_data
        self.init_ui()
        
        if activity_data:
            self.load_activity_data(activity_data)
            
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Log Activity")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("🏃 Log Your Activity")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(title)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        
        # Date & Time
        datetime_section = self.create_datetime_section()
        form_layout.addWidget(datetime_section)
        
        # Activity Type
        type_section = self.create_activity_type_section()
        form_layout.addWidget(type_section)
        
        # Duration & Distance
        metrics_section = self.create_metrics_section()
        form_layout.addWidget(metrics_section)
        
        # Heart Rate
        hr_section = self.create_heart_rate_section()
        form_layout.addWidget(hr_section)
        
        # Calories
        calories_section = self.create_calories_section()
        form_layout.addWidget(calories_section)
        
        # Notes
        notes_section = self.create_notes_section()
        form_layout.addWidget(notes_section)
        
        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)
        
        # Buttons
        button_layout = self.create_button_section()
        main_layout.addLayout(button_layout)
        
        # Styling
        self.setStyleSheet("""
            QDialog {
                background: #f8f9fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, 
            QDateTimeEdit, QTextEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
            QDoubleSpinBox:focus, QDateTimeEdit:focus, QTextEdit:focus {
                border: 2px solid #FF6B6B;
            }
        """)
        
    def create_datetime_section(self):
        """Create date & time selection"""
        container = self.create_section_container("📅 When did you exercise?")
        layout = container.layout()
        
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd MMM yyyy - hh:mm AP")
        
        layout.addWidget(self.datetime_edit)
        
        return container
        
    def create_activity_type_section(self):
        """Create activity type selection"""
        container = self.create_section_container("🏃 Activity Type")
        layout = container.layout()
        
        self.activity_type = QComboBox()
        self.activity_type.addItems([
            "Walking",
            "Running", 
            "Cycling",
            "Swimming",
            "Gym / Weights",
            "Yoga",
            "Pilates",
            "Dancing",
            "Sports",
            "Hiking",
            "Other"
        ])
        
        # Custom activity input
        custom_layout = QHBoxLayout()
        self.custom_checkbox = QCheckBox("Custom activity:")
        self.custom_activity = QLineEdit()
        self.custom_activity.setPlaceholderText("Enter custom activity name")
        self.custom_activity.setEnabled(False)
        
        self.custom_checkbox.toggled.connect(self.toggle_custom_activity)
        
        custom_layout.addWidget(self.custom_checkbox)
        custom_layout.addWidget(self.custom_activity)
        
        layout.addWidget(self.activity_type)
        layout.addLayout(custom_layout)
        
        return container
        
    def create_metrics_section(self):
        """Create duration & distance inputs"""
        container = self.create_section_container("⏱️ Duration & Distance")
        layout = container.layout()
        
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Duration
        duration_label = QLabel("Duration *")
        duration_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.duration = QSpinBox()
        self.duration.setRange(1, 999)
        self.duration.setSuffix(" minutes")
        self.duration.setValue(30)
        
        # Distance (optional)
        distance_label = QLabel("Distance (optional)")
        distance_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.distance = QDoubleSpinBox()
        self.distance.setRange(0, 999.9)
        self.distance.setSuffix(" km")
        self.distance.setDecimals(1)
        self.distance.setValue(0)
        
        grid.addWidget(duration_label, 0, 0)
        grid.addWidget(self.duration, 0, 1)
        grid.addWidget(distance_label, 1, 0)
        grid.addWidget(self.distance, 1, 1)
        
        layout.addLayout(grid)
        
        return container
        
    def create_heart_rate_section(self):
        """Create heart rate inputs"""
        container = self.create_section_container("❤️ Heart Rate (optional)")
        layout = container.layout()
        
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Average HR
        avg_hr_label = QLabel("Average Heart Rate")
        avg_hr_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.avg_heart_rate = QSpinBox()
        self.avg_heart_rate.setRange(0, 220)
        self.avg_heart_rate.setSuffix(" bpm")
        self.avg_heart_rate.setValue(0)
        
        # Max HR
        max_hr_label = QLabel("Max Heart Rate")
        max_hr_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.max_heart_rate = QSpinBox()
        self.max_heart_rate.setRange(0, 220)
        self.max_heart_rate.setSuffix(" bpm")
        self.max_heart_rate.setValue(0)
        
        grid.addWidget(avg_hr_label, 0, 0)
        grid.addWidget(self.avg_heart_rate, 0, 1)
        grid.addWidget(max_hr_label, 1, 0)
        grid.addWidget(self.max_heart_rate, 1, 1)
        
        layout.addLayout(grid)
        
        return container
        
    def create_calories_section(self):
        """Create calories input"""
        container = self.create_section_container("🔥 Calories Burned")
        layout = container.layout()
        
        cal_layout = QHBoxLayout()
        
        self.calories = QSpinBox()
        self.calories.setRange(0, 9999)
        self.calories.setSuffix(" kcal")
        self.calories.setValue(0)
        
        # Auto-calculate button
        calc_btn = QPushButton("🧮 Auto Calculate")
        calc_btn.setStyleSheet("""
            QPushButton {
                background: #e3f2fd;
                color: #1976d2;
                border: 2px solid #90caf9;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #bbdefb;
            }
        """)
        calc_btn.clicked.connect(self.auto_calculate_calories)
        
        cal_layout.addWidget(self.calories, 2)
        cal_layout.addWidget(calc_btn, 1)
        
        layout.addLayout(cal_layout)
        
        # Info label
        info = QLabel("💡 Tip: Leave at 0 to auto-calculate based on duration and activity type")
        info.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(info)
        
        return container
        
    def create_notes_section(self):
        """Create notes section"""
        container = self.create_section_container("📝 Notes (Optional)")
        layout = container.layout()
        
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("How did you feel? Any achievements or observations?")
        self.notes.setMaximumHeight(100)
        
        layout.addWidget(self.notes)
        
        return container
        
    def create_button_section(self):
        """Create dialog buttons"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # Cancel
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #f0f0f0;
                color: #7f8c8d;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        # Save
        save_btn = QPushButton("💾 Save Activity")
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF6B6B, stop:1 #ee5a52);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ee5a52, stop:1 #dc4f47);
            }
        """)
        save_btn.clicked.connect(self.save_activity)
        
        layout.addStretch()
        layout.addWidget(cancel_btn)
        layout.addWidget(save_btn)
        
        return layout
        
    def create_section_container(self, title):
        """Create a styled section container"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; background: transparent;")
        layout.addWidget(title_label)
        
        return container
        
    def toggle_custom_activity(self, checked):
        """Toggle custom activity input"""
        self.custom_activity.setEnabled(checked)
        self.activity_type.setEnabled(not checked)
        
    def auto_calculate_calories(self):
        """Auto-calculate calories based on activity and duration"""
        duration = self.duration.value()
        
        # MET values (Metabolic Equivalent of Task)
        met_values = {
            "Walking": 3.5,
            "Running": 8.0,
            "Cycling": 6.0,
            "Swimming": 7.0,
            "Gym / Weights": 5.0,
            "Yoga": 2.5,
            "Pilates": 3.0,
            "Dancing": 4.5,
            "Sports": 6.0,
            "Hiking": 6.5,
            "Other": 4.0
        }
        
        activity = self.activity_type.currentText()
        met = met_values.get(activity, 4.0)
        
        # Assume average weight of 70kg
        # Calories = MET × weight(kg) × duration(hours)
        calories = int(met * 70 * (duration / 60))
        
        self.calories.setValue(calories)
        
    def save_activity(self):
        """Save activity entry"""
        # Get activity name
        if self.custom_checkbox.isChecked():
            activity_name = self.custom_activity.text()
            if not activity_name.strip():
                print("Error: Custom activity name required")
                return
        else:
            activity_name = self.activity_type.currentText()
        
        # Auto-calculate calories if not set
        if self.calories.value() == 0:
            self.auto_calculate_calories()
        
        # Collect data
        activity_data = {
            'datetime': self.datetime_edit.dateTime().toPyDateTime(),
            'activity_type': activity_name,
            'duration_minutes': self.duration.value(),
            'distance_km': self.distance.value() if self.distance.value() > 0 else None,
            'calories_burned': self.calories.value(),
            'avg_heart_rate': self.avg_heart_rate.value() if self.avg_heart_rate.value() > 0 else None,
            'max_heart_rate': self.max_heart_rate.value() if self.max_heart_rate.value() > 0 else None,
            'notes': self.notes.toPlainText()
        }
        
        # Emit signal
        self.activity_logged.emit(activity_data)
        
        # TODO: Save to database
        print("Activity logged:", activity_data)
        
        self.accept()
        
    def load_activity_data(self, data):
        """Load existing activity data for editing"""
        if 'datetime' in data:
            self.datetime_edit.setDateTime(data['datetime'])
        if 'activity_type' in data:
            index = self.activity_type.findText(data['activity_type'])
            if index >= 0:
                self.activity_type.setCurrentIndex(index)
        if 'duration_minutes' in data:
            self.duration.setValue(data['duration_minutes'])
        if 'distance_km' in data and data['distance_km']:
            self.distance.setValue(data['distance_km'])
        if 'calories_burned' in data:
            self.calories.setValue(data['calories_burned'])
        if 'avg_heart_rate' in data and data['avg_heart_rate']:
            self.avg_heart_rate.setValue(data['avg_heart_rate'])
        if 'max_heart_rate' in data and data['max_heart_rate']:
            self.max_heart_rate.setValue(data['max_heart_rate'])
        if 'notes' in data:
            self.notes.setPlainText(data['notes'])