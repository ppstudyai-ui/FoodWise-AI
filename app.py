import streamlit as st
import math

# ============================================================
# ANNSEVA AI
# AI-Based Food Security & Demand Prediction System
# SDG 2 - Zero Hunger
# ============================================================

st.set_page_config(
    page_title="AnnSeva AI",
    page_icon="🌾",
    layout="wide"
)

# ============================================================
# PAGE DESIGN
# ============================================================

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
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌾 ANNSEVA AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Based Food Security & Demand Prediction System'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "🌍 SDG 2 – Zero Hunger | "
    "Predict food requirements and identify possible food shortages."
)


# ============================================================
# FOOD DATABASE
# ============================================================

FOOD_DATABASE = {

    "Rice": {
        "quantity": 180,
        "unit": "kg/person/day"
    },

    "Wheat Flour": {
        "quantity": 120,
        "unit": "kg/person/day"
    },

    "Dal": {
        "quantity": 60,
        "unit": "kg/person/day"
    },

    "Vegetables": {
        "quantity": 150,
        "unit": "kg/person/day"
    },

    "Potatoes": {
        "quantity": 100,
        "unit": "kg/person/day"
    },

    "Milk": {
        "quantity": 200,
        "unit": "litres/person/day"
    },

    "Fruits": {
        "quantity": 100,
        "unit": "kg/person/day"
    }
}


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("👥 Community Information")

adults = st.sidebar.number_input(
    "Number of Adults",
    min_value=0,
    max_value=100000,
    value=100,
    step=10
)

children = st.sidebar.number_input(
    "Number of Children",
    min_value=0,
    max_value=100000,
    value=50,
    step=10
)

days = st.sidebar.number_input(
    "Planning Period (Days)",
    min_value=1,
    max_value=365,
    value=7,
    step=1
)

meals_per_day = st.sidebar.selectbox(
    "Meals Per Day",
    [1, 2, 3]
)

activity_level = st.sidebar.selectbox(
    "Community Activity Level",
    [
        "Low",
        "Normal",
        "High"
    ]
)


# ============================================================
# FOOD SELECTION
# ============================================================

st.subheader("🍚 Select Food Items")

selected_foods = st.multiselect(
    "Choose food items to plan:",
    list(FOOD_DATABASE.keys()),
    default=[
        "Rice",
        "Dal",
        "Vegetables"
    ]
)


# ============================================================
# FOOD REQUIREMENT FUNCTION
# ============================================================

def calculate_food_requirement(
    food,
    adults,
    children,
    days,
    meals_per_day,
    activity_level
):

    base_quantity = FOOD_DATABASE[food]["quantity"]

    # Children are treated as approximately
    # 60% of an adult-equivalent portion.
    effective_people = (
        adults +
        (children * 0.60)
    )

    # Activity adjustment
    if activity_level == "High":

        activity_factor = 1.10

    elif activity_level == "Low":

        activity_factor = 0.90

    else:

        activity_factor = 1.00

    # Food requirement
    quantity = (
        base_quantity
        * effective_people
        * days
        * meals_per_day
        * activity_factor
    )

    return round(quantity, 2)


# ============================================================
# PREDICT BUTTON
# ============================================================

