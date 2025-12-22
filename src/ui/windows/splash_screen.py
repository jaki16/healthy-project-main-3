"""
Splash Screen with Loading Animation
HealthTrack AI Pro - Final Project Version
File: src/ui/windows/splash_screen.py

Author: [Your Name]
Created: December 2024
Description: Animated splash screen displayed during application startup
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont


class SplashScreen(QWidget):
    """
    Animated splash screen with loading progress
    
    Features:
    - Frameless window design
    - Smooth fade in/out animations
    - Progressive loading messages
    - Auto-close when loading complete
    
    Signals:
    - finished: Emitted when splash screen completes
    """
    
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.progress = 0
        self.setup_ui()
        self.start_loading()
        
    def setup_ui(self):
        """Setup splash screen UI components"""
        # Window configuration
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(600, 400)
        
        # Center window on screen
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        # Main container
        container = QWidget(self)
        container.setGeometry(0, 0, 600, 400)
        container.setStyleSheet("""
            QWidget {
                background-color: #121212;
                border-radius: 20px;
                border: 2px solid #2D2D2D;
            }            
        """)
        
        # Layout
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Animated loader (dot wave) - lebih modern dibanding ikon hati statis
        self.loader_label = QLabel("●   ●   ●")
        self.loader_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.loader_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loader_label.setStyleSheet("""
            color: #00BFA5;
            border: none;
            background: transparent;
            padding: 10px 8px;
        """)
        self.loader_label.setMinimumHeight(80)
        layout.addWidget(self.loader_label)
        
        # Application name
        app_name = QLabel("HealthTrack AI Pro")
        app_name.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setStyleSheet("""
            color: #00BFA5;
            border: none;
            background: transparent;
        """)
        layout.addWidget(app_name)
        
        # Subtitle / tagline
        subtitle = QLabel("Smart Health & Activity Dashboard")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            color: #888888;
            border: none;
            background: transparent;
        """)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Loading message
        self.loading_label = QLabel("Initializing application...")
        self.loading_label.setFont(QFont("Segoe UI", 11))
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("""
            color: #CCCCCC;
            border: none;
            background: transparent;
        """)
        layout.addWidget(self.loading_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2D2D2D;
                border-radius: 3px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00BFA5,
                    stop:1 #00E5CC
                );
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Version info
        version = QLabel("Version 1.0.0")
        version.setFont(QFont("Segoe UI", 9))
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("""
            color: #666666;
            border: none;
            background: transparent;
            margin-top: 10px;
        """)
        layout.addWidget(version)
        
        # Loader animation state
        self.loader_states = [
            "●   ○   ○",
            "○   ●   ○",
            "○   ○   ●",
        ]
        self.loader_index = 0

        # Timer untuk animasi loader
        self.loader_timer = QTimer(self)
        self.loader_timer.timeout.connect(self.animate_loader)
        self.loader_timer.start(220)

        # Start fade in animation
        self.fade_in()
    
    def fade_in(self):
        """Animate splash screen fade in"""
        self.setWindowOpacity(0.0)
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()
    
    def start_loading(self):
        """Start simulated loading process"""
        # Loading messages sequence
        self.loading_messages = [
            "Initializing application...",
            "Loading UI components...",
            "Setting up database...",
            "Connecting services...",
            "Loading AI models...",
            "Preparing dashboard...",
            "Almost ready...",
            "Starting application..."
        ]
        self.message_index = 0
        
        # Progress timer (updates every 200ms)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(200)
    
    def update_progress(self):
        """Update loading progress and messages"""
        self.progress += 5
        
        # Check if loading complete
        if self.progress > 100:
            self.progress = 100
            self.timer.stop()
            self.fade_out()
            return
        
        # Update progress bar
        self.progress_bar.setValue(self.progress)
        
        # Update loading message
        msg_index = int((self.progress / 100) * len(self.loading_messages))
        if msg_index < len(self.loading_messages):
            self.loading_label.setText(self.loading_messages[msg_index])
    
    def fade_out(self):
        """Initiate fade out animation"""
        QTimer.singleShot(300, self.fade_out_animation)
    
    def fade_out_animation(self):
        """Animate splash screen fade out"""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.finished.connect(self.on_finished)
        self.fade_animation.start()
    
    def on_finished(self):
        """Emit finished signal when animation completes"""
        if hasattr(self, "loader_timer"):
            self.loader_timer.stop()
        self.close()
        self.finished.emit()

    def animate_loader(self):
        """Cycle loader dots to show motion"""
        if not hasattr(self, "loader_states"):
            return
        self.loader_index = (self.loader_index + 1) % len(self.loader_states)
        self.loader_label.setText(self.loader_states[self.loader_index])