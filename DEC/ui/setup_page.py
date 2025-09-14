from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QRadioButton, QPushButton, QFileDialog, QGroupBox, QScrollArea,
    QApplication, QStyleFactory, QFrame, QLineEdit, QSpacerItem,
    QSizePolicy, QButtonGroup, QGridLayout, QProgressBar, QToolTip,
    QGraphicsDropShadowEffect, QStackedWidget
)
from PyQt5.QtCore import (Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, 
                         QTimer, QRect, QParallelAnimationGroup)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QPainter

# A single, consistent color palette for the application
DARK_THEME_PALETTE = {
    # Core background and text colors
    "background_dark": "#000000",    # A very dark background
    "background_card": "#000000",    # Slightly lighter for cards/containers
    "text_primary": "#e0e0e0",       # Light gray for main text
    "text_secondary": "#a0a0a0",      # Muted gray for descriptions
    
    # Accent colors
    "accent_blue": "#2196f3",        # A vibrant but not overpowering blue for primary actions
    "accent_blue_hover": "#1e88e5",
    "accent_blue_pressed": "#1565c0",
    
    # Status and feedback colors
    "status_success": "#4caf50",     # Green for success
    "status_warning": "#ff9800",     # Orange for warnings
    "status_error": "#f44336",       # Red for errors
    "status_info": "#2196f3",        # Blue for info
    
    # Border and shadow colors
    "border_color": "#303030",       # Dark gray for borders
    "shadow_color": QColor(0, 0, 0, 100), # Slightly stronger shadow
}

class AnimatedToggle(QCheckBox):
    """Custom animated toggle switch with dark theme"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QCheckBox::indicator {{
                width: 50px;
                height: 24px;
                border-radius: 12px;
                background-color: {DARK_THEME_PALETTE['border_color']};
                border: 2px solid {DARK_THEME_PALETTE['border_color']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {DARK_THEME_PALETTE['accent_blue']};
                border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: {DARK_THEME_PALETTE['accent_blue_hover']};
            }}
            QCheckBox::indicator:hover {{
                border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
            }}
        """)

class ModernCard(QFrame):
    """Modern card widget with dark theme shadow effect"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            ModernCard {{
                background-color: {DARK_THEME_PALETTE['background_card']};
                border: 1px solid {DARK_THEME_PALETTE['border_color']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(DARK_THEME_PALETTE['shadow_color'])
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

class ModernButton(QPushButton):
    """Modern styled button with dark theme hover effects"""
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setMinimumHeight(44)
        self.setFont(QFont("Segoe UI", 10, QFont.Medium))
        self.setCursor(Qt.PointingHandCursor)
        self.apply_style()

    def apply_style(self):
        if self.button_type == "primary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {DARK_THEME_PALETTE['accent_blue']};
                    color: {DARK_THEME_PALETTE['text_primary']};
                    border: none;
                    border-radius: 10px;
                    padding: 12px 28px;
                    font-weight: 600;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {DARK_THEME_PALETTE['accent_blue_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {DARK_THEME_PALETTE['accent_blue_pressed']};
                }}
                QPushButton:disabled {{
                    background-color: {DARK_THEME_PALETTE['border_color']};
                    color: {DARK_THEME_PALETTE['text_secondary']};
                }}
            """)
        elif self.button_type == "secondary":
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {DARK_THEME_PALETTE['background_card']};
                    color: {DARK_THEME_PALETTE['text_primary']};
                    border: 1px solid {DARK_THEME_PALETTE['border_color']};
                    border-radius: 10px;
                    padding: 12px 28px;
                    font-weight: 600;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {DARK_THEME_PALETTE['border_color']};
                    border-color: {DARK_THEME_PALETTE['accent_blue']};
                }}
                QPushButton:pressed {{
                    background-color: {DARK_THEME_PALETTE['border_color']};
                }}
            """)
        else:  # ghost/text button
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {DARK_THEME_PALETTE['accent_blue']};
                    border: none;
                    border-radius: 10px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: {DARK_THEME_PALETTE['border_color']};
                }}
                QPushButton:pressed {{
                    background-color: {DARK_THEME_PALETTE['background_card']};
                }}
            """)

