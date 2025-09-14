# login_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginPage(QWidget):
    def __init__(self, switch_callback, session_state):
        super().__init__()
        self.switch_callback = switch_callback
        self.session_state = session_state
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        header = QLabel("🔐 Investigator Login")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color:#00ffcc;")
        layout.addWidget(header)

        form = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Investigator Name")
        self.case_input = QLineEdit()
        self.case_input.setPlaceholderText("Case ID")
        self.agency_input = QLineEdit()
        self.agency_input.setPlaceholderText("Agency (optional)")

        for w in (self.name_input, self.case_input, self.agency_input):
            w.setFixedWidth(400)
            w.setStyleSheet("background:#1a1d23; color:#EEE; padding:6px; border-radius:4px;")

        form.addWidget(self.name_input)
        form.addWidget(self.case_input)
        form.addWidget(self.agency_input)

        btn = QPushButton("Continue ▶")
        btn.setFixedWidth(200)
        btn.clicked.connect(self.on_continue)
        btn.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #00ffcc, stop:1 #0066ff); "
            "color:black; padding:8px; border-radius:6px;"
        )
        form.addWidget(btn, alignment=Qt.AlignCenter)

        # ⚠️ Info note at the bottom
        note = QLabel("\n\n\nNo credentials are saved.\n"
                      "The entered details will only appear in the final report.")
        note.setStyleSheet("color: gray; font-size: 9pt; font-style: italic; margin-top:10px;")
        note.setAlignment(Qt.AlignCenter)
        form.addWidget(note, alignment=Qt.AlignCenter)

        layout.addLayout(form)
        self.setLayout(layout)

    def on_continue(self):
        name = self.name_input.text().strip()
        case_id = self.case_input.text().strip()
        agency = self.agency_input.text().strip()
        if not name or not case_id:
            QMessageBox.warning(self, "Missing", "Please enter Investigator name and Case ID.")
            return
        self.session_state["investigator"] = {"name": name, "case_id": case_id, "agency": agency}
        self.switch_callback("setup")
