"""
Theme System - Dark and Light Mode
File: src/ui/styles/themes.py

Manages application themes and color schemes
"""

from enum import Enum
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication


class ThemeMode(Enum):
    """Theme mode enum"""
    DARK = "dark"
    LIGHT = "light"


class Theme:
    """Theme color definitions"""
    
    # Dark Theme Colors
    DARK = {
        # Primary Colors
        "primary": "#00BFA5",
        "primary_light": "#00E5CC",
        "primary_dark": "#00896B",
        
        # Background Colors
        "bg_primary": "#1E1E1E",
        "bg_secondary": "#252525",
        "bg_tertiary": "#2D2D2D",
        
        # Text Colors
        "text_primary": "#FFFFFF",
        "text_secondary": "#CCCCCC",
        "text_tertiary": "#888888",
        "text_disabled": "#666666",
        
        # Border Colors
        "border_primary": "#3D3D3D",
        "border_secondary": "#2D2D2D",
        "border_hover": "#00BFA5",
        
        # Status Colors
        "success": "#00BFA5",
        "warning": "#FF9800",
        "error": "#FF5252",
        "info": "#2196F3",
        
        # Chart Colors
        "chart_1": "#00BFA5",
        "chart_2": "#FF4081",
        "chart_3": "#FFD54F",
        "chart_4": "#7C4DFF",
        "chart_5": "#FF6B6B",
    }
    
    # Light Theme Colors
    LIGHT = {
        # Primary Colors
        "primary": "#00BFA5",
        "primary_light": "#00E5CC",
        "primary_dark": "#00896B",
        
        # Background Colors
        "bg_primary": "#FFFFFF",
        "bg_secondary": "#F5F5F5",
        "bg_tertiary": "#EEEEEE",
        
        # Text Colors
        "text_primary": "#212121",
        "text_secondary": "#424242",
        "text_tertiary": "#757575",
        "text_disabled": "#BDBDBD",
        
        # Border Colors
        "border_primary": "#E0E0E0",
        "border_secondary": "#EEEEEE",
        "border_hover": "#00BFA5",
        
        # Status Colors
        "success": "#00BFA5",
        "warning": "#FF9800",
        "error": "#FF5252",
        "info": "#2196F3",
        
        # Chart Colors
        "chart_1": "#00BFA5",
        "chart_2": "#FF4081",
        "chart_3": "#FFD54F",
        "chart_4": "#7C4DFF",
        "chart_5": "#FF6B6B",
    }
    
    @staticmethod
    def get_colors(mode: ThemeMode):
        """Get color scheme for theme mode"""
        return Theme.DARK if mode == ThemeMode.DARK else Theme.LIGHT


