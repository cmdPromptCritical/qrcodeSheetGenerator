import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import qrcode
from io import BytesIO
from PIL import Image
import time

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 800, 700)

        self.main_layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.qr_layout = QVBoxLayout()

        self.inputs = []
        self.qr_labels = []

        for i in range(4):
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter number {i+1}")
            input_field.textChanged.connect(self.update_qr_codes)
            self.inputs.append(input_field)
            self.input_layout.addWidget(input_field)

        for i in range(5):
            row_layout = QHBoxLayout()
            for j in range(4):
                label = QLabel()
                label.setAlignment(Qt.AlignCenter)
                self.qr_labels.append(label)
                row_layout.addWidget(label)
            self.qr_layout.addLayout(row_layout)

        # Create the PRINT button
        self.print_button = QPushButton("PRINT")
        self.print_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-size: 24px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.print_button.setFixedSize(200, 60)
        self.print_button.clicked.connect(self.print_qr_codes)

        # Create a layout for the button and center it
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.print_button)
        button_layout.addStretch()

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.qr_layout)
        self.main_layout.addLayout(button_layout)
        self.setLayout(self.main_layout)

    def update_qr_codes(self):
        for i, input_field in enumerate(self.inputs):
            number = input_field.text()
            if number:
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(number)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")

                buffer = BytesIO()
                img.save(buffer, format="PNG")
                qr_image = QPixmap()
                qr_image.loadFromData(buffer.getvalue())

                for j in range(5):
                    self.qr_labels[i + j * 4].setPixmap(qr_image.scaled(100, 100, Qt.KeepAspectRatio))
            else:
                for j in range(5):
                    self.qr_labels[i + j * 4].clear()

    def print_qr_codes(self):
        # Collect input values
        input_values = [input_field.text() for input_field in self.inputs]
        
        # Create the argument string
        arg_string = ','.join(input_values)
        
        # Path to your Python script
        script_path = "qrcodegenerator.py"
        
        try:
            # Run the Python script with the input values as an argument
            subprocess.Popen(['python', script_path, arg_string])
            print(f"External Python script launched with arguments: {arg_string}")

            # Show popup message
            msg_box = QMessageBox()
            msg_box.setWindowTitle("QR Code Generated")
            msg_box.setText("QR codes generated and saved to QR_CODES_PRINT_ME_0.png\nPrint this file using printer HP Laserjet")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

            # open image in default photo viewer
            #time.sleep(1)
            #image = Image.open('QR_CODES_PRINT_ME_0.png')
            #time.sleep(1)
            #image.show()
            subprocess.Popen(['explorer', 'C:\QR_CODE_PRINTER'])

        except Exception as e:
            print(f"Error launching external Python script: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec())
