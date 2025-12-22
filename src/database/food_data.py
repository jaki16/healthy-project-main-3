"""
Food Database - Indonesian & International Foods
File: src/database/food_data.py

Comprehensive food database with nutrition information
"""

FOOD_DATABASE = {
    # Indonesian Foods - Breakfast
    "nasi_goreng": {
        "name": "Nasi Goreng",
        "category": "Indonesian",
        "meal_type": "breakfast",
        "calories": 450,
        "protein": 15,
        "carbs": 65,
        "fat": 12,
        "fiber": 3,
        "serving": "1 plate (300g)"
    },
    "nasi_uduk": {
        "name": "Nasi Uduk",
        "category": "Indonesian",
        "meal_type": "breakfast",
        "calories": 380,
        "protein": 12,
        "carbs": 55,
        "fat": 10,
        "fiber": 2,
        "serving": "1 plate (250g)"
    },
    "bubur_ayam": {
        "name": "Bubur Ayam",
        "category": "Indonesian",
        "meal_type": "breakfast",
        "calories": 320,
        "protein": 18,
        "carbs": 48,
        "fat": 8,
        "fiber": 2,
        "serving": "1 bowl (350g)"
    },
    "lontong_sayur": {
        "name": "Lontong Sayur",
        "category": "Indonesian",
        "meal_type": "breakfast",
        "calories": 280,
        "protein": 10,
        "carbs": 45,
        "fat": 7,
        "fiber": 4,
        "serving": "1 serving (300g)"
    },
    
    # Indonesian Foods - Lunch/Dinner
    "rendang": {
        "name": "Rendang Daging",
        "category": "Indonesian",
        "meal_type": "lunch",
        "calories": 420,
        "protein": 28,
        "carbs": 8,
        "fat": 32,
        "fiber": 2,
        "serving": "1 serving (200g)"
    },
    "soto_ayam": {
        "name": "Soto Ayam",
        "category": "Indonesian",
        "meal_type": "lunch",
        "calories": 310,
        "protein": 22,
        "carbs": 35,
        "fat": 9,
        "fiber": 3,
        "serving": "1 bowl (400g)"
    },
    "gado_gado": {
        "name": "Gado-Gado",
        "category": "Indonesian",
        "meal_type": "lunch",
        "calories": 350,
        "protein": 14,
        "carbs": 42,
        "fat": 16,
        "fiber": 8,
        "serving": "1 plate (350g)"
    },
    "ayam_goreng": {
        "name": "Ayam Goreng",
        "category": "Indonesian",
        "meal_type": "lunch",
        "calories": 380,
        "protein": 32,
        "carbs": 18,
        "fat": 22,
        "fiber": 1,
        "serving": "1 piece (200g)"
    },
    "nasi_padang": {
        "name": "Nasi Padang (set)",
        "category": "Indonesian",
        "meal_type": "lunch",
        "calories": 650,
        "protein": 28,
        "carbs": 75,
        "fat": 28,
        "fiber": 5,
        "serving": "1 set"
    },
    "mie_goreng": {
        "name": "Mie Goreng",
        "category": "Indonesian",
        "meal_type": "lunch",
        "calories": 420,
        "protein": 16,
        "carbs": 58,
        "fat": 14,
        "fiber": 3,
        "serving": "1 plate (300g)"
    },
    "sate_ayam": {
        "name": "Sate Ayam",
        "category": "Indonesian",
        "meal_type": "lunch",
        "calories": 280,
        "protein": 26,
        "carbs": 12,
        "fat": 14,
        "fiber": 1,
        "serving": "10 skewers"
    },
    "pecel_lele": {
        "name": "Pecel Lele",
        "category": "Indonesian",
        "meal_type": "dinner",
        "calories": 340,
        "protein": 24,
        "carbs": 28,
        "fat": 16,
        "fiber": 4,
        "serving": "1 serving"
    },
    
    # Indonesian Snacks
    "pisang_goreng": {
        "name": "Pisang Goreng",
        "category": "Indonesian",
        "meal_type": "snack",
        "calories": 180,
        "protein": 2,
        "carbs": 32,
        "fat": 6,
        "fiber": 2,
        "serving": "2 pieces"
    },
    "lemper": {
        "name": "Lemper",
        "category": "Indonesian",
        "meal_type": "snack",
        "calories": 220,
        "protein": 8,
        "carbs": 35,
        "fat": 6,
        "fiber": 2,
        "serving": "2 pieces"
    },
    "risoles": {
        "name": "Risoles",
        "category": "Indonesian",
        "meal_type": "snack",
        "calories": 190,
        "protein": 7,
        "carbs": 24,
        "fat": 8,
        "fiber": 2,
        "serving": "1 piece"
    },
    
    # International - Western
    "chicken_salad": {
        "name": "Chicken Salad",
        "category": "Western",
        "meal_type": "lunch",
        "calories": 350,
        "protein": 35,
        "carbs": 20,
        "fat": 15,
        "fiber": 6,
        "serving": "1 bowl (300g)"
    },
    "grilled_salmon": {
        "name": "Grilled Salmon",
        "category": "Western",
        "meal_type": "dinner",
        "calories": 420,
        "protein": 38,
        "carbs": 5,
        "fat": 28,
        "fiber": 0,
        "serving": "1 fillet (200g)"
    },
    "beef_steak": {
        "name": "Beef Steak",
        "category": "Western",
        "meal_type": "dinner",
        "calories": 480,
        "protein": 42,
        "carbs": 8,
        "fat": 32,
        "fiber": 1,
        "serving": "1 piece (250g)"
    },
    "caesar_salad": {
        "name": "Caesar Salad",
        "category": "Western",
        "meal_type": "lunch",
        "calories": 380,
        "protein": 18,
        "carbs": 22,
        "fat": 24,
        "fiber": 4,
        "serving": "1 bowl"
    },
    "spaghetti_bolognese": {
        "name": "Spaghetti Bolognese",
        "category": "Western",
        "meal_type": "lunch",
        "calories": 520,
        "protein": 24,
        "carbs": 68,
        "fat": 16,
        "fiber": 5,
        "serving": "1 plate"
    },
    
    # Fruits
    "banana": {
        "name": "Banana",
        "category": "Fruit",
        "meal_type": "snack",
        "calories": 105,
        "protein": 1.3,
        "carbs": 27,
        "fat": 0.4,
        "fiber": 3,
        "serving": "1 medium (120g)"
    },
    "apple": {
        "name": "Apple",
        "category": "Fruit",
        "meal_type": "snack",
        "calories": 95,
        "protein": 0.5,
        "carbs": 25,
        "fat": 0.3,
        "fiber": 4,
        "serving": "1 medium (180g)"
    },
    "orange": {
        "name": "Orange",
        "category": "Fruit",
        "meal_type": "snack",
        "calories": 62,
        "protein": 1.2,
        "carbs": 15,
        "fat": 0.2,
        "fiber": 3,
        "serving": "1 medium (130g)"
    },
    "mango": {
        "name": "Mango",
        "category": "Fruit",
        "meal_type": "snack",
        "calories": 135,
        "protein": 1.4,
        "carbs": 35,
        "fat": 0.6,
        "fiber": 4,
        "serving": "1 cup (165g)"
    },
    
    # Beverages
    "teh_manis": {
        "name": "Teh Manis",
        "category": "Beverage",
        "meal_type": "snack",
        "calories": 90,
        "protein": 0,
        "carbs": 24,
        "fat": 0,
        "fiber": 0,
        "serving": "1 glass (250ml)"
    },
    "kopi_susu": {
        "name": "Kopi Susu",
        "category": "Beverage",
        "meal_type": "breakfast",
        "calories": 120,
        "protein": 4,
        "carbs": 18,
        "fat": 4,
        "fiber": 0,
        "serving": "1 glass (250ml)"
    },
    "jus_alpukat": {
        "name": "Jus Alpukat",
        "category": "Beverage",
        "meal_type": "snack",
        "calories": 180,
        "protein": 3,
        "carbs": 28,
        "fat": 8,
        "fiber": 4,
        "serving": "1 glass (300ml)"
    },
    
    # Rice & Staples
    "nasi_putih": {
        "name": "Nasi Putih",
        "category": "Staple",
        "meal_type": "lunch",
        "calories": 204,
        "protein": 4.2,
        "carbs": 45,
        "fat": 0.4,
        "fiber": 0.6,
        "serving": "1 cup cooked (158g)"
    },
    "roti_tawar": {
        "name": "Roti Tawar",
        "category": "Staple",
        "meal_type": "breakfast",
        "calories": 160,
        "protein": 6,
        "carbs": 30,
        "fat": 2,
        "fiber": 2,
        "serving": "2 slices"
    },
}