class StepIndicator(QWidget):
    """Dark themed step indicator showing current progress"""
    def __init__(self, total_steps=4, parent=None):
        super().__init__(parent)
        self.total_steps = total_steps
        self.current_step = 0
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.step_widgets = []
        step_names = ["Setup", "Analysis Options", "File Selection", "Keywords"]

        for i in range(self.total_steps):
            step_container = QVBoxLayout()
            step_container.setSpacing(6)

            # Step circle
            step_circle = QLabel(str(i + 1))
            step_circle.setAlignment(Qt.AlignCenter)
            step_circle.setFixedSize(36, 36)
            step_circle.setStyleSheet(f"""
                QLabel {{
                    background-color: {DARK_THEME_PALETTE['border_color']};
                    color: {DARK_THEME_PALETTE['text_secondary']};
                    border-radius: 18px;
                    font-weight: bold;
                    font-size: 13px;
                    border: 2px solid {DARK_THEME_PALETTE['border_color']};
                }}
            """)

            # Step name
            step_name = QLabel(step_names[i])
            step_name.setAlignment(Qt.AlignCenter)
            step_name.setFont(QFont("Segoe UI", 9))
            step_name.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']};")

            step_container.addWidget(step_circle)
            step_container.addWidget(step_name)
            
            step_widget = QWidget()
            step_widget.setLayout(step_container)
            
            self.step_widgets.append((step_circle, step_name))
            layout.addWidget(step_widget)

            # Add connector line (except for last step)
            if i < self.total_steps - 1:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                # The problematic line
                # line.setStyleSheet("color: black; margin-top: 18px;") 
                
                # The corrected line, using a specified background color
                line.setStyleSheet(f"background-color: {DARK_THEME_PALETTE['border_color']}; border: none; height: 1px;")
                line.setFixedHeight(2)
                layout.addWidget(line)
        self.update_step(0)

    def update_step(self, step):
        self.current_step = step
        for i, (circle, name) in enumerate(self.step_widgets):
            if i == step:
                # Current step
                circle.setStyleSheet(f"""
                    QLabel {{
                        background-color: {DARK_THEME_PALETTE['accent_blue']};
                        color: white;
                        border-radius: 18px;
                        font-weight: bold;
                        font-size: 13px;
                        border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
                    }}
                """)
                name.setStyleSheet(f"color: {DARK_THEME_PALETTE['accent_blue']}; font-weight: bold;")
            elif i < step:
                # Completed step
                circle.setText("✓")
                circle.setStyleSheet(f"""
                    QLabel {{
                        background-color: {DARK_THEME_PALETTE['status_success']};
                        color: white;
                        border-radius: 18px;
                        font-weight: bold;
                        font-size: 13px;
                        border: 2px solid {DARK_THEME_PALETTE['status_success']};
                    }}
                """)
                name.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; font-weight: bold;")
            else:
                # Future step
                circle.setText(str(i + 1))
                circle.setStyleSheet(f"""
                    QLabel {{
                        background-color: {DARK_THEME_PALETTE['border_color']};
                        color: {DARK_THEME_PALETTE['text_secondary']};
                        border-radius: 18px;
                        font-weight: bold;
                        font-size: 13px;
                        border: 2px solid {DARK_THEME_PALETTE['border_color']};
                    }}
                """)
                name.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']};")

class SetupStep(QWidget):
    """Step 0: Initial Setup - Directory Selection with dark theme"""
    analysis_complete = pyqtSignal()
    
    def __init__(self, session_state, parent=None):
        super().__init__(parent)
        self.session_state = session_state
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        # Main setup card
        setup_card = ModernCard()
        setup_layout = QVBoxLayout(setup_card)
        setup_layout.setSpacing(20)

        # Header (no icon now)
        title_layout = QVBoxLayout()
        section_title = QLabel("🔧 Initial Setup")
        section_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        section_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        
        section_desc = QLabel("Select source and destination folders for your forensic analysis")
        section_desc.setFont(QFont("Segoe UI", 11))
        section_desc.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 6px;")
        
        title_layout.addWidget(section_title)
        title_layout.addWidget(section_desc)
        setup_layout.addLayout(title_layout)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {DARK_THEME_PALETTE['border_color']}; border: none; height: 1px;")
        setup_layout.addWidget(sep)

        # Source folder section
        source_layout = QHBoxLayout()
        
        source_info_layout = QVBoxLayout()
        source_title = QLabel("📂 Source Folder")
        source_title.setFont(QFont("Segoe UI", 13, QFont.Medium))
        source_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        
        self.source_label = QLabel("No folder selected")
        self.source_label.setFont(QFont("Segoe UI", 11))
        self.source_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 4px;")
        
        source_info_layout.addWidget(source_title)
        source_info_layout.addWidget(self.source_label)
        source_layout.addLayout(source_info_layout)
        
        source_layout.addStretch()
        
        self.source_btn = ModernButton("Browse", "secondary")
        self.source_btn.clicked.connect(self.browse_source_folder)
        source_layout.addWidget(self.source_btn)
        
        setup_layout.addLayout(source_layout)

        # Destination folder section
        dest_layout = QHBoxLayout()
        
        dest_info_layout = QVBoxLayout()
        dest_title = QLabel("💾 Destination Folder")
        dest_title.setFont(QFont("Segoe UI", 13, QFont.Medium))
        dest_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        
        self.dest_label = QLabel("No folder selected")
        self.dest_label.setFont(QFont("Segoe UI", 11))
        self.dest_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 4px;")
        
        dest_info_layout.addWidget(dest_title)
        dest_info_layout.addWidget(self.dest_label)
        dest_layout.addLayout(dest_info_layout)
        
        dest_layout.addStretch()
        
        self.dest_btn = ModernButton("Browse", "secondary")
        self.dest_btn.clicked.connect(self.browse_dest_folder)
        dest_layout.addWidget(self.dest_btn)
        
        setup_layout.addLayout(dest_layout)

        layout.addWidget(setup_card)
        layout.addStretch()


    def browse_source_folder(self):
        """Browse for source folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Source Folder")
        if folder:
            self.source_label.setText(f"✓ {folder}")
            self.source_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; margin-top: 4px;")
            self.session_state["source_folder"] = folder
            self.check_completion()

    def browse_dest_folder(self):
        """Browse for destination folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.dest_label.setText(f"✓ {folder}")
            self.dest_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; margin-top: 4px;")
            self.session_state["dest_folder"] = folder
            self.check_completion()

    def check_completion(self):
        """Check if setup is complete and emit signal"""
        if ("source_folder" in self.session_state and 
            "dest_folder" in self.session_state):
            self.analysis_complete.emit()

