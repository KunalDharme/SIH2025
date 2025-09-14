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

class AnimatedToggle(QCheckBox):
    """Custom animated toggle switch"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 50px;
                height: 24px;
                border-radius: 12px;
                background-color: #ddd;
                border: 2px solid #ccc;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #45a049;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #999;
            }
        """)

class ModernCard(QFrame):
    """Modern card widget with shadow effect"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            ModernCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

class ModernButton(QPushButton):
    """Modern styled button with hover effects"""
    def __init__(self, text="", button_type="primary", parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10, QFont.Medium))
        self.setCursor(Qt.PointingHandCursor)
        self.apply_style()

    def apply_style(self):
        if self.button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 24px;
                    font-weight: 600;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
                QPushButton:disabled {
                    background-color: #f3f2f1;
                    color: #a19f9d;
                }
            """)
        elif self.button_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #323130;
                    border: 2px solid #8a8886;
                    border-radius: 8px;
                    padding: 10px 24px;
                    font-weight: 600;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #f3f2f1;
                    border-color: #323130;
                }
                QPushButton:pressed {
                    background-color: #edebe9;
                }
            """)
        else:  # ghost/text button
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #0078d4;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 16px;
                    font-weight: 600;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #f3f2f1;
                }
                QPushButton:pressed {
                    background-color: #edebe9;
                }
            """)

class StepIndicator(QWidget):
    """Step indicator showing current progress"""
    def __init__(self, total_steps=3, parent=None):
        super().__init__(parent)
        self.total_steps = total_steps
        self.current_step = 0
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.step_widgets = []
        step_names = ["Analysis Options", "File Selection", "Keywords"]

        for i in range(self.total_steps):
            step_container = QVBoxLayout()
            step_container.setSpacing(4)

            # Step circle
            step_circle = QLabel(str(i + 1))
            step_circle.setAlignment(Qt.AlignCenter)
            step_circle.setFixedSize(32, 32)
            step_circle.setStyleSheet("""
                QLabel {
                    background-color: #f3f2f1;
                    color: #8a8886;
                    border-radius: 16px;
                    font-weight: bold;
                    font-size: 12px;
                }
            """)

            # Step name
            step_name = QLabel(step_names[i])
            step_name.setAlignment(Qt.AlignCenter)
            step_name.setFont(QFont("Segoe UI", 9))
            step_name.setStyleSheet("color: #8a8886;")

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
                line.setStyleSheet("color: #edebe9; margin-top: 16px;")
                line.setFixedHeight(2)
                layout.addWidget(line)

        self.update_step(0)

    def update_step(self, step):
        self.current_step = step
        for i, (circle, name) in enumerate(self.step_widgets):
            if i == step:
                # Current step
                circle.setStyleSheet("""
                    QLabel {
                        background-color: #0078d4;
                        color: white;
                        border-radius: 16px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                """)
                name.setStyleSheet("color: #0078d4; font-weight: bold;")
            elif i < step:
                # Completed step
                circle.setText("✓")
                circle.setStyleSheet("""
                    QLabel {
                        background-color: #107c10;
                        color: white;
                        border-radius: 16px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                """)
                name.setStyleSheet("color: #107c10; font-weight: bold;")
            else:
                # Future step
                circle.setText(str(i + 1))
                circle.setStyleSheet("""
                    QLabel {
                        background-color: #f3f2f1;
                        color: #8a8886;
                        border-radius: 16px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                """)
                name.setStyleSheet("color: #8a8886;")

