import streamlit as st
import math

# ============================================================
# FOODWISE AI
# AI-Based Food Quantity Predictor
# SDG 12 - Responsible Consumption and Production
# ============================================================

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="FoodWise AI",
    page_icon="🍽️",
    layout="wide"
)

# ------------------------------------------------------------
# FOOD DATABASE
# Average quantity per adult
# ------------------------------------------------------------

FOOD_DATABASE = {
    "Rice": {"quantity": 180, "unit": "g"},
    "Biryani": {"quantity": 250, "unit": "g"},
    "Pulao": {"quantity": 200, "unit": "g"},
    "Dal": {"quantity": 150, "unit": "g"},
    "Paneer": {"quantity": 120, "unit": "g"},
    "Vegetable Curry": {"quantity": 130, "unit": "g"},
    "Chole": {"quantity": 140, "unit": "g"},
    "Rajma": {"quantity": 140, "unit": "g"},
    "Chapati": {"quantity": 3, "unit": "pieces"},
    "Poori": {"quantity": 3, "unit": "pieces"},
    "Naan": {"quantity": 2, "unit": "pieces"},
    "Salad": {"quantity": 80, "unit": "g"},
    "Raita": {"quantity": 100, "unit": "g"},
    "Dessert": {"quantity": 100, "unit": "g"},
    "Ice Cream": {"quantity": 100, "unit": "g"},
    "Fruit": {"quantity": 120, "unit": "g"},
    "Snacks": {"quantity": 100, "unit": "g"},
    "Samosa": {"quantity": 2, "unit": "pieces"},
    "Juice": {"quantity": 250, "unit": "ml"},
    "Soft Drink": {"quantity": 250, "unit": "ml"}
}

# ------------------------------------------------------------
# EVENT FACTORS
# ------------------------------------------------------------

EVENT_FACTORS = {
    "Birthday Party": 0.90,
    "Wedding": 1.10,
    "School Function": 0.85,
    "Office Event": 0.90,
    "Festival": 1.05,
    "Family Function": 1.00,
    "Community Event": 0.95,
    "Other": 1.00
}

# ------------------------------------------------------------
# MEAL FACTORS
# ------------------------------------------------------------

MEAL_FACTORS = {
    "Breakfast": 0.75,
    "Lunch": 1.00,
    "Dinner": 1.00,
    "Snacks": 0.60
}

# ------------------------------------------------------------
# APPETITE FACTORS
# ------------------------------------------------------------

APPETITE_FACTORS = {
    "Low": 0.85,
    "Normal": 1.00,
    "High": 1.15
}


# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 45px;
    font-weight: bold;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    margin-bottom: 30px;
}

.info-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #f0f8f0;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.markdown(
    '<div class="main-title">🍽️ FOODWISE AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Based Food Quantity Prediction System'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "🎯 Goal: Predict the required amount of food for an event "
    "and reduce unnecessary food preparation and wastage."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Event Information")

event = st.sidebar.selectbox(
    "Type of Event",
    list(EVENT_FACTORS.keys())
)

meal = st.sidebar.selectbox(
    "Meal Type",
    list(MEAL_FACTORS.keys())
)

adults = st.sidebar.number_input(
    "Number of Adults",
    min_value=0,
    max_value=10000,
    value=50,
    step=1
)

children = st.sidebar.number_input(
    "Number of Children",
    min_value=0,
    max_value=10000,
    value=20,
    step=1
)

appetite = st.sidebar.selectbox(
    "Expected Appetite",
    list(APPETITE_FACTORS.keys())
)


# ============================================================
# MENU SELECTION
# ============================================================

st.subheader("🍛 Select Food Menu")

selected_foods = st.multiselect(
    "Choose the food items you want to prepare:",
    list(FOOD_DATABASE.keys()),
    default=["Rice", "Dal", "Paneer", "Chapati", "Salad", "Dessert"]
)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_quantity(
    food,
    adults,
    children,
    event,
    meal,
    appetite
):

    base_quantity = FOOD_DATABASE[food]["quantity"]
    unit = FOOD_DATABASE[food]["unit"]

    event_factor = EVENT_FACTORS[event]
    meal_factor = MEAL_FACTORS[meal]
    appetite_factor = APPETITE_FACTORS[appetite]

    # Children consume approximately 60% of adult portion
    child_factor = 0.60

    effective_people = adults + (children * child_factor)

    # AI prediction formula

    quantity = (
        base_quantity
        * effective_people
        * event_factor
        * meal_factor
        * appetite_factor
    )

    # Small 5% safety margin
    quantity = quantity * 1.05

    # Convert grams to kilograms
    if unit == "g":

        quantity = quantity / 1000
        unit = "kg"

        quantity = round(quantity, 2)

    elif unit == "ml":

        quantity = quantity / 1000
        unit = "litres"

        quantity = round(quantity, 2)

    else:

        quantity = math.ceil(quantity)

    return quantity, unit