class ThemeManager:
    """Manages application theme"""
    
    _instance = None
    _current_theme = ThemeMode.DARK
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.colors = Theme.get_colors(self._current_theme)
    
    @property
    def current_theme(self):
        """Get current theme mode"""
        return self._current_theme
    
    def set_theme(self, mode: ThemeMode):
        """Set theme mode"""
        self._current_theme = mode
        self.colors = Theme.get_colors(mode)
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        new_mode = ThemeMode.LIGHT if self._current_theme == ThemeMode.DARK else ThemeMode.DARK
        self.set_theme(new_mode)
        return new_mode
    
    def get_stylesheet(self):
        """Get complete application stylesheet"""
        c = self.colors
        
        return f"""
            /* ========== Global Styles ========== */
            QWidget {{
                background-color: {c['bg_primary']};
                color: {c['text_primary']};
                font-family: "Segoe UI", Arial, sans-serif;
            }}
            
            QMainWindow {{
                background-color: {c['bg_primary']};
            }}
            
            /* ========== Labels ========== */
            QLabel {{
                color: {c['text_primary']};
                background-color: transparent;
            }}
            
            /* ========== Buttons ========== */
            QPushButton {{
                background-color: {c['bg_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['border_primary']};
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 11px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {c['bg_secondary']};
                border-color: {c['border_hover']};
            }}
            
            QPushButton:pressed {{
                background-color: {c['primary_dark']};
            }}
            
            QPushButton:disabled {{
                background-color: {c['bg_tertiary']};
                color: {c['text_disabled']};
                border-color: {c['border_secondary']};
            }}
            
            /* Primary Button */
            QPushButton[primary="true"] {{
                background-color: {c['primary']};
                color: white;
                border: none;
            }}
            
            QPushButton[primary="true"]:hover {{
                background-color: {c['primary_light']};
            }}
            
            /* ========== Input Fields ========== */
            QLineEdit, QTextEdit {{
                background-color: {c['bg_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['border_primary']};
                border-radius: 8px;
                padding: 8px 12px;
                selection-background-color: {c['primary']};
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border-color: {c['primary']};
                background-color: {c['bg_secondary']};
            }}
            
            QLineEdit::placeholder, QTextEdit::placeholder {{
                color: {c['text_disabled']};
            }}
            
            /* ========== Combo Box ========== */
            QComboBox {{
                background-color: {c['bg_tertiary']};
                color: {c['text_primary']};
                border: 2px solid {c['border_primary']};
                border-radius: 8px;
                padding: 8px 12px;
                min-height: 30px;
            }}
            
            QComboBox:hover {{
                border-color: {c['primary']};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {c['bg_secondary']};
                color: {c['text_primary']};
                selection-background-color: {c['primary']};
                border: 1px solid {c['border_primary']};
                border-radius: 8px;
            }}
            
            /* ========== Scroll Bars ========== */
            QScrollBar:vertical {{
                background-color: {c['bg_tertiary']};
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {c['border_primary']};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {c['primary']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background-color: {c['bg_tertiary']};
                height: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {c['border_primary']};
                border-radius: 6px;
                min-width: 20px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {c['primary']};
            }}
            
            /* ========== Progress Bar ========== */
            QProgressBar {{
                background-color: {c['bg_tertiary']};
                border: none;
                border-radius: 5px;
                text-align: center;
                color: {c['text_primary']};
            }}
            
            QProgressBar::chunk {{
                background-color: {c['primary']};
                border-radius: 5px;
            }}
            
            /* ========== Tab Widget ========== */
            QTabWidget::pane {{
                border: 1px solid {c['border_primary']};
                border-radius: 8px;
                background-color: {c['bg_secondary']};
            }}
            
            QTabBar::tab {{
                background-color: {c['bg_tertiary']};
                color: {c['text_secondary']};
                border: 1px solid {c['border_primary']};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 10px 20px;
                margin-right: 2px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {c['bg_secondary']};
                color: {c['primary']};
                border-bottom: 2px solid {c['primary']};
            }}
            
            QTabBar::tab:hover {{
                background-color: {c['bg_secondary']};
            }}
            
            /* ========== Tooltips ========== */
            QToolTip {{
                background-color: {c['bg_secondary']};
                color: {c['text_primary']};
                border: 1px solid {c['border_primary']};
                border-radius: 5px;
                padding: 5px;
            }}
            
            /* ========== Menu ========== */
            QMenu {{
                background-color: {c['bg_secondary']};
                color: {c['text_primary']};
                border: 1px solid {c['border_primary']};
                border-radius: 8px;
                padding: 5px;
            }}
            
            QMenu::item {{
                padding: 8px 25px;
                border-radius: 5px;
            }}
            
            QMenu::item:selected {{
                background-color: {c['primary']};
                color: white;
            }}
            
            QMenu::separator {{
                height: 1px;
                background-color: {c['border_primary']};
                margin: 5px 10px;
            }}
            
            /* ========== Checkbox & Radio ========== */
            QCheckBox, QRadioButton {{
                color: {c['text_primary']};
                spacing: 8px;
            }}
            
            QCheckBox::indicator, QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {c['border_primary']};
                border-radius: 4px;
                background-color: {c['bg_tertiary']};
            }}
            
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
                background-color: {c['primary']};
                border-color: {c['primary']};
            }}
            
            /* ========== Slider ========== */
            QSlider::groove:horizontal {{
                height: 6px;
                background-color: {c['bg_tertiary']};
                border-radius: 3px;
            }}
            
            QSlider::handle:horizontal {{
                background-color: {c['primary']};
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            
            QSlider::handle:horizontal:hover {{
                background-color: {c['primary_light']};
            }}
        """
    
    def apply_to_app(self, app: QApplication):
        """Apply theme to QApplication"""
        app.setStyleSheet(self.get_stylesheet())


# Global theme instance
theme_manager = ThemeManager()