class FileTypeCard(ModernCard):
    """Card for file type selection with better layout"""
    def __init__(self, category, file_types, parent=None):
        super().__init__(parent)
        self.category = category
        self.file_types = file_types
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

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
            "Others": "📁"
        }
        
        icon_label = QLabel(icon_map.get(self.category, "📄"))
        icon_label.setFont(QFont("Segoe UI", 16))
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(self.category)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet("color: #323130;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Select all toggle
        self.select_all_toggle = AnimatedToggle()
        self.select_all_toggle.setText("Select All")
        self.select_all_toggle.setFont(QFont("Segoe UI", 9))
        self.select_all_toggle.stateChanged.connect(self.toggle_all)
        header_layout.addWidget(self.select_all_toggle)
        
        layout.addLayout(header_layout)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #edebe9;")
        layout.addWidget(separator)
        
        # File type checkboxes in a grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)
        
        self.file_checkboxes = []
        row, col = 0, 0
        for file_type in self.file_types:
            checkbox = QCheckBox(file_type)
            checkbox.setFont(QFont("Segoe UI", 9))
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: #605e5c;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border-radius: 3px;
                    border: 2px solid #8a8886;
                }
                QCheckBox::indicator:checked {
                    background-color: #0078d4;
                    border: 2px solid #0078d4;
                }
                QCheckBox::indicator:hover {
                    border: 2px solid #0078d4;
                }
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
    """Step 1: Analysis Options"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Main options card
        options_card = ModernCard()
        options_layout = QVBoxLayout(options_card)
        options_layout.setSpacing(24)

        # Security Level Section
        security_section = QVBoxLayout()
        security_title = QLabel("🛡️ Security Level")
        security_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        security_title.setStyleSheet("color: #323130; margin-bottom: 8px;")
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
            radio.setFont(QFont("Segoe UI", 11, QFont.Medium))
            radio.setChecked(default)
            self.security_group.addButton(radio, i)
            
            option_info = QVBoxLayout()
            option_info.addWidget(radio)
            
            desc_label = QLabel(desc)
            desc_label.setFont(QFont("Segoe UI", 9))
            desc_label.setStyleSheet("color: #605e5c; margin-left: 20px;")
            option_info.addWidget(desc_label)
            
            option_layout.addLayout(option_info)
            option_layout.addStretch()
            
            security_section.addLayout(option_layout)

        options_layout.addLayout(security_section)

        # Separator
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setStyleSheet("color: #edebe9;")
        options_layout.addWidget(sep1)

        # Advanced Options Section
        advanced_section = QVBoxLayout()
        advanced_title = QLabel("⚙️ Advanced Options")
        advanced_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        advanced_title.setStyleSheet("color: #323130; margin-bottom: 12px;")
        advanced_section.addWidget(advanced_title)

        # Copy files option
        copy_layout = QHBoxLayout()
        copy_info_layout = QVBoxLayout()
        
        copy_title = QLabel("Create secure copies of suspicious files")
        copy_title.setFont(QFont("Segoe UI", 11, QFont.Medium))
        copy_title.setStyleSheet("color: #323130;")
        
        copy_desc = QLabel("Automatically backup files that match security criteria for further analysis")
        copy_desc.setFont(QFont("Segoe UI", 9))
        copy_desc.setStyleSheet("color: #605e5c; margin-top: 2px;")
        
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
        monitor_title.setFont(QFont("Segoe UI", 11, QFont.Medium))
        monitor_title.setStyleSheet("color: #323130;")
        
        monitor_desc = QLabel("Monitor file system changes while analysis is running")
        monitor_desc.setFont(QFont("Segoe UI", 9))
        monitor_desc.setStyleSheet("color: #605e5c; margin-top: 2px;")
        
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
    """Step 2: File Type Selection"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_type_cards = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Quick actions header
        header_card = ModernCard()
        header_layout = QHBoxLayout(header_card)
        
        info_layout = QVBoxLayout()
        info_title = QLabel("📁 File Type Selection")
        info_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        info_title.setStyleSheet("color: #323130;")
        
        info_desc = QLabel("Choose which file types to include in your security analysis")
        info_desc.setFont(QFont("Segoe UI", 10))
        info_desc.setStyleSheet("color: #605e5c; margin-top: 4px;")
        
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
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f3f2f1;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #c8c6c4;
                border-radius: 4px;
                min-height: 20px;
            }
        """)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(12)

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
    """Step 3: Keywords Configuration"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Keywords configuration card
        keywords_card = ModernCard()
        keywords_layout = QVBoxLayout(keywords_card)
        keywords_layout.setSpacing(24)

        # Header
        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        
        section_title = QLabel("🔍 Keyword Detection")
        section_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        section_title.setStyleSheet("color: #323130;")
        
        section_desc = QLabel("Configure how the system detects suspicious content")
        section_desc.setFont(QFont("Segoe UI", 10))
        section_desc.setStyleSheet("color: #605e5c; margin-top: 4px;")
        
        title_layout.addWidget(section_title)
        title_layout.addWidget(section_desc)
        header_layout.addLayout(title_layout)
        keywords_layout.addLayout(header_layout)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #edebe9;")
        keywords_layout.addWidget(sep)

        # Radio button group
        self.keywords_group = QButtonGroup()
        
        # Default keywords option
        default_layout = QHBoxLayout()
        default_icon = QLabel("🛡️")
        default_icon.setFont(QFont("Segoe UI", 16))
        default_layout.addWidget(default_icon)
        
        default_info_layout = QVBoxLayout()
        self.default_radio = QRadioButton("Use built-in security keywords")
        self.default_radio.setFont(QFont("Segoe UI", 12, QFont.Medium))
        self.default_radio.setChecked(True)
        
        default_desc = QLabel("Comprehensive database of 2,500+ security-related terms, threat indicators, and malware signatures")
        default_desc.setFont(QFont("Segoe UI", 10))
        default_desc.setStyleSheet("color: #605e5c; margin-left: 20px; margin-top: 4px;")
        default_desc.setWordWrap(True)
        
        # Built-in categories preview
        categories_label = QLabel("Includes: Malware signatures, suspicious commands, credential patterns, network indicators")
        categories_label.setFont(QFont("Segoe UI", 9))
        categories_label.setStyleSheet("color: #8a8886; margin-left: 20px; margin-top: 8px; font-style: italic;")
        categories_label.setWordWrap(True)
        
        default_info_layout.addWidget(self.default_radio)
        default_info_layout.addWidget(default_desc)
        default_info_layout.addWidget(categories_label)
        default_layout.addLayout(default_info_layout)
        
        keywords_layout.addLayout(default_layout)
        keywords_layout.addSpacing(16)
        
        # Custom keywords option
        custom_layout = QHBoxLayout()
        custom_icon = QLabel("📝")
        custom_icon.setFont(QFont("Segoe UI", 16))
        custom_layout.addWidget(custom_icon)
        
        custom_info_layout = QVBoxLayout()
        self.custom_radio = QRadioButton("Use custom keyword file")
        self.custom_radio.setFont(QFont("Segoe UI", 12, QFont.Medium))
        
        custom_desc = QLabel("Load your own keyword list from a text file (one keyword per line)")
        custom_desc.setFont(QFont("Segoe UI", 10))
        custom_desc.setStyleSheet("color: #605e5c; margin-left: 20px; margin-top: 4px;")
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
        self.file_path_label.setFont(QFont("Segoe UI", 9))
        self.file_path_label.setStyleSheet("color: #8a8886; margin-top: 4px;")
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
            self.file_path_label.setStyleSheet("color: #107c10; margin-top: 4px;")
            return file_path
        return None