# ============================================================
# CALCULATE BUTTON
# ============================================================

if st.button(
    "🤖 PREDICT REQUIRED FOOD QUANTITY",
    type="primary",
    use_container_width=True
):

    if adults == 0 and children == 0:

        st.error(
            "Please enter at least one adult or child."
        )

    elif len(selected_foods) == 0:

        st.warning(
            "Please select at least one food item."
        )

    else:

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        st.subheader("📋 Event Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Adults",
            adults
        )

        col2.metric(
            "Children",
            children
        )

        col3.metric(
            "Event",
            event
        )

        col4.metric(
            "Meal",
            meal
        )

        # ----------------------------------------------------
        # EFFECTIVE PEOPLE
        # ----------------------------------------------------

        effective_people = adults + (children * 0.60)

        st.write(
            f"👥 **Effective consumption population:** "
            f"{effective_people:.1f} adult-equivalent portions"
        )

        # ----------------------------------------------------
        # FOOD PREDICTION
        # ----------------------------------------------------

        st.subheader("📊 AI Food Quantity Prediction")

        results = []

        for food in selected_foods:

            quantity, unit = predict_quantity(
                food,
                adults,
                children,
                event,
                meal,
                appetite
            )

            results.append(
                {
                    "Food Item": food,
                    "Recommended Quantity": quantity,
                    "Unit": unit
                }
            )

        # ----------------------------------------------------
        # DISPLAY RESULTS
        # ----------------------------------------------------

        for result in results:

            col1, col2, col3 = st.columns([3, 2, 1])

            col1.write(
                f"🍴 **{result['Food Item']}**"
            )

            col2.metric(
                "Quantity",
                f"{result['Recommended Quantity']} "
                f"{result['Unit']}"
            )

            col3.write("✅ Recommended")

        # ----------------------------------------------------
        # WASTE REDUCTION
        # ----------------------------------------------------

        st.divider()

        st.subheader("♻️ Food Waste Reduction Analysis")

        # Traditional catering safety margin
        traditional_margin = 0.15

        # FoodWise AI margin
        ai_margin = 0.05

        traditional_food = (
            effective_people *
            (1 + traditional_margin)
        )

        ai_food = (
            effective_people *
            (1 + ai_margin)
        )

        estimated_reduction = (
            (traditional_food - ai_food)
            / traditional_food
        ) * 100

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Traditional Planning",
            "15% Extra"
        )

        col2.metric(
            "FoodWise AI",
            "5% Safety Margin"
        )

        col3.metric(
            "Estimated Reduction",
            f"{estimated_reduction:.1f}%"
        )

        # ----------------------------------------------------
        # MONEY SAVING ESTIMATE
        # ----------------------------------------------------

        st.subheader("💰 Estimated Cost Saving")

        food_cost = st.number_input(
            "Estimated average food cost per person (₹)",
            min_value=1,
            max_value=10000,
            value=150,
            step=10
        )

        traditional_cost = (
            effective_people *
            (1 + traditional_margin) *
            food_cost
        )

        ai_cost = (
            effective_people *
            (1 + ai_margin) *
            food_cost
        )

        estimated_saving = (
            traditional_cost -
            ai_cost
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Traditional Estimated Cost",
            f"₹{traditional_cost:,.0f}"
        )

        col2.metric(
            "FoodWise AI Cost",
            f"₹{ai_cost:,.0f}"
        )

        col3.metric(
            "Potential Saving",
            f"₹{estimated_saving:,.0f}"
        )

        # ----------------------------------------------------
        # SDG CONNECTION
        # ----------------------------------------------------

        st.divider()

        st.subheader("🌍 SDG Impact")

        st.success(
            """
            **SDG 12 – Responsible Consumption and Production**

            FoodWise AI helps event organizers estimate the required
            quantity of food before preparation. By reducing
            over-preparation, the system can help reduce avoidable
            food waste, unnecessary expenditure and resource usage.

            **Problem → Excess Preparation → Food Waste**

            **AI Solution → Demand Prediction → Better Planning → Less Waste**
            """
        )

        # ----------------------------------------------------
        # AI RECOMMENDATION
        # ----------------------------------------------------

        st.subheader("🤖 FoodWise AI Recommendation")

        if estimated_reduction >= 8:

            recommendation = (
                "The event has a significant opportunity to reduce "
                "over-preparation. Follow the recommended quantities "
                "and monitor actual consumption for future events."
            )

        else:

            recommendation = (
                "The recommended quantities provide a balanced "
                "safety margin while avoiding unnecessary "
                "over-preparation."
            )

        st.info(recommendation)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FOODWISE AI | SDG 12 – Responsible Consumption and Production"
)
