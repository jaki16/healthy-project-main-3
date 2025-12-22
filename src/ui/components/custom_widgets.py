"""
Custom Reusable Widgets Library
HealthTrack AI Pro - Final Project Version
File: src/ui/components/custom_widgets.py

Author: [Your Name]
Created: December 2024
Description: Collection of reusable UI components for consistent design
"""

from PyQt6.QtWidgets import (QWidget, QFrame, QLabel, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QProgressBar, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPainter, QColor, QPen


class GlassCard(QFrame):
    """
    Glassmorphism style card with blur effect
    
    Features:
    - Semi-transparent background
    - Hover effects
    - Customizable title
    - Flexible content addition
    """
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        
    def setup_ui(self):
        """Setup glass card UI"""
        self.setObjectName("glassCard")
        self.setStyleSheet("""
            #glassCard {
                background-color: rgba(30, 30, 30, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
            }
            #glassCard:hover {
                background-color: rgba(30, 30, 30, 0.85);
                border: 1px solid rgba(0, 191, 165, 0.3);
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #FFFFFF; border: none; background: transparent;")
            self.layout.addWidget(title_label)
    
    def add_widget(self, widget):
        """Add widget to card content"""
        self.layout.addWidget(widget)


class StatCard(QFrame):
    """
    Animated statistics card
    
    Features:
    - Icon display
    - Large value display
    - Subtitle support
    - Click signal emission
    - Hover animations
    """
    
    clicked = pyqtSignal()
    
    def __init__(self, icon, title, value, subtitle="", color="#00BFA5", parent=None):
        super().__init__(parent)
        self.icon = icon
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.color = color
        self.setup_ui()
        
    def setup_ui(self):
        """Setup stat card UI"""
        self.setObjectName("statCard")
        self.setMinimumSize(180, 140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            #statCard {{
                background-color: #1E1E1E;
                border: 2px solid #2D2D2D;
                border-radius: 12px;
                padding: 15px;
            }}
            #statCard:hover {{
                background-color: #252525;
                border: 2px solid {self.color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 32))
        icon_label.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_label)
        
        # Value
        self.value_label = QLabel(str(self.value))
        self.value_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: {self.color}; border: none; background: transparent;")
        layout.addWidget(self.value_label)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 10))
        title_label.setStyleSheet("color: #888; border: none; background: transparent;")
        layout.addWidget(title_label)
        
        # Subtitle
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_label.setFont(QFont("Segoe UI", 8))
            subtitle_label.setStyleSheet("color: #666; border: none; background: transparent;")
            layout.addWidget(subtitle_label)
        
        layout.addStretch()
    
    def update_value(self, new_value):
        """Update card value"""
        self.value = new_value
        self.value_label.setText(str(new_value))
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        self.clicked.emit()
        super().mousePressEvent(event)


class ProgressCard(QFrame):
    """
    Card with progress bar visualization
    
    Features:
    - Title and percentage display
    - Animated progress bar
    - Current/target values
    - Color customization
    """
    
    def __init__(self, title, current, target, unit="", color="#00BFA5", parent=None):
        super().__init__(parent)
        self.title = title
        self.current = current
        self.target = target
        self.unit = unit
        self.color = color
        self.setup_ui()
        
    def setup_ui(self):
        """Setup progress card UI"""
        self.setObjectName("progressCard")
        self.setStyleSheet("""
            #progressCard {
                background-color: #1E1E1E;
                border: 2px solid #2D2D2D;
                border-radius: 12px;
                padding: 20px;
            }
            #progressCard:hover {
                background-color: #252525;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Header with percentage
        header = QHBoxLayout()
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FFF; border: none; background: transparent;")
        header.addWidget(title_label)
        
        header.addStretch()
        
        percentage = int((self.current / self.target) * 100) if self.target > 0 else 0
        percent_label = QLabel(f"{percentage}%")
        percent_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        percent_label.setStyleSheet(f"color: {self.color}; border: none; background: transparent;")
        header.addWidget(percent_label)
        
        layout.addLayout(header)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.target)
        self.progress_bar.setValue(self.current)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #2D2D2D;
                border-radius: 5px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {self.color};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Current/Target values
        values_text = f"{self.current} / {self.target} {self.unit}"
        values_label = QLabel(values_text)
        values_label.setFont(QFont("Segoe UI", 9))
        values_label.setStyleSheet("color: #888; border: none; background: transparent;")
        layout.addWidget(values_label)
    
    def update_progress(self, current):
        """Update progress value"""
        self.current = current
        self.progress_bar.setValue(current)


