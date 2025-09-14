# dec_app.py
# Main application file for Digital Evidence Categorizer (DEC)
# Handles the main window, page switching, and app startup

import sys
import os
import time
import shutil
import threading
import datetime
import ctypes # DPI fix for Windows
from pathlib import Path

# Ensure Python can find the ui and dec packages
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# -------------------- DPI Fix for Windows --------------------
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# -------------------- PyQt5 Imports --------------------
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedLayout, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox,
    QProgressBar, QPlainTextEdit, QFormLayout, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon

# -------------------- Import Pages & Worker --------------------
from ui.terms_page import TermsPage
from ui.splash_page import SplashPage
from ui.login_page import LoginPage
from ui.setup_page import SetupPage
from ui.options_page import OptionsPage
from ui.processing_page import ProcessingPage
from ui.analysis_worker import AnalysisWorker
from ui.final_page import FinalPage

# -------------------- Backend Imports --------------------
import pandas as pd
from dec.scanner import scan_directory
from dec.categorizer import categorize_file
from dec.keyword_search import load_keywords, search_keywords
from dec.scoring import assign_risk_level

# -------------------- Constants --------------------
REPORT_PATH = "output/report.csv" # Default path for saving reports


# -------------------- Main Application Window --------------------
class MainWindow(QMainWindow):
    """
    Main window that manages all pages and handles page switching.
    Uses a QStackedLayout to switch between different pages with proper geometry management.
    """
    def __init__(self):
        super().__init__()

        # -------------------- Window Settings --------------------
        self.setWindowTitle("Digital Evidence Categorizer (DEC)")
        self.setMinimumSize(800, 600) # Set minimum size for all pages
        
        # Set application icon if available
        # self.setWindowIcon(QIcon("path/to/icon.png"))
        
        self.setStyleSheet("""
            QMainWindow { 
                background: #0e1117; 
                color: #e0e0e0; 
            }
        """)

        # -------------------- Session State --------------------
        self.session_state = {}

        # -------------------- Container & Layout --------------------
        self.container = QWidget()
        self.layout = QStackedLayout()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # -------------------- Page Geometries --------------------
        # Define optimal sizes for each page
        self.page_geometries = {
            "terms": {"size": (850, 640), "resizable": False, "center": True},
            "splash": {"size": (900, 650), "resizable": False, "center": True},
            "login": {"size": (900, 650), "resizable": False, "center": True},
            "setup": {"size": (1000, 700), "resizable": True, "center": True},
            "options": {"size": (1100, 750), "resizable": True, "center": True},
            "processing": {"size": (1200, 800), "resizable": True, "center": True},
            "final": {"size": (1150, 780), "resizable": True, "center": True}
        }

        # -------------------- Initialize Pages --------------------
        self.terms = TermsPage(self.switch_to)
        self.splash = SplashPage(self.switch_to)
        self.login = LoginPage(self.switch_to, self.session_state)
        self.setup = SetupPage(self.switch_to, self.session_state)
        self.options = OptionsPage(self.switch_to, self.session_state)
        self.processing = ProcessingPage(self.switch_to, self.session_state)
        self.final = FinalPage(self.switch_to, self.session_state)

        # Add all pages to the stacked layout
        for page in (self.terms, self.splash, self.login,
                     self.setup, self.options, self.processing, self.final):
            self.layout.addWidget(page)

        # Store current page for reference
        self.current_page = None

        # Start at the Terms page and apply its specific window settings
        self.switch_to("terms")

    # -------------------- Geometry Management --------------------
    def center_window(self):
        """Center the window on the screen"""
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        x = (screen.width() - window_geometry.width()) // 2
        y = (screen.height() - window_geometry.height()) // 2
        self.move(x, y)

    def apply_page_geometry(self, page_name):
        """Apply specific geometry settings for the given page"""
        if page_name not in self.page_geometries:
            return

        config = self.page_geometries[page_name]
        width, height = config["size"]
        resizable = config.get("resizable", True)

        # Use window flags to control resizability
        if not resizable:
            self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
            self.setFixedSize(width, height)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.MSWindowsFixedSizeDialogHint)
            self.setMinimumSize(800, 600) # Keep a consistent minimum size
            self.setMaximumSize(16777215, 16777215)
            self.resize(width, height)

        # Center the window if requested
        if config.get("center", False):
            self.center_window()
        else:
            # If not centered, reset position to avoid issues
            self.move(100, 100)

    # -------------------- Page Switching --------------------
    def switch_to(self, page_name):
        """Switch to the specified page with appropriate geometry"""
        previous_page = self.current_page
        self.current_page = page_name

        self.apply_page_geometry(page_name)
        
        # Handle page-specific logic
        if page_name == "terms":
            self.layout.setCurrentWidget(self.terms)
        elif page_name == "splash":
            self.layout.setCurrentWidget(self.splash)
        elif page_name == "login":
            self.layout.setCurrentWidget(self.login)
        elif page_name == "setup":
            self.layout.setCurrentWidget(self.setup)
            if previous_page == "login" and hasattr(self.setup, 'initialize_setup'):
                self.setup.initialize_setup()
        elif page_name == "processing":
            self.layout.setCurrentWidget(self.processing)
            QTimer.singleShot(200, self.processing.start_analysis)
        elif page_name == "final":
            if hasattr(self.final, 'show_summary'):
                self.final.show_summary()
            self.layout.setCurrentWidget(self.final)

        self.show()
        self.raise_()
        self.activateWindow()

    # (Other methods like get_optimal_size_for_content, save_window_state, etc. remain the same)
    def get_optimal_size_for_content(self, page_widget):
        # ... (same as before) ...
        size_hint = page_widget.sizeHint()
        min_size = page_widget.minimumSizeHint()
        
        optimal_width = max(size_hint.width(), min_size.width()) + 50
        optimal_height = max(size_hint.height(), min_size.height()) + 100
        
        return optimal_width, optimal_height

    def save_window_state(self):
        # ... (same as before) ...
        pass

    def restore_window_state(self):
        # ... (same as before) ...
        pass

    def closeEvent(self, event):
        # ... (same as before) ...
        if hasattr(self.processing, 'stop_analysis'):
            self.processing.stop_analysis()
        event.accept()

    def resizeEvent(self, event):
        # ... (same as before) ...
        super().resizeEvent(event)
        current_widget = self.layout.currentWidget()
        if hasattr(current_widget, 'update_layout_on_resize'):
            current_widget.update_layout_on_resize()

    # -------------------- Utility Methods --------------------
    def is_maximized_or_fullscreen(self):
        # ... (same as before) ...
        return self.isMaximized() or self.isFullScreen()

    def toggle_fullscreen(self):
        # ... (same as before) ...
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def set_page_resizable(self, page_name, resizable=True):
        # ... (same as before) ...
        if page_name in self.page_geometries:
            self.page_geometries[page_name]["resizable"] = resizable
            if self.current_page == page_name:
                self.apply_page_geometry(page_name)


# -------------------- Run Application --------------------
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


# -------------------- Entry Point --------------------
if __name__ == "__main__":
    main()