if st.button(
    "🤖 PREDICT FOOD REQUIREMENT",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    total_people = adults + children

    if total_people == 0:

        st.error(
            "Please enter at least one adult or child."
        )

    elif len(selected_foods) == 0:

        st.warning(
            "Please select at least one food item."
        )

    else:

        # ----------------------------------------------------
        # COMMUNITY SUMMARY
        # ----------------------------------------------------

        st.subheader("👥 Community Summary")

        effective_people = (
            adults +
            (children * 0.60)
        )

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
            "Total People",
            total_people
        )

        col4.metric(
            "Adult Equivalent",
            f"{effective_people:.0f}"
        )


        # ----------------------------------------------------
        # FOOD PREDICTION
        # ----------------------------------------------------

        st.divider()

        st.subheader("🌾 AI Food Requirement Prediction")

        predictions = []

        for food in selected_foods:

            quantity = calculate_food_requirement(
                food,
                adults,
                children,
                days,
                meals_per_day,
                activity_level
            )

            predictions.append(
                {
                    "Food": food,
                    "Required": quantity
                }
            )

        for item in predictions:

            col1, col2 = st.columns([3, 2])

            col1.write(
                f"🍚 **{item['Food']}**"
            )

            col2.metric(
                "Required Quantity",
                f"{item['Required']:,.0f} kg"
            )


        # ----------------------------------------------------
        # FOOD STOCK CHECK
        # ----------------------------------------------------

        st.divider()

        st.subheader("📦 Check Available Food Stock")

        st.write(
            "Enter the currently available quantity "
            "for each selected food item."
        )

        stock_data = {}

        for food in selected_foods:

            stock = st.number_input(
                f"Available {food} (kg)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                key=f"stock_{food}"
            )

            stock_data[food] = stock


        # ----------------------------------------------------
        # STOCK ANALYSIS
        # ----------------------------------------------------

        st.divider()

        st.subheader("📊 Food Security Analysis")

        for item in predictions:

            food = item["Food"]

            required = item["Required"]

            available = stock_data[food]

            difference = available - required

            if available >= required:

                st.success(
                    f"✅ {food}: Sufficient stock. "
                    f"Surplus ≈ {difference:,.0f} kg"
                )

            else:

                shortage = abs(difference)

                st.error(
                    f"⚠️ {food}: Possible shortage of "
                    f"{shortage:,.0f} kg"
                )


        # ----------------------------------------------------
        # PEOPLE AT RISK
        # ----------------------------------------------------

        st.divider()

        st.subheader("👥 Food Coverage Prediction")

        coverage_results = []

        for item in predictions:

            food = item["Food"]

            required = item["Required"]

            available = stock_data[food]

            if required > 0:

                coverage = (
                    available /
                    required
                ) * 100

            else:

                coverage = 100

            coverage = min(coverage, 100)

            coverage_results.append(
                coverage
            )

        average_coverage = (
            sum(coverage_results) /
            len(coverage_results)
        )

        estimated_people_served = (
            total_people *
            average_coverage /
            100
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Food Coverage",
            f"{average_coverage:.1f}%"
        )

        col2.metric(
            "Estimated People Served",
            f"{estimated_people_served:,.0f}"
        )

        col3.metric(
            "Coverage Gap",
            f"{100 - average_coverage:.1f}%"
        )


        # ----------------------------------------------------
        # AI RECOMMENDATIONS
        # ----------------------------------------------------

        st.divider()

        st.subheader("🤖 AnnSeva AI Recommendations")

        recommendations = []

        for item in predictions:

            food = item["Food"]

            required = item["Required"]

            available = stock_data[food]

            if available < required:

                shortage = required - available

                recommendations.append(
                    f"Arrange approximately "
                    f"{shortage:,.0f} kg additional "
                    f"{food}."
                )

            elif available > required * 1.30:

                surplus = available - required

                recommendations.append(
                    f"{food} has a possible surplus of "
                    f"{surplus:,.0f} kg. Consider sharing "
                    f"with another food distribution centre."
                )


        if average_coverage < 70:

            recommendations.append(
                "⚠️ Food availability is significantly "
                "below predicted demand. Consider arranging "
                "additional supplies or community support."
            )

        elif average_coverage < 100:

            recommendations.append(
                "⚠️ Some food items may not be sufficient "
                "for the complete planning period."
            )

        else:

            recommendations.append(
                "✅ Current food stock appears sufficient "
                "for the selected planning period."
            )


        for recommendation in recommendations:

            st.write(
                "🔹 " + recommendation
            )


        # ----------------------------------------------------
        # SDG 2 IMPACT
        # ----------------------------------------------------

        st.divider()

        st.subheader("🌍 SDG 2 – ZERO HUNGER")

        st.success(
            """
            **AnnSeva AI supports SDG 2 by helping communities
            plan food requirements according to expected demand.**

            The system can help identify possible food shortages
            before they occur and support better distribution
            planning.

            **Community Data**
            ↓

            **AI Demand Prediction**
            ↓

            **Food Requirement**
            ↓

            **Stock Analysis**
            ↓

            **Shortage Detection**
            ↓

            **Food Distribution Recommendation**
            """
        )


        # ----------------------------------------------------
        # FINAL MESSAGE
        # ----------------------------------------------------

        st.subheader("💡 Project Goal")

        st.write(
            "The goal of AnnSeva AI is not simply to calculate "
            "food quantities. It is to help communities make "
            "better food-planning decisions so that available "
            "resources can reach the people who need them."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ANNSEVA AI | AI + SDG 2 | Zero Hunger"
)
