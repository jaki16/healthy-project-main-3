"""
Main Window dengan Sidebar Navigation
HealthTrack AI Pro - Final Project Version
File: src/ui/windows/main_window.py

Author: [Your Name]
Created: December 2024
Description: Main application window with sidebar navigation and page management
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QStackedWidget, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont

# Import pages with proper error handling
try:
    from ui.pages.dashboard import DashboardPage
    DASHBOARD_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Dashboard not available - {e}")
    DASHBOARD_AVAILABLE = False

try:
    from ui.pages.nutrition import NutritionPage
    NUTRITION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Nutrition page not available - {e}")
    NUTRITION_AVAILABLE = False

try:
    # Import the activity page from the correct module name
    from ui.pages.activity_page import ActivityPage
    ACTIVITY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Activity page not available - {e}")
    ACTIVITY_AVAILABLE = False

try:
    from ui.pages.health import HealthPage
    HEALTH_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: Health page not available - {e}")
    HEALTH_AVAILABLE = False

try:
    from ui.pages.ai_assistant import AIAssistantPage
    AI_ASSISTANT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: AI Assistant not available - {e}")
    AI_ASSISTANT_AVAILABLE = False


class NavButton(QPushButton):
    """
    Custom navigation button with hover effects
    
    Features:
    - Checkable state for active page indication
    - Smooth hover animations
    - Icon + text display
    """
    
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"{icon_text}  {text}")
        self.setCheckable(True)
        self.setMinimumHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Set font
        font = QFont("Segoe UI", 11)
        self.setFont(font)
        
        self.setStyleSheet("""
            NavButton {
                background-color: transparent;
                color: #CCCCCC;
                text-align: left;
                padding-left: 30px;
                border: none;
                border-left: 3px solid transparent;
            }
            NavButton:hover {
                background-color: rgba(255, 255, 255, 0.05);
                color: #FFFFFF;
            }
            NavButton:checked {
                background-color: rgba(0, 191, 165, 0.15);
                color: #00BFA5;
                border-left: 3px solid #00BFA5;
            }
        """)


class Sidebar(QFrame):
    """
    Application sidebar with navigation menu
    
    Features:
    - Logo and branding
    - Navigation buttons
    - User information display
    - Page change signal emission
    """
    
    page_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(280)
        self.setObjectName("sidebar")
        self.setup_ui()
    
    def setup_ui(self):
        """Setup sidebar UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header Section
        header = QWidget()
        header.setFixedHeight(80)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        logo = QLabel("HealthTrack AI")
        logo.setStyleSheet("color: #00BFA5; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(logo)
        
        tagline = QLabel("Pro")
        tagline.setStyleSheet("color: #888888; font-size: 12px;")
        header_layout.addWidget(tagline)
        
        layout.addWidget(header)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # Navigation Buttons
        layout.addSpacing(20)
        
        nav_items = [
            ("Dashboard", "🏠", 0),
            ("Nutrition", "🍎", 1),
            ("Activity", "🏃", 2),
            ("Health", "❤️", 3),
            ("AI Assistant", "🤖", 4),
            ("Devices", "⌚", 5),
            ("Reports", "📊", 6),
            ("Settings", "⚙️", 7),
        ]
        
        self.nav_buttons = []
        for name, icon, index in nav_items:
            btn = NavButton(name, icon)
            btn.clicked.connect(lambda checked, i=index: self.on_nav_clicked(i))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        layout.addStretch()
        
        # User Information Section
        user_section = QWidget()
        user_section.setFixedHeight(80)
        user_layout = QVBoxLayout(user_section)
        user_layout.setContentsMargins(20, 10, 20, 10)
        
        user_name = QLabel("👤 John Doe")
        user_name.setStyleSheet("color: #CCCCCC; font-size: 13px; font-weight: bold;")
        user_layout.addWidget(user_name)
        
        user_status = QLabel("Premium Member")
        user_status.setStyleSheet("color: #00BFA5; font-size: 11px;")
        user_layout.addWidget(user_status)
        
        layout.addWidget(user_section)
        
        # Apply sidebar styling
        self.setStyleSheet("""
            #sidebar {
                background-color: #252525;
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Set dashboard as default active page
        self.nav_buttons[0].setChecked(True)
    
    def on_nav_clicked(self, index):
        """
        Handle navigation button clicks
        
        Args:
            index (int): Index of the page to navigate to
        """
        # Uncheck all buttons
        for btn in self.nav_buttons:
            btn.setChecked(False)
        
        # Check clicked button
        self.nav_buttons[index].setChecked(True)
        
        # Emit page change signal
        self.page_changed.emit(index)


class PlaceholderPage(QWidget):
    """
    Placeholder page for features under development
    
    Displays:
    - Page title
    - "Under development" message
    - "Coming soon" indicator
    """
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Setup placeholder page UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel(self.title)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #00BFA5;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("This page is under development")
        desc.setStyleSheet("""
            font-size: 16px;
            color: #888888;
            margin-top: 20px;
        """)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Coming soon indicator
        coming = QLabel("✨ Coming Soon ✨")
        coming.setStyleSheet("""
            font-size: 24px;
            color: #CCCCCC;
            margin-top: 40px;
        """)
        coming.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(coming)


class MainWindow(QMainWindow):
    """
    Main application window
    
    Features:
    - Sidebar navigation
    - Stacked widget for page management
    - Smooth page transitions
    - Responsive layout
    
    Architecture:
    - Uses QStackedWidget for page management
    - Signal-slot pattern for navigation
    - Modular page loading with error handling
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HealthTrack AI Pro")
        self.setGeometry(100, 50, 1400, 900)
        self.setMinimumSize(1200, 700)
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup main window UI components"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (horizontal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)
        
        # Content area (stacked pages)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Load all pages
        self.add_pages()
    
    def add_pages(self):
        """
        Load and add pages to stacked widget
        
        Pages loaded:
        0. Dashboard - Health metrics and real-time data
        1. Nutrition - Food tracking and calorie management
        2. Activity - Exercise and activity logging
        3-7. Placeholder pages for future features
        """
        
        print("\n" + "="*60)
        print("📦 Loading Application Pages...")
        print("="*60)
        
        # Page 0: Dashboard
        if DASHBOARD_AVAILABLE:
            try:
                self.dashboard_page = DashboardPage()
                self.content_stack.addWidget(self.dashboard_page)
                print("✓ Dashboard page loaded")
            except Exception as e:
                print(f"✗ Dashboard error: {e}")
                self.content_stack.addWidget(PlaceholderPage("Dashboard"))
        else:
            self.content_stack.addWidget(PlaceholderPage("Dashboard"))
        
        # Page 1: Nutrition
        if NUTRITION_AVAILABLE:
            try:
                self.nutrition_page = NutritionPage()
                self.content_stack.addWidget(self.nutrition_page)
                print("✓ Nutrition page loaded")
            except Exception as e:
                print(f"✗ Nutrition error: {e}")
                self.content_stack.addWidget(PlaceholderPage("Nutrition"))
        else:
            self.content_stack.addWidget(PlaceholderPage("Nutrition"))
        
        # Page 2: Activity
        if ACTIVITY_AVAILABLE:
            try:
                self.activity_page = ActivityPage()
                self.content_stack.addWidget(self.activity_page)
                print("✓ Activity page loaded")
            except Exception as e:
                print(f"✗ Activity error: {e}")
                self.content_stack.addWidget(PlaceholderPage("Activity"))
        else:
            self.content_stack.addWidget(PlaceholderPage("Activity"))
        
        # Page 3: Health
        if HEALTH_AVAILABLE:
            try:
                self.health_page = HealthPage()
                self.content_stack.addWidget(self.health_page)
                print("✓ Health page loaded")
            except Exception as e:
                print(f"✗ Health error: {e}")
                self.content_stack.addWidget(PlaceholderPage("Health"))
        else:
            self.content_stack.addWidget(PlaceholderPage("Health"))
        
        # Pages 4-7: Placeholder pages for future development
        placeholder_pages = [
            # Index 4: AI Assistant (if available)
            None,
            "Devices",       # Smartwatch integration
            "Reports",       # Health reports and analytics
            "Settings"       # App settings and preferences
        ]
        
        # Page 4: AI Assistant
        if AI_ASSISTANT_AVAILABLE:
            try:
                self.ai_page = AIAssistantPage()
                self.content_stack.addWidget(self.ai_page)
                print("✓ AI Assistant page loaded")
            except Exception as e:
                print(f"✗ AI Assistant error: {e}")
                self.content_stack.addWidget(PlaceholderPage("AI Assistant"))
        else:
            self.content_stack.addWidget(PlaceholderPage("AI Assistant"))
        
        # Remaining placeholders (Devices, Reports, Settings)
        for page_title in placeholder_pages[1:]:
            page = PlaceholderPage(page_title)
            self.content_stack.addWidget(page)
        
        print("="*60)
        print(f"✓ {self.content_stack.count()} pages loaded successfully")
        print("="*60 + "\n")
    
    def switch_page(self, index):
        """
        Switch to a different page
        
        Args:
            index (int): Index of the page to switch to
            
        Features:
        - Validates page index
        - Logs page navigation
        - Smooth transition without animation (for stability)
        """
        if index >= self.content_stack.count():
            print(f"⚠️  Invalid page index: {index}")
            return
        
        # Page names for logging
        page_names = ["Dashboard", "Nutrition", "Activity", "Health", 
                     "AI Assistant", "Devices", "Reports", "Settings"]
        
        if index < len(page_names):
            print(f"→ Navigating to: {page_names[index]}")
        
        # Simple page switch (stable and fast)
        self.content_stack.setCurrentIndex(index)
    
    def apply_styles(self):
        """Apply global application styles"""
        self.setStyleSheet("""
            /* Main Window */
            QMainWindow {
                background-color: #1e1e1e;
            }
            
            /* Global Widget Styles */
            QWidget {
                background-color: #1e1e1e;
                color: #FFFFFF;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            
            /* Label Styles */
            QLabel {
                color: #FFFFFF;
            }
            
            /* Scrollbar Styles */
            QScrollBar:vertical {
                background-color: #2D2D2D;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #00BFA5;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background-color: #2D2D2D;
                height: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #555555;
                border-radius: 6px;
                min-width: 20px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #00BFA5;
            }
        """)