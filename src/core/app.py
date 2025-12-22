"""
Application core class
"""
from PyQt6.QtWidgets import QApplication
from ui.windows.splash_screen import SplashScreen
from ui.windows.main_window import MainWindow

class HealthTrackApp:
    """Main application class"""
    
    def __init__(self):
        self.main_window = None
        self.splash = None
    
    def run(self):
        """Run the application"""
        # Show splash screen
        self.splash = SplashScreen()
        self.splash.show()
        
        # Initialize main window
        self.main_window = MainWindow()
        
        # Close splash and show main window
        self.splash.finish(self.main_window)
        self.main_window.show()
