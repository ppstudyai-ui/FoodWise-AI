import streamlit as st

# ============================================================
# JALWISE AI
# AI-Based Clean Water Management System
# SDG 6 - Clean Water and Sanitation
# ============================================================

st.set_page_config(
    page_title="JalWise AI",
    page_icon="💧",
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
    '<div class="main-title">💧 JALWISE AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Based Water Requirement & Conservation System'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "🌍 SDG 6: Clean Water and Sanitation | "
    "Predict water requirements and identify possible excess usage."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🏠 User Information")

location_type = st.sidebar.selectbox(
    "Location Type",
    [
        "Household",
        "School",
        "Office",
        "Community"
    ]
)

people = st.sidebar.number_input(
    "Number of People",
    min_value=1,
    max_value=10000,
    value=5,
    step=1
)

bathrooms = st.sidebar.number_input(
    "Number of Bathrooms",
    min_value=1,
    max_value=100,
    value=2,
    step=1
)

garden_area = st.sidebar.number_input(
    "Garden Area (square metres)",
    min_value=0.0,
    max_value=10000.0,
    value=20.0,
    step=1.0
)

washing_loads = st.sidebar.number_input(
    "Washing Machine Loads per Day",
    min_value=0,
    max_value=100,
    value=1,
    step=1
)

temperature = st.sidebar.slider(
    "Temperature (°C)",
    min_value=10,
    max_value=50,
    value=30
)

previous_usage = st.sidebar.number_input(
    "Previous Daily Water Usage (litres)",
    min_value=0.0,
    max_value=1000000.0,
    value=700.0,
    step=50.0
)


# ============================================================
# AI PREDICTION FUNCTION
# ============================================================

def predict_water_requirement(
    people,
    bathrooms,
    garden_area,
    washing_loads,
    temperature,
    location_type
):

    # --------------------------------------------------------
    # Basic daily requirement
    # --------------------------------------------------------

    # Approximate planning value for demonstration.
    # This is NOT a medical or official water requirement.
    personal_use = people * 135

    # --------------------------------------------------------
    # Bathroom infrastructure factor
    # --------------------------------------------------------

    bathroom_use = bathrooms * 20

    # --------------------------------------------------------
    # Washing machine water requirement
    # --------------------------------------------------------

    washing_use = washing_loads * 70

    # --------------------------------------------------------
    # Garden water requirement
    # --------------------------------------------------------

    garden_use = garden_area * 3

    # --------------------------------------------------------
    # Temperature adjustment
    # --------------------------------------------------------

    if temperature >= 35:
        temperature_factor = 1.15

    elif temperature >= 30:
        temperature_factor = 1.08

    elif temperature <= 20:
        temperature_factor = 0.90

    else:
        temperature_factor = 1.00

    # --------------------------------------------------------
    # Location adjustment
    # --------------------------------------------------------

    if location_type == "School":
        location_factor = 0.80

    elif location_type == "Office":
        location_factor = 0.75

    elif location_type == "Community":
        location_factor = 0.90

    else:
        location_factor = 1.00

    # --------------------------------------------------------
    # AI-style prediction
    # --------------------------------------------------------

    estimated_water = (
        personal_use
        + bathroom_use
        + washing_use
        + garden_use
    )

    estimated_water *= temperature_factor
    estimated_water *= location_factor

    return round(estimated_water, 2)


# ============================================================
# PREDICT BUTTON
# ============================================================

if st.button(
    "🤖 PREDICT WATER REQUIREMENT",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------------

    predicted_water = predict_water_requirement(
        people,
        bathrooms,
        garden_area,
        washing_loads,
        temperature,
        location_type
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    st.subheader("📊 AI Water Prediction")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "People",
        people
    )

    col2.metric(
        "Predicted Requirement",
        f"{predicted_water:,.0f} L/day"
    )

    col3.metric(
        "Current Usage",
        f"{previous_usage:,.0f} L/day"
    )

    difference = previous_usage - predicted_water

    if difference > 0:

        col4.metric(
            "Possible Excess",
            f"{difference:,.0f} L/day"
        )

    else:

        col4.metric(
            "Additional Need",
            f"{abs(difference):,.0f} L/day"
        )


    # ========================================================
    # WATER USAGE ANALYSIS
    # ========================================================

    st.divider()

    st.subheader("💧 Water Usage Analysis")

    if previous_usage > predicted_water * 1.20:

        excess = previous_usage - predicted_water

        st.error(
            f"⚠️ Your estimated usage is approximately "
            f"{excess:,.0f} litres/day higher than the "
            f"predicted requirement."
        )

        status = "High Water Usage"

    elif previous_usage > predicted_water:

        excess = previous_usage - predicted_water

        st.warning(
            f"⚠️ Your usage is approximately "
            f"{excess:,.0f} litres/day above the "
            f"predicted requirement."
        )

        status = "Moderately High"

    else:

        st.success(
            "✅ Your current water usage is within the "
            "predicted requirement range."
        )

        status = "Efficient"


    # ========================================================
    # SAVING POTENTIAL
    # ========================================================

    st.subheader("♻️ Water Saving Potential")

    if previous_usage > predicted_water:

        saving = previous_usage - predicted_water

    else:

        saving = 0

    monthly_saving = saving * 30

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Daily Saving Potential",
        f"{saving:,.0f} L"
    )

    col2.metric(
        "Monthly Saving Potential",
        f"{monthly_saving:,.0f} L"
    )

    col3.metric(
        "Status",
        status
    )


    # ========================================================
    # COST ESTIMATION
    # ========================================================

    st.subheader("💰 Estimated Water Cost")

    water_cost = st.number_input(
        "Estimated cost per 1,000 litres (₹)",
        min_value=1.0,
        max_value=10000.0,
        value=50.0,
        step=5.0
    )

    current_cost = (
        previous_usage / 1000
    ) * water_cost

    predicted_cost = (
        predicted_water / 1000
    ) * water_cost

    possible_saving = (
        current_cost - predicted_cost
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Daily Cost",
        f"₹{current_cost:,.2f}"
    )

    col2.metric(
        "Predicted Daily Cost",
        f"₹{predicted_cost:,.2f}"
    )

    col3.metric(
        "Possible Saving",
        f"₹{max(possible_saving, 0):,.2f}"
    )


    # ========================================================
    # AI RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.subheader("🤖 JalWise AI Recommendations")

    recommendations = []

    if previous_usage > predicted_water * 1.20:

        recommendations.append(
            "Check for leaking taps, pipes and toilets."
        )

    if garden_area > 50:

        recommendations.append(
            "Consider watering plants during early morning "
            "or evening to reduce water loss."
        )

    if washing_loads > 2:

        recommendations.append(
            "Try running the washing machine with full loads."
        )

    if bathrooms > people:

        recommendations.append(
            "Avoid unnecessary water use in multiple bathrooms."
        )

    if temperature >= 35:

        recommendations.append(
            "High temperature may increase water demand. "
            "Use water carefully during hot weather."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Your water usage pattern appears reasonable. "
            "Continue monitoring daily consumption."
        )

    for recommendation in recommendations:

        st.write(
            "🔹 " + recommendation
        )


    # ========================================================
    # SDG 6 IMPACT
    # ========================================================

    st.divider()

    st.subheader("🌍 SDG 6 Impact")

    st.success(
        """
        **SDG 6 – Clean Water and Sanitation**

        JalWise AI promotes responsible water management by
        estimating water requirements and identifying possible
        excessive consumption.

        **Data Input**
        ↓

        **AI Prediction**
        ↓

        **Water Usage Analysis**
        ↓

        **Conservation Recommendation**
        ↓

        **Reduced Water Wastage**
        """
    )


    # ========================================================
    # PROJECT MESSAGE
    # ========================================================

    st.subheader("💡 Why JalWise AI?")

    st.write(
        "Water is a limited resource. Instead of using the same "
        "amount of water every day, JalWise AI estimates water "
        "requirements based on people, facilities, weather and "
        "activities. This can help users make better water-use "
        "decisions."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "JALWISE AI | AI + SDG 6 | Clean Water and Sanitation"
)
