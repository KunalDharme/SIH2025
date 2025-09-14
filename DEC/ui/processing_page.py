# processing_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit,
    QProgressBar, QMessageBox, QPushButton, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import pandas as pd
import os
import json

# Import your worker class
from ui.analysis_worker import AnalysisWorker

class ProcessingPage(QWidget):
    def __init__(self, switch_callback, session_state):
        super().__init__()
        self.switch_callback = switch_callback
        self.session_state = session_state
        self.worker = None
        self._setup_ui()

    def _setup_ui(self):
        """Set up the UI with the same theme as your original processing page"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(20)
        
        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: rgba(0, 255, 204, 0.1);
                border: 1px solid #00ffcc;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        header = QLabel("🛠️ Running Forensic Analysis")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: #00ffcc; background: transparent; border: none;")
        header.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(header)
        
        # Configuration summary
        self.config_label = QLabel()
        self.config_label.setFont(QFont("Segoe UI", 10))
        self.config_label.setStyleSheet("color: #e0e0e0; background: transparent; border: none; margin-top: 10px;")
        self.config_label.setAlignment(Qt.AlignCenter)
        self.config_label.setWordWrap(True)
        header_layout.addWidget(self.config_label)
        
        main_layout.addWidget(header_frame)

        # Progress section
        progress_frame = QFrame()
        progress_frame.setStyleSheet("""
            QFrame {
                background: rgba(34, 34, 34, 0.8);
                border: 1px solid #444;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        progress_layout = QVBoxLayout(progress_frame)
        
        # Current task label
        self.current_task_label = QLabel("Initializing analysis...")
        self.current_task_label.setFont(QFont("Segoe UI", 11, QFont.Medium))
        self.current_task_label.setStyleSheet("color: #00ffcc; background: transparent; border: none;")
        progress_layout.addWidget(self.current_task_label)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setMinimumHeight(25)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #222;
                color: #FFF;
                border: 2px solid #444;
                border-radius: 12px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                           stop:0 #00ffcc, stop:1 #0066ff);
                border-radius: 10px;
            }
        """)
        progress_layout.addWidget(self.progress)
        
        # Statistics display
        stats_layout = QHBoxLayout()
        
        self.files_processed_label = QLabel("Files: 0")
        self.files_processed_label.setStyleSheet("color: #e0e0e0; font-size: 10px;")
        stats_layout.addWidget(self.files_processed_label)
        
        self.suspicious_found_label = QLabel("Suspicious: 0")
        self.suspicious_found_label.setStyleSheet("color: #ff6b6b; font-size: 10px;")
        stats_layout.addWidget(self.suspicious_found_label)
        
        self.time_elapsed_label = QLabel("Time: 00:00")
        self.time_elapsed_label.setStyleSheet("color: #e0e0e0; font-size: 10px;")
        stats_layout.addWidget(self.time_elapsed_label)
        
        stats_layout.addStretch()
        progress_layout.addLayout(stats_layout)
        
        main_layout.addWidget(progress_frame)

        # Log display
        log_label = QLabel("Analysis Log:")
        log_label.setFont(QFont("Segoe UI", 12, QFont.Medium))
        log_label.setStyleSheet("color: #e0e0e0; margin-top: 10px;")
        main_layout.addWidget(log_label)
        
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("""
            QPlainTextEdit {
                background: #000;
                color: #00FF00;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: 2px solid #333;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.log.setMinimumHeight(250)
        main_layout.addWidget(self.log)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Stop analysis button (visible during processing)
        self.stop_btn = QPushButton("⏹️ Stop Analysis")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                           stop:0 #ff6b6b, stop:1 #ff4757);
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                           stop:0 #ff5252, stop:1 #ff3742);
            }
            QPushButton:pressed {
                background: #ff4757;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_analysis)
        self.stop_btn.setVisible(True)
        button_layout.addWidget(self.stop_btn)
        
        # View results button (visible after completion)
        self.view_results_btn = QPushButton("📊 View Results")
        self.view_results_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                           stop:0 #00ffcc, stop:1 #0066ff);
                color: black;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 140px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                           stop:0 #00e6b8, stop:1 #0052cc);
            }
            QPushButton:pressed {
                background: #0066ff;
                color: white;
            }
        """)
        self.view_results_btn.setVisible(False)
        self.view_results_btn.clicked.connect(lambda: self.switch_callback("final"))
        button_layout.addWidget(self.view_results_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        
        # Initialize statistics
        self.files_processed = 0
        self.suspicious_files = 0
        self.start_time = None
        
        # Timer for updating elapsed time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_elapsed_time)

    def display_configuration_summary(self):
        """Display a summary of the selected configuration"""
        config_parts = []
        
        # Security level
        security_level = self.session_state.get("security_level", "Standard Scan")
        config_parts.append(f"Security Level: {security_level}")
        
        # File types count
        selected_extensions = self.session_state.get("selected_extensions", [])
        config_parts.append(f"File Types: {len(selected_extensions)} selected")
        
        # Keywords type
        if self.session_state.get("use_custom_keywords", False):
            config_parts.append("Keywords: Custom file")
        else:
            config_parts.append("Keywords: Built-in database")
        
        # Additional options
        options = []
        if self.session_state.get("copy_suspicious", False):
            options.append("Copy suspicious files")
        if self.session_state.get("real_time_monitoring", False):
            options.append("Real-time monitoring")
        
        if options:
            config_parts.append(f"Options: {', '.join(options)}")
        
        config_text = " | ".join(config_parts)
        self.config_label.setText(config_text)

    def start_analysis(self):
        """Initialize and start the analysis worker thread based on setup configuration"""
        # Get paths from session state
        source_folder = self.session_state.get("source_folder")
        dest_folder = self.session_state.get("dest_folder")
        
        # Validate required paths
        if not source_folder or not dest_folder:
            QMessageBox.warning(self, "Configuration Error", 
                              "Source or destination folder is missing. Please check your setup configuration.")
            self.switch_callback("setup")  # Go back to setup
            return
        
        if not os.path.exists(source_folder):
            QMessageBox.warning(self, "Path Error", 
                              f"Source folder does not exist:\n{source_folder}")
            self.switch_callback("setup")  # Go back to setup
            return

        # Display configuration summary
        self.display_configuration_summary()
        
        # Reset UI for new analysis
        self.log.clear()
        self.progress.setValue(0)
        self.view_results_btn.setVisible(False)
        self.stop_btn.setVisible(True)
        self.files_processed = 0
        self.suspicious_files = 0
        
        # Log initial configuration
        self.log.appendPlainText("="*60)
        self.log.appendPlainText("🔍 DIGITAL FORENSIC ANALYSIS STARTED")
        self.log.appendPlainText("="*60)
        self.log.appendPlainText(f"⏰ Start Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log.appendPlainText(f"📁 Source: {source_folder}")
        self.log.appendPlainText(f"💾 Destination: {dest_folder}")
        self.log.appendPlainText(f"🛡️  Security Level: {self.session_state.get('security_level', 'Standard')}")
        
        # Log file type configuration
        selected_extensions = self.session_state.get("selected_extensions", [])
        if selected_extensions:
            self.log.appendPlainText(f"📋 File Types ({len(selected_extensions)}): {', '.join(selected_extensions[:10])}")
            if len(selected_extensions) > 10:
                self.log.appendPlainText(f"    ... and {len(selected_extensions) - 10} more")
        else:
            self.log.appendPlainText("📋 File Types: All files")
        
        # Log keyword configuration
        if self.session_state.get("use_custom_keywords", False):
            custom_file = self.session_state.get("custom_keyword_file", "")
            self.log.appendPlainText(f"🔎 Keywords: Custom file - {os.path.basename(custom_file) if custom_file else 'Unknown'}")
        else:
            self.log.appendPlainText("🔎 Keywords: Built-in security database (2500+ terms)")
        
        # Log additional options
        options_enabled = []
        if self.session_state.get("copy_suspicious", False):
            options_enabled.append("Copy suspicious files")
        if self.session_state.get("real_time_monitoring", False):
            options_enabled.append("Real-time monitoring")
        
        if options_enabled:
            self.log.appendPlainText(f"⚙️  Options: {', '.join(options_enabled)}")
        
        self.log.appendPlainText("-"*60)
        self.log.appendPlainText("🚀 Initializing analysis engine...")
        
        # Start timing
        self.start_time = pd.Timestamp.now()
        self.timer.start(1000)  # Update every second
        
        # Create analysis configuration for the worker
        analysis_config = {
            "source_folder": source_folder,
            "dest_folder": dest_folder,
            "security_level": self.session_state.get("security_level", "Standard Scan"),
            "selected_extensions": selected_extensions,
            "use_custom_keywords": self.session_state.get("use_custom_keywords", False),
            "custom_keyword_file": self.session_state.get("custom_keyword_file"),
            "copy_suspicious": self.session_state.get("copy_suspicious", False),
            "real_time_monitoring": self.session_state.get("real_time_monitoring", False)
        }
        
        # Start the worker thread with the configuration
        self.worker = AnalysisWorker(analysis_config)
        self.worker.log_update.connect(self.append_log)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.task_update.connect(self.update_current_task)
        self.worker.stats_update.connect(self.update_statistics)
        self.worker.finished_signal.connect(self.on_analysis_finished)
        self.worker.error_signal.connect(self.on_analysis_error)
        
        self.worker.start()
        self.current_task_label.setText("🔍 Scanning directory structure...")

    def stop_analysis(self):
        """Stop the currently running analysis"""
        if self.worker and self.worker.isRunning():
            self.log.appendPlainText("\n⏹️  Stopping analysis - please wait...")
            self.current_task_label.setText("🛑 Stopping analysis...")
            self.worker.stop()
            self.worker.wait()  # Wait for thread to finish
            
            self.log.appendPlainText("✋ Analysis stopped by user")
            self.current_task_label.setText("❌ Analysis stopped")
            self.stop_btn.setVisible(False)
            self.view_results_btn.setText("🔙 Back to Setup")
            self.view_results_btn.clicked.disconnect()
            self.view_results_btn.clicked.connect(lambda: self.switch_callback("setup"))
            self.view_results_btn.setVisible(True)
            
        self.timer.stop()

    def append_log(self, text):
        """Append text to the log display"""
        self.log.appendPlainText(text)
        # Auto-scroll to bottom
        scrollbar = self.log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def update_progress(self, percentage):
        """Update the progress bar"""
        self.progress.setValue(int(percentage))

    def update_current_task(self, task_description):
        """Update the current task label"""
        self.current_task_label.setText(task_description)

    def update_statistics(self, stats):
        """Update the statistics display"""
        self.files_processed = stats.get("files_processed", 0)
        self.suspicious_files = stats.get("suspicious_found", 0)
        
        self.files_processed_label.setText(f"Files: {self.files_processed}")
        self.suspicious_found_label.setText(f"Suspicious: {self.suspicious_files}")

    def update_elapsed_time(self):
        """Update the elapsed time display"""
        if self.start_time:
            elapsed = pd.Timestamp.now() - self.start_time
            total_seconds = int(elapsed.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            self.time_elapsed_label.setText(f"Time: {minutes:02d}:{seconds:02d}")

    def on_analysis_finished(self, results):
        """Handle successful completion of analysis"""
        self.timer.stop()
        
        if results is None or results.empty:
            self.log.appendPlainText("\n⚠️  Analysis completed but no results were generated")
            self.current_task_label.setText("⚠️  No results generated")
        else:
            self.session_state["analysis_results"] = results
            self.log.appendPlainText(f"\n✅ Analysis completed successfully!")
            self.log.appendPlainText(f"📊 Total files processed: {self.files_processed}")
            self.log.appendPlainText(f"🚨 Suspicious files found: {self.suspicious_files}")
            self.log.appendPlainText(f"⏱️  Total time: {self.time_elapsed_label.text().replace('Time: ', '')}")
            self.log.appendPlainText("="*60)
            
            self.current_task_label.setText("✅ Analysis completed successfully")
            
            # Show completion message
            QMessageBox.information(
                self, 
                "Analysis Complete", 
                f"Forensic analysis completed successfully!\n\n"
                f"Files processed: {self.files_processed}\n"
                f"Suspicious files found: {self.suspicious_files}\n"
                f"Time elapsed: {self.time_elapsed_label.text().replace('Time: ', '')}"
            )
        
        # Update buttons
        self.stop_btn.setVisible(False)
        self.view_results_btn.setVisible(True)
        self.view_results_btn.setText("📊 View Results")
        
        # Reconnect the results button to go to final page
        self.view_results_btn.clicked.disconnect()
        self.view_results_btn.clicked.connect(lambda: self.switch_callback("final"))

    def on_analysis_error(self, error_message):
        """Handle analysis errors"""
        self.timer.stop()
        
        self.log.appendPlainText(f"\n❌ Analysis failed: {error_message}")
        self.current_task_label.setText("❌ Analysis failed")
        
        QMessageBox.critical(
            self, 
            "Analysis Error", 
            f"Analysis failed with error:\n\n{error_message}\n\nCheck the logs for more details."
        )
        
        # Update buttons
        self.stop_btn.setVisible(False)
        self.view_results_btn.setText("🔙 Back to Setup")
        self.view_results_btn.clicked.disconnect()
        self.view_results_btn.clicked.connect(lambda: self.switch_callback("setup"))
        self.view_results_btn.setVisible(True)