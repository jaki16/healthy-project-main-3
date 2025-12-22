"""
Food Logging Dialog
Add or edit food/meal entries
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QComboBox, QTextEdit,
                             QSpinBox, QDoubleSpinBox, QDateTimeEdit, QFileDialog,
                             QFrame, QGridLayout, QScrollArea, QWidget)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from datetime import datetime

class FoodLoggingDialog(QDialog):
    """Dialog for adding or editing food entries"""
    food_logged = pyqtSignal(dict)  # Signal when food is logged
    
    def __init__(self, parent=None, food_data=None):
        super().__init__(parent)
        self.food_data = food_data  # For editing existing entry
        self.image_path = None
        self.init_ui()
        
        if food_data:
            self.load_food_data(food_data)
            
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Log Food")
        self.setMinimumWidth(600)
        self.setMinimumHeight(700)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("🍎 Log Your Meal")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(title)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        
        # Date & Time
        datetime_section = self.create_datetime_section()
        form_layout.addWidget(datetime_section)
        
        # Meal Type
        meal_section = self.create_meal_type_section()
        form_layout.addWidget(meal_section)
        
        # Food Details
        food_section = self.create_food_details_section()
        form_layout.addWidget(food_section)
        
        # Nutrition Facts
        nutrition_section = self.create_nutrition_section()
        form_layout.addWidget(nutrition_section)
        
        # Photo Upload (Optional)
        photo_section = self.create_photo_section()
        form_layout.addWidget(photo_section)
        
        # Notes (Optional)
        notes_section = self.create_notes_section()
        form_layout.addWidget(notes_section)
        
        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)
        
        # Buttons
        button_layout = self.create_button_section()
        main_layout.addLayout(button_layout)
        
        # Apply dialog styling
        self.setStyleSheet("""
            QDialog {
                background: #f8f9fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateTimeEdit, QTextEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, 
            QDoubleSpinBox:focus, QDateTimeEdit:focus, QTextEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        
    def create_datetime_section(self):
        """Create date & time selection"""
        container = self.create_section_container("📅 When did you eat this?")
        layout = container.layout()
        
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd MMM yyyy - hh:mm AP")
        
        layout.addWidget(self.datetime_edit)
        
        return container
        
    def create_meal_type_section(self):
        """Create meal type selection"""
        container = self.create_section_container("🍽️ Meal Type")
        layout = container.layout()
        
        self.meal_type = QComboBox()
        self.meal_type.addItems(["Breakfast", "Lunch", "Dinner", "Snacks"])
        self.meal_type.setCurrentText(self.get_current_meal_type())
        
        layout.addWidget(self.meal_type)
        
        return container
        
    def create_food_details_section(self):
        """Create food details input"""
        container = self.create_section_container("🥗 Food Details")
        layout = container.layout()
        
        # Food name
        name_label = QLabel("Food Name *")
        name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.food_name = QLineEdit()
        self.food_name.setPlaceholderText("e.g., Grilled Chicken Breast")
        
        # Description
        desc_label = QLabel("Description")
        desc_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.food_description = QLineEdit()
        self.food_description.setPlaceholderText("e.g., With olive oil and herbs (optional)")
        
        # Serving size
        serving_label = QLabel("Serving Size")
        serving_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.serving_size = QLineEdit()
        self.serving_size.setPlaceholderText("e.g., 1 plate, 200g, 1 cup")
        
        layout.addWidget(name_label)
        layout.addWidget(self.food_name)
        layout.addWidget(desc_label)
        layout.addWidget(self.food_description)
        layout.addWidget(serving_label)
        layout.addWidget(self.serving_size)
        
        return container
        
    def create_nutrition_section(self):
        """Create nutrition facts input"""
        container = self.create_section_container("📊 Nutrition Facts")
        layout = container.layout()
        
        # Grid layout for nutrition inputs
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Calories
        cal_label = QLabel("Calories (kcal) *")
        cal_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.calories = QSpinBox()
        self.calories.setRange(0, 9999)
        self.calories.setSuffix(" kcal")
        self.calories.setValue(0)
        
        # Protein
        protein_label = QLabel("Protein (g)")
        protein_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.protein = QDoubleSpinBox()
        self.protein.setRange(0, 999.9)
        self.protein.setSuffix(" g")
        self.protein.setDecimals(1)
        
        # Carbs
        carbs_label = QLabel("Carbohydrates (g)")
        carbs_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.carbs = QDoubleSpinBox()
        self.carbs.setRange(0, 999.9)
        self.carbs.setSuffix(" g")
        self.carbs.setDecimals(1)
        
        # Fats
        fats_label = QLabel("Fats (g)")
        fats_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.fats = QDoubleSpinBox()
        self.fats.setRange(0, 999.9)
        self.fats.setSuffix(" g")
        self.fats.setDecimals(1)
        
        # Fiber (optional)
        fiber_label = QLabel("Fiber (g)")
        fiber_label.setFont(QFont("Segoe UI", 11))
        self.fiber = QDoubleSpinBox()
        self.fiber.setRange(0, 999.9)
        self.fiber.setSuffix(" g")
        self.fiber.setDecimals(1)
        
        # Sugar (optional)
        sugar_label = QLabel("Sugar (g)")
        sugar_label.setFont(QFont("Segoe UI", 11))
        self.sugar = QDoubleSpinBox()
        self.sugar.setRange(0, 999.9)
        self.sugar.setSuffix(" g")
        self.sugar.setDecimals(1)
        
        # Add to grid
        grid.addWidget(cal_label, 0, 0)
        grid.addWidget(self.calories, 0, 1)
        grid.addWidget(protein_label, 1, 0)
        grid.addWidget(self.protein, 1, 1)
        grid.addWidget(carbs_label, 2, 0)
        grid.addWidget(self.carbs, 2, 1)
        grid.addWidget(fats_label, 3, 0)
        grid.addWidget(self.fats, 3, 1)
        grid.addWidget(fiber_label, 4, 0)
        grid.addWidget(self.fiber, 4, 1)
        grid.addWidget(sugar_label, 5, 0)
        grid.addWidget(self.sugar, 5, 1)
        
        layout.addLayout(grid)
        
        # Quick calculate button
        calc_btn = QPushButton("📱 Use Nutrition Calculator")
        calc_btn.setStyleSheet("""
            QPushButton {
                background: #e3f2fd;
                color: #1976d2;
                border: 2px solid #90caf9;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #bbdefb;
            }
        """)
        calc_btn.clicked.connect(self.open_calculator)
        layout.addWidget(calc_btn)
        
        return container
        
    def create_photo_section(self):
        """Create photo upload section"""
        container = self.create_section_container("📸 Food Photo (Optional)")
        layout = container.layout()
        
        # Photo preview
        self.photo_label = QLabel("No photo selected")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setMinimumHeight(150)
        self.photo_label.setStyleSheet("""
            QLabel {
                background: white;
                border: 2px dashed #e0e0e0;
                border-radius: 8px;
                color: #95a5a6;
            }
        """)
        
        # Upload button
        upload_btn = QPushButton("📤 Upload Photo")
        upload_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #7f8c8d;
                border: 2px solid #e0e0e0;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                border: 2px solid #4CAF50;
                color: #4CAF50;
            }
        """)
        upload_btn.clicked.connect(self.upload_photo)
        
        layout.addWidget(self.photo_label)
        layout.addWidget(upload_btn)
        
        return container
        
    def create_notes_section(self):
        """Create notes section"""
        container = self.create_section_container("📝 Notes (Optional)")
        layout = container.layout()
        
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Any additional notes about this meal...")
        self.notes.setMaximumHeight(100)
        
        layout.addWidget(self.notes)
        
        return container
        
    def create_button_section(self):
        """Create dialog buttons"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #f0f0f0;
                color: #7f8c8d;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e0e0e0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        # Save button
        save_btn = QPushButton("💾 Save Meal")
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
        """)
        save_btn.clicked.connect(self.save_food)
        
        layout.addStretch()
        layout.addWidget(cancel_btn)
        layout.addWidget(save_btn)
        
        return layout
        
    def create_section_container(self, title):
        """Create a styled section container"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        
        # Section title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; background: transparent;")
        layout.addWidget(title_label)
        
        return container
        
    def get_current_meal_type(self):
        """Determine meal type based on current time"""
        hour = datetime.now().hour
        
        if 5 <= hour < 11:
            return "Breakfast"
        elif 11 <= hour < 15:
            return "Lunch"
        elif 15 <= hour < 18:
            return "Snacks"
        else:
            return "Dinner"
            
    def upload_photo(self):
        """Upload food photo"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Food Photo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(
                400, 150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.photo_label.setPixmap(scaled_pixmap)
            
    def open_calculator(self):
        """Open nutrition calculator"""
        # TODO: Implement nutrition calculator dialog
        print("Nutrition calculator - Will be implemented")
        
    def save_food(self):
        """Save food entry"""
        # Validate required fields
        if not self.food_name.text().strip():
            # TODO: Show error message
            print("Error: Food name is required")
            return
            
        if self.calories.value() == 0:
            # TODO: Show warning
            print("Warning: Calories is 0")
            
        # Collect data
        food_data = {
            'datetime': self.datetime_edit.dateTime().toPyDateTime(),
            'meal_type': self.meal_type.currentText(),
            'food_name': self.food_name.text(),
            'description': self.food_description.text(),
            'serving_size': self.serving_size.text(),
            'calories': self.calories.value(),
            'protein': self.protein.value(),
            'carbs': self.carbs.value(),
            'fats': self.fats.value(),
            'fiber': self.fiber.value(),
            'sugar': self.sugar.value(),
            'image_path': self.image_path,
            'notes': self.notes.toPlainText()
        }
        
        # Emit signal
        self.food_logged.emit(food_data)
        
        # TODO: Save to database
        print("Food logged:", food_data)
        
        self.accept()
        
    def load_food_data(self, data):
        """Load existing food data for editing"""
        if 'datetime' in data:
            self.datetime_edit.setDateTime(data['datetime'])
        if 'meal_type' in data:
            self.meal_type.setCurrentText(data['meal_type'])
        if 'food_name' in data:
            self.food_name.setText(data['food_name'])
        if 'description' in data:
            self.food_description.setText(data['description'])
        if 'serving_size' in data:
            self.serving_size.setText(data['serving_size'])
        if 'calories' in data:
            self.calories.setValue(data['calories'])
        if 'protein' in data:
            self.protein.setValue(data['protein'])
        if 'carbs' in data:
            self.carbs.setValue(data['carbs'])
        if 'fats' in data:
            self.fats.setValue(data['fats'])
        if 'fiber' in data:
            self.fiber.setValue(data['fiber'])
        if 'sugar' in data:
            self.sugar.setValue(data['sugar'])
        if 'notes' in data:
            self.notes.setPlainText(data['notes'])