class FileTypeCard(ModernCard):
    """Dark themed card for file type selection"""
    def __init__(self, category, file_types, parent=None):
        super().__init__(parent)
        self.category = category
        self.file_types = file_types
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # Header with icon and category name
        header_layout = QHBoxLayout()
        
        # Category icon
        icon_map = {
            "Documents": "📄",
            "Images": "🖼️", 
            "Audio": "🎵",
            "Videos": "🎬",
            "Archives": "📦",
            "Executables & Scripts": "⚙️",
            "Others": "📋"
        }
        
        icon_label = QLabel(icon_map.get(self.category, "📄"))
        icon_label.setFont(QFont("Segoe UI", 18))
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(self.category)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        title_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Select all toggle
        self.select_all_toggle = AnimatedToggle()
        self.select_all_toggle.setText("Select All")
        self.select_all_toggle.setFont(QFont("Segoe UI", 10))
        self.select_all_toggle.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        self.select_all_toggle.stateChanged.connect(self.toggle_all)
        header_layout.addWidget(self.select_all_toggle)
        
        layout.addLayout(header_layout)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"background-color: {DARK_THEME_PALETTE['border_color']}; border: none; height: 1px;")
        layout.addWidget(separator)
        
        # File type checkboxes in a grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        
        self.file_checkboxes = []
        row, col = 0, 0
        for file_type in self.file_types:
            checkbox = QCheckBox(file_type)
            checkbox.setFont(QFont("Segoe UI", 10))
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {DARK_THEME_PALETTE['text_primary']};
                    spacing: 10px;
                }}
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                    border-radius: 4px;
                    border: 2px solid {DARK_THEME_PALETTE['border_color']};
                    background-color: {DARK_THEME_PALETTE['background_card']};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {DARK_THEME_PALETTE['accent_blue']};
                    border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
                }}
                QCheckBox::indicator:hover {{
                    border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
                }}
            """)
            self.file_checkboxes.append(checkbox)
            grid_layout.addWidget(checkbox, row, col)
            
            col += 1
            if col > 2:  # 3 columns max
                col = 0
                row += 1
        
        layout.addLayout(grid_layout)

    def toggle_all(self, state):
        for checkbox in self.file_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

    def get_selected_types(self):
        return [cb.text() for cb in self.file_checkboxes if cb.isChecked()]

    def is_category_selected(self):
        return any(cb.isChecked() for cb in self.file_checkboxes)

class AnalysisOptionsStep(QWidget):
    """Dark themed Step 1: Analysis Options"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        # Main options card
        options_card = ModernCard()
        options_layout = QVBoxLayout(options_card)
        options_layout.setSpacing(28)

        # Security Level Section
        security_section = QVBoxLayout()
        security_title = QLabel("🛡️ Security Level")
        security_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        security_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']}; margin-bottom: 10px;")
        security_section.addWidget(security_title)

        # Security options
        self.security_group = QButtonGroup()
        security_options = [
            ("Quick Scan", "Fast analysis focusing on high-risk areas", False),
            ("Standard Scan", "Balanced approach with comprehensive coverage", True),
            ("Deep Scan", "Thorough analysis including all file contents", False)
        ]

        for i, (title, desc, default) in enumerate(security_options):
            option_layout = QHBoxLayout()
            
            radio = QRadioButton(title)
            radio.setFont(QFont("Segoe UI", 12, QFont.Medium))
            radio.setStyleSheet(f"""
                QRadioButton {{
                    color: {DARK_THEME_PALETTE['text_primary']};
                    spacing: 8px;
                }}
                QRadioButton::indicator {{
                    width: 18px;
                    height: 18px;
                    border-radius: 9px;
                    border: 2px solid {DARK_THEME_PALETTE['border_color']};
                    background-color: {DARK_THEME_PALETTE['background_card']};
                }}
                QRadioButton::indicator:checked {{
                    background-color: {DARK_THEME_PALETTE['accent_blue']};
                    border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
                }}
                QRadioButton::indicator:hover {{
                    border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
                }}
            """)
            radio.setChecked(default)
            self.security_group.addButton(radio, i)
            
            option_info = QVBoxLayout()
            option_info.addWidget(radio)
            
            desc_label = QLabel(desc)
            desc_label.setFont(QFont("Segoe UI", 10))
            desc_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-left: 24px;")
            option_info.addWidget(desc_label)
            
            option_layout.addLayout(option_info)
            option_layout.addStretch()
            
            security_section.addLayout(option_layout)

        options_layout.addLayout(security_section)

        # Separator
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setStyleSheet(f"background-color: {DARK_THEME_PALETTE['border_color']}; border: none; height: 1px;")
        options_layout.addWidget(sep1)

        # Advanced Options Section
        advanced_section = QVBoxLayout()
        advanced_title = QLabel("⚙️ Advanced Options")
        advanced_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        advanced_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']}; margin-bottom: 14px;")
        advanced_section.addWidget(advanced_title)

        # Copy files option
        copy_layout = QHBoxLayout()
        copy_info_layout = QVBoxLayout()
        
        copy_title = QLabel("Create secure copies of suspicious files")
        copy_title.setFont(QFont("Segoe UI", 12, QFont.Medium))
        copy_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        
        copy_desc = QLabel("Automatically backup files that match security criteria for further analysis")
        copy_desc.setFont(QFont("Segoe UI", 10))
        copy_desc.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 4px;")
        
        copy_info_layout.addWidget(copy_title)
        copy_info_layout.addWidget(copy_desc)
        copy_layout.addLayout(copy_info_layout)
        copy_layout.addStretch()
        
        self.copy_toggle = AnimatedToggle()
        self.copy_toggle.setChecked(True)
        copy_layout.addWidget(self.copy_toggle)
        
        advanced_section.addLayout(copy_layout)

        # Real-time monitoring option
        monitor_layout = QHBoxLayout()
        monitor_info_layout = QVBoxLayout()
        
        monitor_title = QLabel("Enable real-time monitoring during scan")
        monitor_title.setFont(QFont("Segoe UI", 12, QFont.Medium))
        monitor_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        
        monitor_desc = QLabel("Monitor file system changes while analysis is running")
        monitor_desc.setFont(QFont("Segoe UI", 10))
        monitor_desc.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 4px;")
        
        monitor_info_layout.addWidget(monitor_title)
        monitor_info_layout.addWidget(monitor_desc)
        monitor_layout.addLayout(monitor_info_layout)
        monitor_layout.addStretch()
        
        self.monitor_toggle = AnimatedToggle()
        self.monitor_toggle.setChecked(False)
        monitor_layout.addWidget(self.monitor_toggle)
        
        advanced_section.addLayout(monitor_layout)

        options_layout.addLayout(advanced_section)
        layout.addWidget(options_card)
        layout.addStretch()