def search_food(query):
    """Search food by name"""
    query = query.lower()
    results = []
    
    for food_id, food_data in FOOD_DATABASE.items():
        if query in food_data["name"].lower():
            results.append({
                "id": food_id,
                **food_data
            })
    
    return results


def get_food_by_category(category):
    """Get foods by category"""
    return [
        {"id": food_id, **food_data}
        for food_id, food_data in FOOD_DATABASE.items()
        if food_data["category"] == category
    ]


def get_food_by_meal_type(meal_type):
    """Get foods by meal type"""
    return [
        {"id": food_id, **food_data}
        for food_id, food_data in FOOD_DATABASE.items()
        if food_data["meal_type"] == meal_type
    ]


def get_all_foods():
    """Get all foods"""
    return [
        {"id": food_id, **food_data}
        for food_id, food_data in FOOD_DATABASE.items()
    ]


def get_food_by_id(food_id):
    """Get food details by ID"""
    return FOOD_DATABASE.get(food_id)


# Quick access lists
INDONESIAN_FOODS = get_food_by_category("Indonesian")
WESTERN_FOODS = get_food_by_category("Western")
FRUITS = get_food_by_category("Fruit")
BEVERAGES = get_food_by_category("Beverage")

BREAKFAST_FOODS = get_food_by_meal_type("breakfast")
LUNCH_FOODS = get_food_by_meal_type("lunch")
DINNER_FOODS = get_food_by_meal_type("dinner")
SNACK_FOODS = get_food_by_meal_type("snack")