class OptionsPage(QWidget):
    """Modern multi-step options page with swipe navigation"""
    
    def __init__(self, switch_to, session_state):
        super().__init__(parent=None)
        self.switch_to = switch_to
        self.session_state = session_state
        self.current_step = 0
        self.total_steps = 3
        self.init_ui()

    def init_ui(self):
        # Set overall app style
        self.setStyleSheet("""
            QWidget {
                background-color: #faf9f8;
                color: #323130;
                font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f3f2f1;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #c8c6c4;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a19f9d;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 24, 32, 24)
        main_layout.setSpacing(24)

        # Fixed header section
        self.create_header(main_layout)
        
        # Step indicator
        self.step_indicator = StepIndicator(self.total_steps)
        main_layout.addWidget(self.step_indicator)
        
        # Stacked widget for steps
        self.stacked_widget = QStackedWidget()
        
        # Create step widgets
        self.analysis_step = AnalysisOptionsStep()
        self.file_step = FileSelectionStep()
        self.keywords_step = KeywordsStep()
        
        self.stacked_widget.addWidget(self.analysis_step)
        self.stacked_widget.addWidget(self.file_step)
        self.stacked_widget.addWidget(self.keywords_step)
        
        main_layout.addWidget(self.stacked_widget)
        
        # Footer with navigation
        self.create_footer(main_layout)

    def create_header(self, layout):
        """Create fixed header section"""
        header_card = ModernCard()
        header_layout = QVBoxLayout(header_card)
        
        # Main title
        title = QLabel("Analysis Configuration")
        title.setFont(QFont("Segoe UI", 26, QFont.Light))
        title.setStyleSheet("color: #323130; margin-bottom: 4px;")
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Configure your security analysis settings in three simple steps")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #605e5c; margin-bottom: 12px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_card)

    def create_footer(self, layout):
        """Create footer with navigation buttons"""
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 16, 0, 0)
        
        # Back button
        self.back_btn = ModernButton("← Previous", "secondary")
        self.back_btn.clicked.connect(self.previous_step)
        self.back_btn.setVisible(False)  # Hidden on first step
        footer_layout.addWidget(self.back_btn)
        
        footer_layout.addStretch()
        
        # Status and validation
        self.status_container = QHBoxLayout()
        self.status_container.setSpacing(12)
        
        self.status_label = QLabel("Configure your analysis options to continue")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setStyleSheet("color: #605e5c;")
        
        self.status_container.addWidget(self.status_label)
        footer_layout.addLayout(self.status_container)
        
        # Next/Finish button
        self.next_btn = ModernButton("Next →", "primary")
        self.next_btn.clicked.connect(self.next_step)
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
        # Back button visibility
        self.back_btn.setVisible(self.current_step > 0)
        
        # Next button text and state
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
        if self.current_step == 0:  # Analysis Options
            self.status_label.setText("Configure your analysis options to continue")
            self.status_label.setStyleSheet("color: #605e5c; font-size: 10pt;")
            self.next_btn.setEnabled(True)
            
        elif self.current_step == 1:  # File Selection
            if self.file_step.has_selections():
                selected_count = len(self.file_step.get_selected_extensions())
                self.status_label.setText(f"✓ {selected_count} file types selected")
                self.status_label.setStyleSheet("color: #107c10; font-size: 10pt;")
                self.next_btn.setEnabled(True)
            else:
                self.status_label.setText("⚠️ Please select at least one file type")
                self.status_label.setStyleSheet("color: #d13438; font-size: 10pt;")
                self.next_btn.setEnabled(False)
                
        elif self.current_step == 2:  # Keywords
            if self.keywords_step.custom_radio.isChecked():
                if hasattr(self, 'custom_keyword_file') and self.custom_keyword_file:
                    self.status_label.setText("✓ Custom keyword file selected")
                    self.status_label.setStyleSheet("color: #107c10; font-size: 10pt;")
                    self.next_btn.setEnabled(True)
                else:
                    self.status_label.setText("⚠️ Please select a keyword file")
                    self.status_label.setStyleSheet("color: #d13438; font-size: 10pt;")
                    self.next_btn.setEnabled(False)
            else:
                self.status_label.setText("✓ Ready to start analysis")
                self.status_label.setStyleSheet("color: #107c10; font-size: 10pt;")
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
        if self.current_step == 1:  # File Selection
            if not self.file_step.has_selections():
                self.show_validation_error("Please select at least one file type to analyze.")
                return False
        elif self.current_step == 2:  # Keywords
            if self.keywords_step.custom_radio.isChecked():
                if not hasattr(self, 'custom_keyword_file') or not self.custom_keyword_file:
                    self.show_validation_error("Please select a custom keyword file or use built-in keywords.")
                    return False
        return True

    def show_validation_error(self, message):
        """Show validation error message"""
        self.status_label.setText(f"⚠️ {message}")
        self.status_label.setStyleSheet("color: #d13438; font-size: 10pt;")
        
        # Flash effect for attention
        QTimer.singleShot(100, lambda: self.status_label.setStyleSheet("color: #d13438; font-size: 10pt; background-color: #fef2f2; padding: 4px; border-radius: 4px;"))
        QTimer.singleShot(2000, lambda: self.status_label.setStyleSheet("color: #d13438; font-size: 10pt;"))

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
        self.next_btn.setText("Starting Analysis...")
        self.next_btn.setEnabled(False)
        self.status_label.setText("✓ Configuration saved successfully")
        self.status_label.setStyleSheet("color: #107c10; font-size: 10pt;")
        
        print("Final Configuration:", self.session_state)
        
        # Simulate processing and navigate
        QTimer.singleShot(1000, lambda: self.switch_to('analysis_page'))

    def keyPressEvent(self, event):
        """Handle keyboard navigation"""
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Space:
            if self.next_btn.isEnabled():
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
    
    # Apply modern style
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Set application properties
    app.setApplicationName("Security Analysis Tool")
    app.setApplicationVersion("2.0")
    
    # Test data
    session_state = {}
    switch_to = lambda page: print(f"Navigating to: {page}")
    
    # Create and show the options page
    options_page = OptionsPage(switch_to, session_state)
    options_page.setMinimumSize(1000, 800)
    options_page.show()
    
    sys.exit(app.exec_())