class FileSelectionStep(QWidget):
    """Dark themed Step 2: File Type Selection"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_type_cards = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Quick actions header
        header_card = ModernCard()
        header_layout = QHBoxLayout(header_card)
        
        info_layout = QVBoxLayout()
        info_title = QLabel("🔍 File Type Selection")
        info_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        info_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        
        info_desc = QLabel("Choose which file types to include in your security analysis")
        info_desc.setFont(QFont("Segoe UI", 11))
        info_desc.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 6px;")
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(info_desc)
        header_layout.addLayout(info_layout)
        
        header_layout.addStretch()
        
        # Quick select buttons
        quick_layout = QVBoxLayout()
        select_all_btn = ModernButton("Select All", "ghost")
        select_all_btn.clicked.connect(self.select_all_categories)
        
        select_none_btn = ModernButton("Clear All", "ghost")
        select_none_btn.clicked.connect(self.select_no_categories)
        
        quick_layout.addWidget(select_all_btn)
        quick_layout.addWidget(select_none_btn)
        header_layout.addLayout(quick_layout)
        
        layout.addWidget(header_card)

        # Scrollable file type selection
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {DARK_THEME_PALETTE['background_dark']};
            }}
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet(f"background-color: {DARK_THEME_PALETTE['background_dark']};")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # File type categories
        categories = {
            "Documents": [".docx", ".doc", ".pdf", ".txt", ".odt", ".rtf", ".csv", ".xlsx", ".pptx"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma"],
            "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".dmg"],
            "Executables & Scripts": [".exe", ".bat", ".sh", ".py", ".msi", ".app", ".deb", ".rpm"],
            "Others": [".log", ".tmp", ".bak", ".cfg", ".ini", ".dll", ".sys"]
        }

        pre_selected = ["Documents", "Executables & Scripts"]

        for category, file_types in categories.items():
            card = FileTypeCard(category, file_types)
            if category in pre_selected:
                card.select_all_toggle.setChecked(True)
            self.file_type_cards.append(card)
            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

    def select_all_categories(self):
        for card in self.file_type_cards:
            card.select_all_toggle.setChecked(True)

    def select_no_categories(self):
        for card in self.file_type_cards:
            card.select_all_toggle.setChecked(False)

    def get_selected_extensions(self):
        selected_extensions = []
        for card in self.file_type_cards:
            selected_extensions.extend(card.get_selected_types())
        return selected_extensions

    def has_selections(self):
        return any(card.is_category_selected() for card in self.file_type_cards)

class KeywordsStep(QWidget):
    """Dark themed Step 3: Keywords Configuration"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        # Keywords configuration card
        keywords_card = ModernCard()
        keywords_layout = QVBoxLayout(keywords_card)
        keywords_layout.setSpacing(28)

        # Header
        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        
        section_title = QLabel("🔎 Keyword Detection")
        section_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        section_title.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_primary']};")
        
        section_desc = QLabel("Configure how the system detects suspicious content")
        section_desc.setFont(QFont("Segoe UI", 11))
        section_desc.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 6px;")
        
        title_layout.addWidget(section_title)
        title_layout.addWidget(section_desc)
        header_layout.addLayout(title_layout)
        keywords_layout.addLayout(header_layout)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {DARK_THEME_PALETTE['border_color']}; border: none; height: 1px;")
        keywords_layout.addWidget(sep)

        # Radio button group
        self.keywords_group = QButtonGroup()
        
        # Default keywords option
        default_layout = QHBoxLayout()
        default_icon = QLabel("🛡️")
        default_icon.setFont(QFont("Segoe UI", 18))
        default_layout.addWidget(default_icon)
        
        default_info_layout = QVBoxLayout()
        self.default_radio = QRadioButton("Use built-in security keywords")
        self.default_radio.setFont(QFont("Segoe UI", 13, QFont.Medium))
        self.default_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {DARK_THEME_PALETTE['text_primary']};
                spacing: 8px;
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid {DARK_THEME_PALETTE['border_color']};
                background-color: {DARK_THEME_PALETTE['background_card']};
            }}
            QRadioButton::indicator:checked {{
                background-color: {DARK_THEME_PALETTE['accent_blue']};
                border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
            }}
            QRadioButton::indicator:hover {{
                border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
            }}
        """)
        self.default_radio.setChecked(True)
        
        default_desc = QLabel("Comprehensive database of 2,500+ security-related terms, threat indicators, and malware signatures")
        default_desc.setFont(QFont("Segoe UI", 11))
        default_desc.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-left: 24px; margin-top: 6px;")
        default_desc.setWordWrap(True)
        
        # Built-in categories preview
        categories_label = QLabel("Includes: Malware signatures, suspicious commands, credential patterns, network indicators")
        categories_label.setFont(QFont("Segoe UI", 10))
        categories_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['accent_blue']}; margin-left: 24px; margin-top: 10px; font-style: italic;")
        categories_label.setWordWrap(True)
        
        default_info_layout.addWidget(self.default_radio)
        default_info_layout.addWidget(default_desc)
        default_info_layout.addWidget(categories_label)
        default_layout.addLayout(default_info_layout)
        
        keywords_layout.addLayout(default_layout)
        keywords_layout.addSpacing(20)
        
        # Custom keywords option
        custom_layout = QHBoxLayout()
        custom_icon = QLabel("📝")
        custom_icon.setFont(QFont("Segoe UI", 18))
        custom_layout.addWidget(custom_icon)
        
        custom_info_layout = QVBoxLayout()
        self.custom_radio = QRadioButton("Use custom keyword file")
        self.custom_radio.setFont(QFont("Segoe UI", 13, QFont.Medium))
        self.custom_radio.setStyleSheet(f"""
            QRadioButton {{
                color: {DARK_THEME_PALETTE['text_primary']};
                spacing: 8px;
            }}
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid {DARK_THEME_PALETTE['border_color']};
                background-color: {DARK_THEME_PALETTE['background_card']};
            }}
            QRadioButton::indicator:checked {{
                background-color: {DARK_THEME_PALETTE['accent_blue']};
                border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
            }}
            QRadioButton::indicator:hover {{
                border: 2px solid {DARK_THEME_PALETTE['accent_blue']};
            }}
        """)
        
        custom_desc = QLabel("Load your own keyword list from a text file (one keyword per line)")
        custom_desc.setFont(QFont("Segoe UI", 11))
        custom_desc.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-left: 24px; margin-top: 6px;")
        custom_desc.setWordWrap(True)
        
        custom_info_layout.addWidget(self.custom_radio)
        custom_info_layout.addWidget(custom_desc)
        custom_layout.addLayout(custom_info_layout)
        
        custom_layout.addStretch()
        
        # Browse button and file info
        file_section = QVBoxLayout()
        self.browse_btn = ModernButton("Browse Files", "secondary")
        self.browse_btn.clicked.connect(self.browse_keyword_file)
        self.browse_btn.setEnabled(False)
        file_section.addWidget(self.browse_btn)
        
        # File path display
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setFont(QFont("Segoe UI", 10))
        self.file_path_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-top: 6px;")
        self.file_path_label.setWordWrap(True)
        file_section.addWidget(self.file_path_label)
        
        custom_layout.addLayout(file_section)
        keywords_layout.addLayout(custom_layout)

        # Connect radio buttons
        self.keywords_group.addButton(self.default_radio, 0)
        self.keywords_group.addButton(self.custom_radio, 1)
        self.custom_radio.toggled.connect(lambda checked: self.browse_btn.setEnabled(checked))
        
        layout.addWidget(keywords_card)
        layout.addStretch()

    def browse_keyword_file(self):
        """Browse for custom keyword file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Keyword File", 
            "", 
            "Text Files (*.txt);;All Files (*.*)"
        )
        if file_path:
            self.file_path_label.setText(f"✓ Selected: {file_path.split('/')[-1]}")
            self.file_path_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; margin-top: 6px;")
            return file_path
        return None

