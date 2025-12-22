"""
HealthTrack AI Pro - Main Entry Point
File: src/main.py

Run: python src/main.py
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Import windows
from ui.windows.splash_screen import SplashScreen
from ui.windows.main_window import MainWindow


def main():
    """Main application entry point"""
    
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("HealthTrack AI Pro")
    app.setOrganizationName("HealthTrack")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle("Fusion")
    
    print("\n" + "="*60)
    print("🚀 HealthTrack AI Pro - Starting Application")
    print("="*60)
    print(f"✓ Python version: {sys.version.split()[0]}")
    print(f"✓ PyQt6 loaded successfully")
    print(f"✓ Application initialized")
    
    # Check if we should show splash screen
    SHOW_SPLASH = True  # Set False untuk skip splash screen saat development
    
    if SHOW_SPLASH:
        # Show splash screen
        print("\n📱 Loading splash screen...")
        splash = SplashScreen()
        splash.show()
        
        # Create main window (hidden)
        main_window = MainWindow()
        
        # Connect splash finished signal to show main window
        def show_main():
            splash.close()
            main_window.show()
            print("✓ Main window displayed")
            print("\n" + "="*60)
            print("✨ Application ready!")
            print("="*60 + "\n")
        
        splash.finished.connect(show_main)
    else:
        # Show main window directly (faster for development)
        print("\n📱 Loading main window...")
        main_window = MainWindow()
        main_window.show()
        print("✓ Main window displayed")
        print("\n" + "="*60)
        print("✨ Application ready!")
        print("="*60 + "\n")
    
    # Start application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)