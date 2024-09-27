import sys
import subprocess
import json
from PySide6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, 
                               QMessageBox, QGridLayout, QScrollArea, QFrame, QSplitter, QDateEdit)
from PySide6.QtGui import QPixmap, QFont, QImage
from PySide6.QtCore import Qt, QDate
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class LabelGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Label Generator")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QHBoxLayout()
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.label_inputs = []
        self.label_previews = []

        for i in range(4):
            heading = QLabel(f"Label {i+1}")
            heading_font = QFont()
            heading_font.setPointSize(16)
            heading_font.setBold(True)
            heading.setFont(heading_font)
            self.scroll_layout.addWidget(heading)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            self.scroll_layout.addWidget(line)

            label_layout = QGridLayout()
            inputs = {}
            for j, field in enumerate(['drumID', 'volume', 'samplePurpose', 'sampleNumber', 'samplesTotal', 'sampleDate', 'sampledBy']):
                label = QLabel(field)
                if field == 'sampleDate':
                    input_field = QDateEdit()
                    input_field.setCalendarPopup(True)
                    input_field.setDate(QDate.currentDate())
                    input_field.dateChanged.connect(self.update_label_previews)
                else:
                    input_field = QLineEdit()
                    input_field.setPlaceholderText(f"Enter {field}")
                    input_field.textChanged.connect(self.update_label_previews)
                inputs[field] = input_field
                label_layout.addWidget(label, j, 0)
                label_layout.addWidget(input_field, j, 1)
            
            self.label_inputs.append(inputs)
            
            preview_label = QLabel()
            preview_label.setAlignment(Qt.AlignCenter)
            self.label_previews.append(preview_label)
            label_layout.addWidget(preview_label, 0, 2, 7, 1)  # Span 7 rows
            
            self.scroll_layout.addLayout(label_layout)
            self.scroll_layout.addSpacing(20)

        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

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
        self.print_button.clicked.connect(self.print_labels)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.print_button)
        button_layout.addStretch()

        left_layout.addWidget(self.scroll_area)
        left_layout.addLayout(button_layout)

        # Right side with description and template image
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        description = QLabel("""
        <h2>How to use the Label Generator:</h2>
        <ol>
            <li>Fill in the details for each label in the form on the left.</li>
            <li>As you type, a preview of each label will appear.</li>
            <li>For the sample date, use the date picker by clicking the calendar icon.</li>
            <li>You can create up to 4 labels at once.</li>
            <li>When you're ready, click the red 'PRINT' button to generate and print the labels.</li>
            <li>The generated labels will be saved as an image file and opened automatically.</li>
            <li>Note: A preview will only be shown if fields other than just the sample date are filled.</li>
        </ol>
        <p>Below is a template of a blank label:</p>
        """)
        description.setWordWrap(True)
        right_layout.addWidget(description)

        # Add blank template image
        template_image = QLabel()
        template_pixmap = QPixmap(self.create_blank_template())
        template_image.setPixmap(template_pixmap.scaled(390, 390, Qt.KeepAspectRatio))
        template_image.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(template_image)

        right_layout.addStretch()

        # Use QSplitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 2)  # Left side takes up more space
        splitter.setStretchFactor(1, 1)  # Right side takes up less space

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def update_label_previews(self):
        for i, inputs in enumerate(self.label_inputs):
            label_data = {}
            for field, input_field in inputs.items():
                if field == 'sampleDate':
                    label_data[field] = input_field.date().toString("yyyy-MM-dd")
                else:
                    label_data[field] = input_field.text()
            
            # Check if any fields other than sampleDate are filled
            other_fields_filled = any(value for key, value in label_data.items() if key != 'sampleDate')
            
            if other_fields_filled:
                preview_image = self.create_label_preview(label_data)
                pixmap = QPixmap()
                pixmap.loadFromData(preview_image.getvalue())
                self.label_previews[i].setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            else:
                self.label_previews[i].clear()

    def create_label_preview(self, label_data):
        img = Image.new('RGB', (390, 390), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('Arial.ttf', 20)

        y_offset = 65
        for field, value in label_data.items():
            draw.text((20, y_offset), f"{field}: {value}", fill='black', font=font)
            y_offset += 45

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def create_blank_template(self):
        img = Image.new('RGB', (390, 390), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('Arial.ttf', 20)

        fields = ['drumID', 'volume', 'samplePurpose', 'sampleNumber', 'samplesTotal', 'sampleDate', 'sampledBy']
        y_offset = 65
        for field in fields:
            draw.text((20, y_offset), f"{field}: _______________", fill='black', font=font)
            y_offset += 45

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()

    def print_labels(self):
        label_data = []
        for inputs in self.label_inputs:
            data = {}
            for field, input_field in inputs.items():
                if field == 'sampleDate':
                    data[field] = input_field.date().toString("yyyy-MM-dd")
                else:
                    data[field] = input_field.text()
            
            # Check if any fields other than sampleDate are filled
            other_fields_filled = any(value for key, value in data.items() if key != 'sampleDate')
            
            if other_fields_filled:
                label_data.append(data)
        
        if not label_data:
            QMessageBox.warning(self, "No Data", "Please enter data for at least one label (fields other than just the sample date).")
            return

        arg_string = json.dumps(label_data)
        script_path = "labelgenerator.py"
        
        try:
            subprocess.Popen(['python', script_path, arg_string])
            print(f"External Python script launched with arguments: {arg_string}")

            msg_box = QMessageBox()
            msg_box.setWindowTitle("Labels Generated")
            msg_box.setText("Labels generated and saved to LABELS_PRINT_ME_0.png\nPrint this file using printer HP Laserjet")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()

            subprocess.Popen(['explorer', 'C:\LABEL_PRINTER'])

        except Exception as e:
            print(f"Error launching external Python script: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabelGenerator()
    window.show()
    sys.exit(app.exec())