class SetupPage(QWidget):
    """Main setup page with dark theme multi-step wizard"""
    
    def __init__(self, switch_to, session_state):
        super().__init__(parent=None)
        self.switch_to = switch_to
        self.session_state = session_state
        self.current_step = 0
        self.total_steps = 4  # Setup, Analysis Options, File Selection, Keywords
        self.setup_completed = False
        self.init_ui()

    def init_ui(self):
        # Set dark theme overall app style
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_THEME_PALETTE['background_dark']};
                color: {DARK_THEME_PALETTE['text_primary']};
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {DARK_THEME_PALETTE['border_color']};
                width: 10px;
                border-radius: 50px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {DARK_THEME_PALETTE['text_secondary']};
                border-radius: 5px;
                min-height: 25px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {DARK_THEME_PALETTE['accent_blue']};
            }}
            QScrollBar::handle:vertical:pressed {{
                background-color: {DARK_THEME_PALETTE['accent_blue_pressed']};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(36, 28, 36, 28)
        main_layout.setSpacing(28)

        # Fixed header section
        self.create_header(main_layout)
        
        # Step indicator
        self.step_indicator = StepIndicator(self.total_steps)
        main_layout.addWidget(self.step_indicator)
        
        # Stacked widget for steps
        self.stacked_widget = QStackedWidget()
        
        # Create step widgets
        self.setup_step = SetupStep(self.session_state)
        self.setup_step.analysis_complete.connect(self.on_setup_complete)
        
        self.analysis_step = AnalysisOptionsStep()
        self.file_step = FileSelectionStep()
        self.keywords_step = KeywordsStep()
        
        self.stacked_widget.addWidget(self.setup_step)
        self.stacked_widget.addWidget(self.analysis_step)
        self.stacked_widget.addWidget(self.file_step)
        self.stacked_widget.addWidget(self.keywords_step)
        
        main_layout.addWidget(self.stacked_widget)
        
        # Footer with navigation
        self.create_footer(main_layout)

    def on_setup_complete(self):
        """Handle setup completion and auto-advance to next step"""
        self.setup_completed = True
        QTimer.singleShot(500, self.next_step)  # Small delay for UX

    def create_header(self, layout):
        """Create fixed header section with dark theme"""
        header_card = ModernCard()
        header_layout = QVBoxLayout(header_card)
        
        # Main title
        title = QLabel("Security Analysis Wizard")
        title.setFont(QFont("Segoe UI", 32, QFont.Light))
        title.setStyleSheet(f"color: blue; margin-bottom: 8px;")
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Complete setup and configure your forensic analysis settings")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; margin-bottom: 16px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_card)

    def create_footer(self, layout):
        """Create footer with navigation buttons"""
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 20, 0, 0)
        
        # Back button
        self.back_btn = ModernButton("← Previous", "secondary")
        self.back_btn.clicked.connect(self.previous_step)
        self.back_btn.setVisible(False)  # Hidden on first step
        footer_layout.addWidget(self.back_btn)
        
        footer_layout.addStretch()
        
        # Status and validation
        self.status_container = QHBoxLayout()
        self.status_container.setSpacing(14)
        
        self.status_label = QLabel("Select source and destination folders to begin")
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']};")
        
        self.status_container.addWidget(self.status_label)
        footer_layout.addLayout(self.status_container)
        
        # Next/Finish button
        self.next_btn = ModernButton("Next →", "primary")
        self.next_btn.clicked.connect(self.next_step)
        self.next_btn.setVisible(False)  # Hidden during setup step
        footer_layout.addWidget(self.next_btn)
        
        layout.addLayout(footer_layout)

    def animate_step_transition(self, direction="next"):
        """Animate transition between steps"""
        if direction == "next" and self.current_step < self.total_steps - 1:
            self.current_step += 1
        elif direction == "prev" and self.current_step > 0:
            self.current_step -= 1
        
        # Update step indicator
        self.step_indicator.update_step(self.current_step)
        
        # Animate to new step
        self.stacked_widget.setCurrentIndex(self.current_step)
        
        # Update navigation buttons
        self.update_navigation_state()

    def update_navigation_state(self):
        """Update navigation button states based on current step"""
        # Back button visibility (not shown on setup step)
        self.back_btn.setVisible(self.current_step > 0 and self.setup_completed)
        
        # Next button visibility and text
        if self.current_step == 0:  # Setup step
            self.next_btn.setVisible(False)  # Setup handles its own progression
        else:
            self.next_btn.setVisible(True)
            if self.current_step == self.total_steps - 1:
                self.next_btn.setText("Start Analysis →")
                self.next_btn.button_type = "primary"
                self.next_btn.apply_style()
            else:
                self.next_btn.setText("Next →")
                self.next_btn.button_type = "primary"
                self.next_btn.apply_style()
        
        # Update status based on current step
        self.update_step_status()

    def update_step_status(self):
        """Update status message based on current step validation"""
        if self.current_step == 0:  # Setup step
            self.status_label.setText("Select source and destination folders to begin")
            self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; font-size: 11pt;")
            
        elif self.current_step == 1:  # Analysis Options
            self.status_label.setText("Configure your analysis options to continue")
            self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['text_secondary']}; font-size: 11pt;")
            self.next_btn.setEnabled(True)
            
        elif self.current_step == 2:  # File Selection
            if self.file_step.has_selections():
                selected_count = len(self.file_step.get_selected_extensions())
                self.status_label.setText(f"✓ {selected_count} file types selected")
                self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; font-size: 11pt;")
                self.next_btn.setEnabled(True)
            else:
                self.status_label.setText("⚠️ Please select at least one file type")
                self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_warning']}; font-size: 11pt;")
                self.next_btn.setEnabled(False)
                
        elif self.current_step == 3:  # Keywords
            if self.keywords_step.custom_radio.isChecked():
                if hasattr(self, 'custom_keyword_file') and self.custom_keyword_file:
                    self.status_label.setText("✓ Custom keyword file selected")
                    self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; font-size: 11pt;")
                    self.next_btn.setEnabled(True)
                else:
                    self.status_label.setText("⚠️ Please select a keyword file")
                    self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_warning']}; font-size: 11pt;")
                    self.next_btn.setEnabled(False)
            else:
                self.status_label.setText("✓ Ready to start analysis")
                self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; font-size: 11pt;")
                self.next_btn.setEnabled(True)

    def previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.animate_step_transition("prev")

    def next_step(self):
        """Go to next step or finish"""
        if self.current_step < self.total_steps - 1:
            # Validate current step before proceeding
            if self.validate_current_step():
                self.animate_step_transition("next")
        else:
            # Final step - save and continue
            self.save_and_finish()

    def validate_current_step(self):
        """Validate current step requirements"""
        if self.current_step == 2:  # File Selection
            if not self.file_step.has_selections():
                self.show_validation_error("Please select at least one file type to analyze.")
                return False
        elif self.current_step == 3:  # Keywords
            if self.keywords_step.custom_radio.isChecked():
                if not hasattr(self, 'custom_keyword_file') or not self.custom_keyword_file:
                    self.show_validation_error("Please select a custom keyword file or use built-in keywords.")
                    return False
        return True

    def show_validation_error(self, message):
        """Show validation error message"""
        self.status_label.setText(f"⚠️ {message}")
        self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_error']}; font-size: 11pt;")
        
        # Flash effect for attention
        QTimer.singleShot(100, lambda: self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_error']}; font-size: 11pt; background-color: #3b2828; padding: 6px; border-radius: 6px;"))
        QTimer.singleShot(2000, lambda: self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_error']}; font-size: 11pt;"))

    def save_and_finish(self):
        """Save all settings and proceed to analysis"""
        # Save analysis options
        security_level = self.analysis_step.security_group.checkedId()
        security_names = ["Quick Scan", "Standard Scan", "Deep Scan"]
        
        self.session_state.update({
            "security_level": security_names[security_level] if security_level >= 0 else "Standard Scan",
            "copy_suspicious": self.analysis_step.copy_toggle.isChecked(),
            "real_time_monitoring": self.analysis_step.monitor_toggle.isChecked(),
            
            # File selection
            "selected_extensions": self.file_step.get_selected_extensions(),
            
            # Keywords
            "use_default_keywords": self.keywords_step.default_radio.isChecked(),
            "use_custom_keywords": self.keywords_step.custom_radio.isChecked(),
        })
        
        if hasattr(self, 'custom_keyword_file'):
            self.session_state["custom_keyword_file"] = self.custom_keyword_file
        
        # Show completion feedback
        self.next_btn.setText("Launching Analysis...")
        self.next_btn.setEnabled(False)
        self.status_label.setText("✅ Configuration complete - Starting forensic analysis...")
        self.status_label.setStyleSheet(f"color: {DARK_THEME_PALETTE['status_success']}; font-size: 11pt;")
        
        print("Complete Configuration:", self.session_state)
        
        # Simulate processing and navigate
        QTimer.singleShot(1500, lambda: self.switch_to('processing'))

    def keyPressEvent(self, event):
        """Handle keyboard navigation"""
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Space:
            if self.next_btn.isVisible() and self.next_btn.isEnabled():
                self.next_step()
        elif event.key() == Qt.Key_Left:
            if self.back_btn.isVisible():
                self.previous_step()
        super().keyPressEvent(event)

    def showEvent(self, event):
        """Initialize validation timer when widget is shown"""
        super().showEvent(event)
        
        # Set up validation timer for real-time feedback
        self.validation_timer = QTimer()
        self.validation_timer.timeout.connect(self.update_step_status)
        self.validation_timer.start(1000)  # Check every second
        
        # Connect keyword file selection
        def on_file_selected():
            file_path = self.keywords_step.browse_keyword_file()
            if file_path:
                self.custom_keyword_file = file_path
                self.update_step_status()
        
        # Reconnect browse button (in case it was disconnected)
        try:
            self.keywords_step.browse_btn.clicked.disconnect()
        except:
            pass
        self.keywords_step.browse_btn.clicked.connect(on_file_selected)

# Example usage and testing
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    
    # Apply modern dark style
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Dark palette for the entire application
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(DARK_THEME_PALETTE['background_dark']))
    dark_palette.setColor(QPalette.WindowText, QColor(DARK_THEME_PALETTE['text_primary']))
    dark_palette.setColor(QPalette.Base, QColor(DARK_THEME_PALETTE['background_card']))
    dark_palette.setColor(QPalette.AlternateBase, QColor(DARK_THEME_PALETTE['background_card']))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(DARK_THEME_PALETTE['text_primary']))
    dark_palette.setColor(QPalette.ToolTipText, QColor(DARK_THEME_PALETTE['text_primary']))
    dark_palette.setColor(QPalette.Text, QColor(DARK_THEME_PALETTE['text_primary']))
    dark_palette.setColor(QPalette.Button, QColor(DARK_THEME_PALETTE['border_color']))
    dark_palette.setColor(QPalette.ButtonText, QColor(DARK_THEME_PALETTE['text_primary']))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Link, QColor(DARK_THEME_PALETTE['accent_blue']))
    dark_palette.setColor(QPalette.Highlight, QColor(DARK_THEME_PALETTE['accent_blue']))
    dark_palette.setColor(QPalette.HighlightedText, QColor(DARK_THEME_PALETTE['text_primary']))
    app.setPalette(dark_palette)
    
    # Set application properties
    app.setApplicationName("Forensic Security Analysis Tool")
    app.setApplicationVersion("2.0")
    
    # Test data
    session_state = {}
    switch_to = lambda page: print(f"Navigating to: {page}")
    
    # Create and show the setup page
    setup_page = SetupPage(switch_to, session_state)
    setup_page.setMinimumSize(1200, 900)
    setup_page.show()
    
    sys.exit(app.exec_())