class SearchBox(QLineEdit):
    """
    Custom search input box with icon
    
    Features:
    - Search icon prefix
    - Focus state styling
    - Placeholder text
    - Rounded corners
    """
    
    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(f"🔍 {placeholder}")
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 11))
        self.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                border: 2px solid #3D3D3D;
                border-radius: 10px;
                padding: 10px 15px;
                color: #FFFFFF;
            }
            QLineEdit:focus {
                border: 2px solid #00BFA5;
                background-color: #252525;
            }
            QLineEdit::placeholder {
                color: #666666;
            }
        """)


class ActionButton(QPushButton):
    """
    Custom styled action button
    
    Features:
    - Icon + text support
    - Color customization
    - Hover effects
    - Auto brightness adjustment
    """
    
    def __init__(self, text, icon="", color="#00BFA5", parent=None):
        super().__init__(f"{icon}  {text}" if icon else text, parent)
        self.color = color
        self.setup_style()
        
    def setup_style(self):
        """Setup button styling"""
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 24px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(self.color, 20)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(self.color, -20)};
            }}
        """)
    
    def adjust_color(self, hex_color, amount):
        """Adjust color brightness"""
        color = QColor(hex_color)
        h, s, l, a = color.getHsl()
        l = max(0, min(255, l + amount))
        color.setHsl(h, s, l, a)
        return color.name()


class InfoBadge(QLabel):
    """
    Circular information badge
    
    Features:
    - Circular shape
    - Centered text
    - Color customization
    - Fixed size
    """
    
    def __init__(self, text, color="#00BFA5", parent=None):
        super().__init__(text, parent)
        self.badge_color = color
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(50, 50)
        self.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: 25px;
                border: 3px solid #1E1E1E;
            }}
        """)


class NotificationCard(QFrame):
    """
    Notification/Alert card with close button
    
    Features:
    - Type-based styling (info, success, warning, error)
    - Icon display
    - Close button
    - Auto-delete on close
    
    Signals:
    - closed: Emitted when notification is closed
    """
    
    closed = pyqtSignal()
    
    def __init__(self, title, message, type="info", parent=None):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.type = type
        self.setup_ui()
        
    def setup_ui(self):
        """Setup notification UI"""
        colors = {
            "info": "#2196F3",
            "success": "#00BFA5",
            "warning": "#FF9800",
            "error": "#FF5252"
        }
        
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        color = colors.get(self.type, colors["info"])
        icon = icons.get(self.type, icons["info"])
        
        self.setObjectName("notificationCard")
        self.setStyleSheet(f"""
            #notificationCard {{
                background-color: #1E1E1E;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(15)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        icon_label.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_label)
        
        # Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)
        
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {color}; border: none; background: transparent;")
        content_layout.addWidget(title_label)
        
        message_label = QLabel(self.message)
        message_label.setFont(QFont("Segoe UI", 10))
        message_label.setStyleSheet("color: #CCC; border: none; background: transparent;")
        message_label.setWordWrap(True)
        content_layout.addWidget(message_label)
        
        layout.addLayout(content_layout, 1)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: #FFF;
            }
        """)
        close_btn.clicked.connect(self.close_notification)
        layout.addWidget(close_btn)
    
    def close_notification(self):
        """Close and delete notification"""
        self.closed.emit()
        self.deleteLater()


class LoadingSpinner(QWidget):
    """
    Animated loading spinner
    
    Features:
    - Rotating arc animation
    - Color customization
    - Size customization
    - Start/stop control
    """
    
    def __init__(self, size=50, color="#00BFA5", parent=None):
        super().__init__(parent)
        self.size = size
        self.color = QColor(color)
        self.angle = 0
        self.setFixedSize(size, size)
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)
    
    def rotate(self):
        """Rotate spinner angle"""
        self.angle = (self.angle + 10) % 360
        self.update()
    
    def paintEvent(self, event):
        """Paint spinner arc"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect().adjusted(5, 5, -5, -5)
        pen = QPen(self.color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        painter.drawArc(rect, self.angle * 16, 120 * 16)
    
    def stop(self):
        """Stop spinner animation"""
        self.timer.stop()


class Separator(QFrame):
    """
    Horizontal separator line
    
    Features:
    - Simple horizontal line
    - Semi-transparent styling
    - 1px height
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                max-height: 1px;
            }
        """)