"""
HealthTrack AI Pro - Main Entry Point
File: src/main.py

Run: python src/main.py
"""

import sys
import io
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add src directory to Python path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

# Add parent directory to path for veev_config
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Import VEEV mode
try:
    from veev_config import initialize_veev_mode, VeevPagefileFactory
    VEEV_AVAILABLE = True
except ImportError:
    VEEV_AVAILABLE = False

# Import windows
from ui.windows.splash_screen import SplashScreen
from ui.windows.main_window import MainWindow


def main():
    """Main application entry point"""
    
    # Initialize VEEV mode (pagefile and virtual memory optimization)
    if VEEV_AVAILABLE:
        try:
            print("\n[VEEV] Initializing Virtual Environment Enhanced Virtual (VEEV) mode...")
            success, veev_info = initialize_veev_mode(debug=False)
            if success:
                print("[VEEV] VEEV mode initialized successfully")
                print(f"[VEEV] Memory available: {veev_info['memory_stats'].get('available_memory_mb', 'N/A')} MB")
            else:
                print("[VEEV] VEEV mode initialization failed, continuing without optimization")
        except Exception as e:
            print(f"[VEEV] Error initializing VEEV mode: {e}")
    
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
    print("HealthTrack AI Pro - Starting Application")
    print("="*60)
    print(f"[OK] Python version: {sys.version.split()[0]}")
    print(f"[OK] PyQt6 loaded successfully")
    print(f"[OK] Application initialized")
    
    # Check if we should show splash screen
    SHOW_SPLASH = True  # Set False untuk skip splash screen saat development
    
    if SHOW_SPLASH:
        # Show splash screen
        print("\n[INFO] Loading splash screen...")
        splash = SplashScreen()
        splash.show()
        
        # Create main window (hidden)
        main_window = MainWindow()
        
        # Connect splash finished signal to show main window
        def show_main():
            splash.close()
            main_window.show()
            print("[OK] Main window displayed")
            print("\n" + "="*60)
            print("Application ready!")
            print("="*60 + "\n")
        
        splash.finished.connect(show_main)
    else:
        # Show main window directly (faster for development)
        print("\n[INFO] Loading main window...")
        main_window = MainWindow()
        main_window.show()
        print("[OK] Main window displayed")
        print("\n" + "="*60)
        print("Application ready!")
        print("="*60 + "\n")
    
    # Start application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
