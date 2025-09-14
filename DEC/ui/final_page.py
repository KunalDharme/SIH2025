# final_page.py
import os
import pandas as pd
from PyQt5.QtCore import Qt, QUrl, QProcess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QApplication, QFrame
)
from PyQt5.QtGui import QFont, QDesktopServices # QDesktopServices should be imported from QtGui
import sys


class FinalPage(QWidget):
    def __init__(self, switch_callback, session_state):
        super().__init__()
        self.switch_callback = switch_callback
        self.session_state = session_state
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        header = QLabel("✅ Analysis Complete")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setStyleSheet("color:#00ffcc;")
        main_layout.addWidget(header, alignment=Qt.AlignCenter)
        main_layout.addSpacing(20)

        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background: #2a2d33;
                border: 2px solid #3c4048;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        summary_layout = QVBoxLayout(summary_frame)
        self.summary = QLabel("")
        self.summary.setStyleSheet("color:#EEE; font-size: 14px;")
        self.summary.setAlignment(Qt.AlignCenter)
        summary_layout.addWidget(self.summary)
        main_layout.addWidget(summary_frame)
        main_layout.addSpacing(30)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        save_btn = self._create_button("📥 Save Report (CSV)", self.save_report)
        open_btn = self._create_button("📂 Open Output Folder", self.open_output)
        exit_btn = self._create_button("Exit", lambda: QApplication.quit())

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(exit_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)

    def _create_button(self, text, handler):
        btn = QPushButton(text)
        btn.clicked.connect(handler)
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00ffcc, stop:1 #0066ff);
                color: black;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00e6b8, stop:1 #0052cc);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00b39c, stop:1 #003a80);
            }
        """)
        return btn

    def show_summary(self):
        df = self.session_state.get("last_df")
        if df is None or df.empty:
            self.summary.setText("<font color='#ff6b6b'>No report available. Analysis may have failed.</font>")
            return
        
        total = len(df)
        high = (df["risk_level"] == "HIGH").sum() if "risk_level" in df.columns else 0
        med = (df["risk_level"] == "MEDIUM").sum() if "risk_level" in df.columns else 0
        low = (df["risk_level"] == "LOW").sum() if "risk_level" in df.columns else 0
        
        html_summary = f"""
        <p style="font-weight: bold; font-size: 18px;">Analysis Summary</p>
        <hr style="border: 1px solid #00ffcc; width: 50%; margin: 10px auto;">
        <br>
        <p>Total files analyzed: <span style="font-weight: bold; color: #00ffcc;">{total}</span></p>
        <p>Files with <span style="font-weight: bold; color: #ff6b6b;">HIGH</span> risk: <span style="font-weight: bold; color: #ff6b6b;">{high}</span></p>
        <p>Files with <span style="font-weight: bold; color: #feca57;">MEDIUM</span> risk: <span style="font-weight: bold; color: #feca57;">{med}</span></p>
        <p>Files with <span style="font-weight: bold; color: #48dbfb;">LOW</span> risk: <span style="font-weight: bold; color: #48dbfb;">{low}</span></p>
        """
        self.summary.setText(html_summary)

    def save_report(self):
        df = self.session_state.get("last_df")
        if df is None or df.empty:
            QMessageBox.warning(self, "No Report", "No report to save.")
            return

        dest_folder = self.session_state.get("dest", "")
        default_path = os.path.join(dest_folder, "forensic_report.csv")
        
        path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Report As", 
            default_path, 
            "CSV Files (*.csv);;All Files (*)"
        )
        if path:
            try:
                df.to_csv(path, index=False)
                QMessageBox.information(self, "Saved", f"Report successfully saved to:<br>{path}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save report: {e}")

    def open_output(self):
        output_path = self.session_state.get("dest", "")
        if not output_path or not os.path.exists(output_path):
            QMessageBox.warning(self, "Path Not Found", "The destination path does not exist.")
            return

        url = QUrl.fromLocalFile(output_path)
        if not QDesktopServices.openUrl(url):
            QMessageBox.critical(self, "Error", f"Could not open folder: {output_path}")