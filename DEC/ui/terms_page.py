from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QPlainTextEdit,
    QRadioButton, QHBoxLayout, QMessageBox, QButtonGroup, QApplication
)
from PyQt5.QtGui import QFont


class TermsPage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Header
        header = QLabel("📜 License Agreement")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color:white; margin: 10px;")
        layout.addWidget(header, alignment=Qt.AlignCenter)

        subheader = QLabel("Please read the following license agreement carefully before using this software:")
        subheader.setStyleSheet("color:#EEE; margin-bottom:6px;")
        layout.addWidget(subheader)

        # Scrollable terms text
        self.terms_box = QPlainTextEdit()
        self.terms_box.setReadOnly(True)
        self.terms_box.setFont(QFont("Courier New", 10))  # ✅ Monospaced like real license text
        self.terms_box.setStyleSheet("""
            QPlainTextEdit {
                background:#1a1d23;
                color:#EEE;
                padding:10px;
                border:1px solid #444;
                border-radius:6px;
            }
        """)

        # Realistic license agreement text
        self.terms_box.setPlainText(
            "END-USER LICENSE AGREEMENT (EULA)\n"
            "----------------------------------\n\n"
            "IMPORTANT: PLEASE READ THIS LICENSE AGREEMENT CAREFULLY BEFORE USING THE SOFTWARE.\n\n"
            "1. GRANT OF LICENSE\n"
            "   This License Agreement permits you to use the Digital Evidence Categorizer (DEC) "
            "for lawful and authorized forensic investigation purposes only.\n\n"
            "2. RESTRICTIONS\n"
            "   You may NOT:\n"
            "   • Modify, reverse engineer, decompile, or disassemble the software.\n"
            "   • Use the software for unlawful activities.\n"
            "   • Rent, lease, or distribute copies to unauthorized third parties.\n\n"
            "3. DISCLAIMER OF WARRANTY\n"
            "   This software is provided 'AS IS' without warranty of any kind, either express "
            "or implied. The entire risk as to the results and performance of the software "
            "is assumed by you.\n\n"
            "4. LIMITATION OF LIABILITY\n"
            "   In no event shall the developers be liable for any damages, including but not "
            "limited to loss of data, loss of profits, or business interruption arising from "
            "the use or inability to use the software.\n\n"
            "5. GOVERNING LAW\n"
            "   This License shall be governed by and construed in accordance with the local "
            "laws applicable to digital forensics and investigative procedures.\n\n"
            "6. TERMINATION\n"
            "   This license is effective until terminated. Failure to comply with these terms "
            "will result in automatic termination of your rights to use this software.\n\n"
            "BY CLICKING 'I ACCEPT', YOU ACKNOWLEDGE THAT YOU HAVE READ AND UNDERSTOOD "
            "THIS AGREEMENT AND AGREE TO BE BOUND BY ITS TERMS.\n"
        )
        self.terms_box.setMinimumHeight(280)
        layout.addWidget(self.terms_box)

        # Custom radio button style
        radio_style = """
        QRadioButton {
            color: #EEE;
            font-size: 11pt;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid #00ffcc;
            background: transparent;
        }
        QRadioButton::indicator:checked {
            background-color: #00ffcc;
            border: 2px solid #00ffcc;
        }
        """

        # Radio buttons (Accept / Decline)
        self.accept_radio = QRadioButton("I accept the terms in the license agreement")
        self.decline_radio = QRadioButton("I do not accept the terms in the license agreement")

        for rb in (self.accept_radio, self.decline_radio):
            rb.setStyleSheet(radio_style)

        radio_group = QButtonGroup(self)
        radio_group.addButton(self.accept_radio)
        radio_group.addButton(self.decline_radio)

        layout.addWidget(self.accept_radio)
        layout.addWidget(self.decline_radio)

        # Buttons row
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close_app)
        btn_row.addWidget(cancel_btn)

        self.next_btn = QPushButton("Next ▶")
        self.next_btn.setVisible(False)  # Hidden until accept
        self.next_btn.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 #00ffcc, stop:1 #0066ff); color:black; padding:8px; border-radius:6px;"
        )
        self.next_btn.clicked.connect(self.on_next)
        btn_row.addWidget(self.next_btn)

        layout.addLayout(btn_row)

        # Connect radio logic
        self.accept_radio.toggled.connect(self.toggle_next)

        self.setLayout(layout)

    def toggle_next(self):
        self.next_btn.setVisible(self.accept_radio.isChecked())

    def on_next(self):
        if self.accept_radio.isChecked():
            self.switch_callback("splash")
        else:
            QMessageBox.warning(self, "License Agreement", "You must accept the terms to continue.")

    def close_app(self):
        QApplication.quit()
