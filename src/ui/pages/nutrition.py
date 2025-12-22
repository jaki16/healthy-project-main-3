"""
Nutrition Tracker Page
File: src/ui/pages/nutrition.py

Features:
- Food logging with database
- Calorie tracking
- Macro nutrients visualization
- Meal planning
- Food search
- Daily nutrition summary
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QGridLayout, QPushButton, QLineEdit,
                            QComboBox, QScrollArea, QDialog, QSpinBox,
                            QDoubleSpinBox, QTextEdit)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from datetime import datetime, date
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))


class FoodCard(QFrame):
    """Card displaying a food entry"""
    
    def __init__(self, food_name, meal_type, calories, protein, carbs, fat, time="", parent=None):
        super().__init__(parent)
        self.food_name = food_name
        self.meal_type = meal_type
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.time = time
        self.setup_ui()
        
    def setup_ui(self):
        """Setup food card UI"""
        self.setObjectName("foodCard")
        self.setStyleSheet("""
            #foodCard {
                background-color: #1E1E1E;
                border: 2px solid #2D2D2D;
                border-radius: 12px;
                padding: 15px;
            }
            #foodCard:hover {
                background-color: #252525;
                border-color: #00BFA5;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(15)
        
        # Left side - Food info
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)
        
        # Meal type badge
        meal_colors = {
            "breakfast": "#FF9800",
            "lunch": "#4CAF50",
            "dinner": "#2196F3",
            "snack": "#9C27B0"
        }
        
        meal_icons = {
            "breakfast": "🌅",
            "lunch": "☀️",
            "dinner": "🌙",
            "snack": "🍿"
        }
        
        meal_badge = QLabel(f"{meal_icons.get(self.meal_type, '🍽️')} {self.meal_type.title()}")
        meal_badge.setFont(QFont("Segoe UI", 9))
        meal_badge.setStyleSheet(f"""
            background-color: {meal_colors.get(self.meal_type, '#666')};
            color: white;
            border: none;
            border-radius: 5px;
            padding: 3px 10px;
        """)
        meal_badge.setFixedWidth(120)
        left_layout.addWidget(meal_badge)
        
        # Food name
        name_label = QLabel(self.food_name)
        name_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        name_label.setStyleSheet("color: white; border: none; background: transparent;")
        left_layout.addWidget(name_label)
        
        # Time
        if self.time:
            time_label = QLabel(f"⏰ {self.time}")
            time_label.setFont(QFont("Segoe UI", 9))
            time_label.setStyleSheet("color: #888; border: none; background: transparent;")
            left_layout.addWidget(time_label)
        
        left_layout.addStretch()
        layout.addLayout(left_layout, 2)
        
        # Right side - Nutrition info
        right_layout = QGridLayout()
        right_layout.setSpacing(10)
        
        # Calories (prominent)
        cal_layout = QVBoxLayout()
        cal_value = QLabel(str(self.calories))
        cal_value.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        cal_value.setStyleSheet("color: #FF6B6B; border: none; background: transparent;")
        cal_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cal_layout.addWidget(cal_value)
        
        cal_label = QLabel("kcal")
        cal_label.setFont(QFont("Segoe UI", 8))
        cal_label.setStyleSheet("color: #888; border: none; background: transparent;")
        cal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cal_layout.addWidget(cal_label)
        
        right_layout.addLayout(cal_layout, 0, 0)
        
        # Macros
        macros = [
            ("P", f"{self.protein}g", "#00BFA5"),
            ("C", f"{self.carbs}g", "#FFD54F"),
            ("F", f"{self.fat}g", "#FF4081")
        ]
        
        for i, (label, value, color) in enumerate(macros, 1):
            macro_layout = QVBoxLayout()
            
            label_widget = QLabel(label)
            label_widget.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            label_widget.setStyleSheet(f"color: {color}; border: none; background: transparent;")
            label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            macro_layout.addWidget(label_widget)
            
            value_widget = QLabel(value)
            value_widget.setFont(QFont("Segoe UI", 9))
            value_widget.setStyleSheet("color: #CCC; border: none; background: transparent;")
            value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            macro_layout.addWidget(value_widget)
            
            right_layout.addLayout(macro_layout, 0, i)
        
        layout.addLayout(right_layout, 1)
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(35, 35)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #FF5252;
                border-radius: 17px;
                color: #FF5252;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FF5252;
                color: white;
            }
        """)
        layout.addWidget(delete_btn)


class AddFoodDialog(QDialog):
    """Dialog for adding new food entry"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Food")
        self.setModal(True)
        self.setFixedSize(500, 600)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
                background-color: #2D2D2D;
                color: white;
                border: 2px solid #3D3D3D;
                border-radius: 8px;
                padding: 8px;
                min-height: 35px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #00BFA5;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Add Food Entry")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #00BFA5;")
        layout.addWidget(title)
        
        # Meal type
        meal_label = QLabel("Meal Type:")
        meal_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(meal_label)
        
        self.meal_combo = QComboBox()
        self.meal_combo.addItems(["Breakfast", "Lunch", "Dinner", "Snack"])
        layout.addWidget(self.meal_combo)
        
        # Food name
        food_label = QLabel("Food Name:")
        food_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(food_label)
        
        self.food_input = QLineEdit()
        self.food_input.setPlaceholderText("e.g., Nasi Goreng")
        layout.addWidget(self.food_input)
        
        # Nutrition info
        nutrition_label = QLabel("Nutrition Information:")
        nutrition_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        layout.addWidget(nutrition_label)
        
        # Grid for nutrition inputs
        nutrition_grid = QGridLayout()
        nutrition_grid.setSpacing(10)
        
        # Calories
        cal_label = QLabel("Calories (kcal):")
        nutrition_grid.addWidget(cal_label, 0, 0)
        self.calories_input = QSpinBox()
        self.calories_input.setRange(0, 5000)
        self.calories_input.setSuffix(" kcal")
        nutrition_grid.addWidget(self.calories_input, 0, 1)
        
        # Protein
        protein_label = QLabel("Protein (g):")
        nutrition_grid.addWidget(protein_label, 1, 0)
        self.protein_input = QDoubleSpinBox()
        self.protein_input.setRange(0, 500)
        self.protein_input.setSuffix(" g")
        nutrition_grid.addWidget(self.protein_input, 1, 1)
        
        # Carbohydrates
        carbs_label = QLabel("Carbs (g):")
        nutrition_grid.addWidget(carbs_label, 2, 0)
        self.carbs_input = QDoubleSpinBox()
        self.carbs_input.setRange(0, 500)
        self.carbs_input.setSuffix(" g")
        nutrition_grid.addWidget(self.carbs_input, 2, 1)
        
        # Fat
        fat_label = QLabel("Fat (g):")
        nutrition_grid.addWidget(fat_label, 3, 0)
        self.fat_input = QDoubleSpinBox()
        self.fat_input.setRange(0, 200)
        self.fat_input.setSuffix(" g")
        nutrition_grid.addWidget(self.fat_input, 3, 1)
        
        layout.addLayout(nutrition_grid)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #3D3D3D;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4D4D4D;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        add_btn = QPushButton("Add Food")
        add_btn.setFixedHeight(45)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00E5CC;
            }
        """)
        add_btn.clicked.connect(self.accept)
        button_layout.addWidget(add_btn)
        
        layout.addLayout(button_layout)
    
    def get_food_data(self):
        """Get entered food data"""
        return {
            "meal_type": self.meal_combo.currentText().lower(),
            "food_name": self.food_input.text(),
            "calories": self.calories_input.value(),
            "protein": self.protein_input.value(),
            "carbs": self.carbs_input.value(),
            "fat": self.fat_input.value()
        }


class NutritionPage(QWidget):
    """Main nutrition tracker page"""
    
    def __init__(self):
        super().__init__()
        
        # Sample data (will be replaced with database)
        self.today_foods = [
            {
                "food_name": "Nasi Goreng",
                "meal_type": "breakfast",
                "calories": 450,
                "protein": 15,
                "carbs": 65,
                "fat": 12,
                "time": "07:30 AM"
            },
            {
                "food_name": "Chicken Salad",
                "meal_type": "lunch",
                "calories": 350,
                "protein": 35,
                "carbs": 20,
                "fat": 15,
                "time": "12:45 PM"
            },
            {
                "food_name": "Banana",
                "meal_type": "snack",
                "calories": 105,
                "protein": 1,
                "carbs": 27,
                "fat": 0.5,
                "time": "03:15 PM"
            }
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup nutrition page UI"""
        # Root layout with scroll area for entire page (smooth in small screens)
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #121212;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #1E1E1E;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #3D3D3D;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #00BFA5;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        container = QWidget()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Title
        title_layout = QVBoxLayout()
        title = QLabel("Nutrition Tracker")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title_layout.addWidget(title)
        
        date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        date_label.setFont(QFont("Segoe UI", 11))
        date_label.setStyleSheet("color: #888;")
        title_layout.addWidget(date_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Add food button
        add_btn = QPushButton("➕ Add Food")
        add_btn.setFixedSize(150, 50)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BFA5;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00E5CC;
            }
        """)
        add_btn.clicked.connect(self.show_add_food_dialog)
        header_layout.addWidget(add_btn)
        
        main_layout.addLayout(header_layout)
        
        # Summary cards
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(15)
        
        total_calories = sum(f["calories"] for f in self.today_foods)
        total_protein = sum(f["protein"] for f in self.today_foods)
        total_carbs = sum(f["carbs"] for f in self.today_foods)
        total_fat = sum(f["fat"] for f in self.today_foods)
        
        self.create_summary_card(summary_layout, "🔥", "Calories", f"{total_calories}", "/ 2000 kcal", int((total_calories/2000)*100))
        self.create_summary_card(summary_layout, "💪", "Protein", f"{total_protein}g", "/ 150g", int((total_protein/150)*100))
        self.create_summary_card(summary_layout, "🍞", "Carbs", f"{total_carbs}g", "/ 250g", int((total_carbs/250)*100))
        self.create_summary_card(summary_layout, "🥑", "Fat", f"{total_fat}g", "/ 70g", int((total_fat/70)*100))
        
        main_layout.addLayout(summary_layout)
        
        # Charts section
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Macro pie chart
        macro_chart = self.create_macro_pie_chart(total_protein, total_carbs, total_fat)
        charts_layout.addWidget(macro_chart, 1)
        
        # Weekly calories bar chart
        weekly_chart = self.create_weekly_calories_chart()
        charts_layout.addWidget(weekly_chart, 2)
        
        main_layout.addLayout(charts_layout)
        
        # Food log section
        log_header = QLabel("📋 Today's Food Log")
        log_header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        log_header.setStyleSheet("color: white;")
        main_layout.addWidget(log_header)

        # Food cards (tanpa nested scroll; halaman sudah di-scroll dari root)
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_layout.setSpacing(10)
        log_layout.setContentsMargins(0, 0, 0, 0)

        for food in self.today_foods:
            card = FoodCard(
                food["food_name"],
                food["meal_type"],
                food["calories"],
                food["protein"],
                food["carbs"],
                food["fat"],
                food.get("time", "")
            )
            log_layout.addWidget(card)

        log_layout.addStretch()
        main_layout.addWidget(log_container)
        main_layout.addStretch()
        root_layout.addWidget(scroll)
    
    def create_summary_card(self, layout, icon, title, value, target, progress):
        """Create nutrition summary card"""
        card = QFrame()
        card.setObjectName("summaryCard")
        card.setStyleSheet("""
            #summaryCard {
                background-color: #1E1E1E;
                border: 2px solid #2D2D2D;
                border-radius: 12px;
                padding: 20px;
                min-width: 180px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        
        # Icon and title
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        header.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10))
        title_label.setStyleSheet("color: #888; background: transparent; border: none;")
        header.addWidget(title_label, 1)
        
        card_layout.addLayout(header)
        
        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #00BFA5; background: transparent; border: none;")
        card_layout.addWidget(value_label)
        
        # Target
        target_label = QLabel(target)
        target_label.setFont(QFont("Segoe UI", 9))
        target_label.setStyleSheet("color: #666; background: transparent; border: none;")
        card_layout.addWidget(target_label)
        
        # Progress bar
        from PyQt6.QtWidgets import QProgressBar
        progress_bar = QProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(8)
        progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2D2D2D;
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #00BFA5;
                border-radius: 4px;
            }
        """)
        card_layout.addWidget(progress_bar)
        
        layout.addWidget(card)
    
    def create_macro_pie_chart(self, protein, carbs, fat):
        """Create macronutrients pie chart"""
        series = QPieSeries()
        series.append(f"Protein {protein}g", protein * 4)  # 4 cal per gram
        series.append(f"Carbs {carbs}g", carbs * 4)  # 4 cal per gram
        series.append(f"Fat {fat}g", fat * 9)  # 9 cal per gram
        
        # Style slices
        colors = [QColor("#00BFA5"), QColor("#FFD54F"), QColor("#FF4081")]
        for i, slice in enumerate(series.slices()):
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("white"))
            slice.setColor(colors[i])
            slice.setLabelFont(QFont("Segoe UI", 10))
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Macro Distribution")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart.legend().setFont(QFont("Segoe UI", 9))
        chart.legend().setLabelColor(QColor("white"))
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        chart.setTitleFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(chart_view.renderHints())
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")
        chart_view.setMinimumHeight(300)
        
        return chart_view
    
    def create_weekly_calories_chart(self):
        """Create weekly calories bar chart"""
        bar_set = QBarSet("Calories")
        bar_set.append([1800, 2100, 1950, 2300, 1850, 905, 0])  # Today is Saturday
        bar_set.setColor(QColor("#00BFA5"))
        
        series = QBarSeries()
        series.append(bar_set)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Weekly Calorie Intake")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.legend().hide()
        chart.setBackgroundBrush(QColor("#1E1E1E"))
        chart.setTitleBrush(QColor("white"))
        chart.setTitleFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        
        categories = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setLabelsColor(QColor("#888"))
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 2500)
        axis_y.setLabelFormat("%d")
        axis_y.setLabelsColor(QColor("#888"))
        axis_y.setGridLineColor(QColor("#2D2D2D"))
        
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(chart_view.renderHints())
        chart_view.setStyleSheet("background-color: #1E1E1E; border-radius: 15px;")
        chart_view.setMinimumHeight(300)
        
        return chart_view
    
    def show_add_food_dialog(self):
        """Show add food dialog"""
        dialog = AddFoodDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            food_data = dialog.get_food_data()
            if food_data["food_name"]:
                # Add to today's foods
                food_data["time"] = datetime.now().strftime("%I:%M %p")
                self.today_foods.append(food_data)
                
                # Refresh UI (in real app, would update database first)
                # For now, just show success message
                print(f"✓ Added: {food_data['food_name']}")
                
                # TODO: Refresh the page to show new food