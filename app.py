import streamlit as st
import math

# ============================================================
# BUILDWISE AI
# AI-Based House Material & Cost Estimator
# Educational Prototype
# ============================================================

st.set_page_config(
    page_title="BuildWise AI",
    page_icon="🏠",
    layout="wide"
)

# ============================================================
# PAGE TITLE
# ============================================================

st.markdown(
    """
    <h1 style="text-align:center;">🏠 BUILDWISE AI</h1>
    <p style="text-align:center; font-size:20px;">
    AI-Based House Material & Construction Cost Estimator
    </p>
    """,
    unsafe_allow_html=True
)

st.info(
    "🤖 Enter your house requirements and BuildWise AI will "
    "estimate the approximate construction materials and cost."
)

st.warning(
    "⚠️ Educational estimation only. Actual construction "
    "requirements must be calculated by qualified architects "
    "and structural engineers."
)


# ============================================================
# SIDEBAR - HOUSE INPUT
# ============================================================

st.sidebar.header("🏠 House Requirements")

land_area = st.sidebar.number_input(
    "Land / Plot Area (sq ft)",
    min_value=100.0,
    max_value=100000.0,
    value=1500.0,
    step=100.0
)

floors = st.sidebar.number_input(
    "Number of Floors",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

bedrooms = st.sidebar.number_input(
    "Number of Bedrooms",
    min_value=0,
    max_value=20,
    value=3,
    step=1
)

bathrooms = st.sidebar.number_input(
    "Number of Bathrooms",
    min_value=0,
    max_value=20,
    value=2,
    step=1
)

living_rooms = st.sidebar.number_input(
    "Living Rooms",
    min_value=0,
    max_value=10,
    value=1,
    step=1
)

dining_rooms = st.sidebar.number_input(
    "Dining Rooms",
    min_value=0,
    max_value=10,
    value=1,
    step=1
)

kitchens = st.sidebar.number_input(
    "Kitchens",
    min_value=0,
    max_value=10,
    value=1,
    step=1
)

parking_spaces = st.sidebar.number_input(
    "Parking Spaces",
    min_value=0,
    max_value=10,
    value=1,
    step=1
)

balconies = st.sidebar.number_input(
    "Balconies",
    min_value=0,
    max_value=20,
    value=1,
    step=1
)


# ============================================================
# CONSTRUCTION QUALITY
# ============================================================

quality = st.sidebar.selectbox(
    "Construction Quality",
    [
        "Economy",
        "Standard",
        "Premium"
    ]
)


# ============================================================
# LOCATION / COST LEVEL
# ============================================================

location_level = st.sidebar.selectbox(
    "Construction Cost Level",
    [
        "Low Cost Area",
        "Average Cost Area",
        "High Cost Area"
    ]
)


# ============================================================
# MATERIAL COST DATABASE
# ============================================================

material_prices = {

    "Cement": 420,        # ₹ per bag
    "Steel": 65,          # ₹ per kg
    "Bricks": 10,         # ₹ per piece
    "Sand": 1800,         # ₹ per cubic metre
    "Aggregate": 1600,    # ₹ per cubic metre
    "Tiles": 70,          # ₹ per sq ft
    "Paint": 35           # ₹ per sq ft
}


# ============================================================
# COST MULTIPLIERS
# ============================================================

quality_factor = {

    "Economy": 0.90,
    "Standard": 1.00,
    "Premium": 1.25
}


location_factor = {

    "Low Cost Area": 0.90,
    "Average Cost Area": 1.00,
    "High Cost Area": 1.20
}


# ============================================================
# ROOM SPACE ESTIMATION
# ============================================================

def estimate_house_area():

    # Approximate space allocation
    bedroom_area = bedrooms * 120

    bathroom_area = bathrooms * 45

    living_area = living_rooms * 180

    dining_area = dining_rooms * 120

    kitchen_area = kitchens * 100

    parking_area = parking_spaces * 180

    balcony_area = balconies * 50

    estimated_required_area = (
        bedroom_area
        + bathroom_area
        + living_area
        + dining_area
        + kitchen_area
        + parking_area
        + balcony_area
    )

    return estimated_required_area


# ============================================================
# MATERIAL ESTIMATION
# ============================================================

def estimate_materials(construction_area):

    # Approximate educational planning factors.
    # These are NOT structural design values.

    cement_per_sqft = 0.40
    steel_per_sqft = 4.0
    bricks_per_sqft = 8.0
    sand_per_sqft = 0.015
    aggregate_per_sqft = 0.012

    # Quality adjustment
    q_factor = quality_factor[quality]

    cement_bags = (
        construction_area
        * cement_per_sqft
        * q_factor
    )

    steel_kg = (
        construction_area
        * steel_per_sqft
        * q_factor
    )

    bricks = (
        construction_area
        * bricks_per_sqft
        * q_factor
    )

    sand_m3 = (
        construction_area
        * sand_per_sqft
        * q_factor
    )

    aggregate_m3 = (
        construction_area
        * aggregate_per_sqft
        * q_factor
    )

    # Approximate floor finishing area
    tiles_area = construction_area * 0.75

    # Approximate paint area
    paint_area = construction_area * 3.0

    return {
        "Cement": round(cement_bags),
        "Steel": round(steel_kg),
        "Bricks": round(bricks),
        "Sand": round(sand_m3, 2),
        "Aggregate": round(aggregate_m3, 2),
        "Tiles": round(tiles_area),
        "Paint": round(paint_area)
    }


# ============================================================
# COST CALCULATION
# ============================================================

def calculate_cost(materials):

    location_multiplier = location_factor[
        location_level
    ]

    costs = {}

    costs["Cement"] = (
        materials["Cement"]
        * material_prices["Cement"]
    )

    costs["Steel"] = (
        materials["Steel"]
        * material_prices["Steel"]
    )

    costs["Bricks"] = (
        materials["Bricks"]
        * material_prices["Bricks"]
    )

    costs["Sand"] = (
        materials["Sand"]
        * material_prices["Sand"]
    )

    costs["Aggregate"] = (
        materials["Aggregate"]
        * material_prices["Aggregate"]
    )

    costs["Tiles"] = (
        materials["Tiles"]
        * material_prices["Tiles"]
    )

    costs["Paint"] = (
        materials["Paint"]
        * material_prices["Paint"]
    )

    # Location adjustment
    for item in costs:

        costs[item] = (
            costs[item]
            * location_multiplier
        )

    return costs


# ============================================================
# AI RECOMMENDATION ENGINE
# ============================================================

def generate_recommendations(
    land_area,
    construction_area,
    bedrooms,
    bathrooms,
    parking_spaces,
    quality
):

    recommendations = []

    # Plot utilization
    utilization = (
        construction_area /
        land_area
    ) * 100

    if utilization > 90:

        recommendations.append(
            "🏠 The estimated built-up area is very high "
            "compared with the plot area. Consider leaving "
            "adequate open space."
        )

    elif utilization < 50:

        recommendations.append(
            "🌱 A significant part of the plot may remain "
            "open. Consider using it for landscaping or "
            "rainwater management."
        )

    else:

        recommendations.append(
            "✅ The estimated space allocation is reasonably "
            "balanced for this prototype."
        )

    # Bathroom recommendation

    if bathrooms > bedrooms + 1:

        recommendations.append(
            "🚿 The number of bathrooms is relatively high "
            "compared with bedrooms. Review the requirement."
        )

    # Parking recommendation

    if parking_spaces == 0:

        recommendations.append(
            "🚗 No parking space has been included."
        )

    # Quality recommendation

    if quality == "Premium":

        recommendations.append(
            "⭐ Premium materials may significantly increase "
            "the project budget."
        )

    # Sustainability recommendation

    recommendations.append(
        "🌧️ Consider rainwater harvesting to improve "
        "water sustainability."
    )

    recommendations.append(
        "☀️ Consider solar panels to reduce long-term "
        "energy consumption."
    )

    recommendations.append(
        "🌿 Consider natural lighting and ventilation "
        "to reduce electricity use."
    )

    return recommendations


# ============================================================
# MAIN BUTTON
# ============================================================

if st.button(
    "🤖 GENERATE AI HOUSE ESTIMATE",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------------------
    # Estimate house area
    # --------------------------------------------------------

    room_area = estimate_house_area()

    # Cannot exceed plot area
    construction_area = min(
        room_area,
        land_area * 0.90
    )

    total_built_area = (
        construction_area * floors
    )

    # --------------------------------------------------------
    # MATERIAL PREDICTION
    # --------------------------------------------------------

    materials = estimate_materials(
        total_built_area
    )

    # --------------------------------------------------------
    # COST
    # --------------------------------------------------------

    costs = calculate_cost(materials)

    total_material_cost = sum(
        costs.values()
    )


    # ========================================================
    # HOUSE SUMMARY
    # ========================================================

    st.subheader("🏠 House Planning Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Land Area",
        f"{land_area:,.0f} sq ft"
    )

    col2.metric(
        "Estimated Floor Area",
        f"{construction_area:,.0f} sq ft"
    )

    col3.metric(
        "Floors",
        floors
    )

    col4.metric(
        "Total Built-up Area",
        f"{total_built_area:,.0f} sq ft"
    )


    # ========================================================
    # ROOM SUMMARY
    # ========================================================

    st.divider()

    st.subheader("🛏️ House Requirements")

    room_col1, room_col2, room_col3 = st.columns(3)

    room_col1.write(
        f"🛏️ Bedrooms: **{bedrooms}**"
    )

    room_col1.write(
        f"🚿 Bathrooms: **{bathrooms}**"
    )

    room_col1.write(
        f"🛋️ Living Rooms: **{living_rooms}**"
    )

    room_col2.write(
        f"🍽️ Dining Rooms: **{dining_rooms}**"
    )

    room_col2.write(
        f"🍳 Kitchens: **{kitchens}**"
    )

    room_col2.write(
        f"🚗 Parking Spaces: **{parking_spaces}**"
    )

    room_col3.write(
        f"🌿 Balconies: **{balconies}**"
    )

    room_col3.write(
        f"🏗️ Quality: **{quality}**"
    )

    room_col3.write(
        f"📍 Cost Level: **{location_level}**"
    )


    # ========================================================
    # MATERIAL PREDICTION
    # ========================================================

    st.divider()

    st.subheader(
        "🧱 AI-Predicted Construction Materials"
    )

    material_units = {

        "Cement": "bags",

        "Steel": "kg",

        "Bricks": "pieces",

        "Sand": "m³",

        "Aggregate": "m³",

        "Tiles": "sq ft",

        "Paint": "sq ft"
    }

    for material in materials:

        col1, col2 = st.columns([3, 2])

        col1.write(
            f"🔹 **{material}**"
        )

        col2.metric(
            "Estimated Requirement",
            f"{materials[material]:,.0f} "
            f"{material_units[material]}"
        )


    # ========================================================
    # COST TABLE
    # ========================================================

    st.divider()

    st.subheader(
        "💰 Estimated Material Cost"
    )

    for material in costs:

        col1, col2 = st.columns([3, 2])

        col1.write(
            f"🧱 **{material}**"
        )

        col2.metric(
            "Estimated Cost",
            f"₹{costs[material]:,.0f}"
        )


    # ========================================================
    # TOTAL COST
    # ========================================================

    st.divider()

    st.subheader(
        "💵 Total Estimated Material Cost"
    )

    st.metric(
        "Estimated Material Cost",
        f"₹{total_material_cost:,.0f}"
    )

    st.caption(
        "This is an approximate material-only estimate "
        "based on demonstration assumptions."
    )


    # ========================================================
    # COST RANGE
    # ========================================================

    lower_estimate = total_material_cost * 0.90
    upper_estimate = total_material_cost * 1.15

    st.info(
        f"Estimated material cost range: "
        f"₹{lower_estimate:,.0f} – "
        f"₹{upper_estimate:,.0f}"
    )


    # ========================================================
    # AI RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.subheader(
        "🤖 BuildWise AI Recommendations"
    )

    recommendations = generate_recommendations(
        land_area,
        construction_area,
        bedrooms,
        bathrooms,
        parking_spaces,
        quality
    )

    for recommendation in recommendations:

        st.write(
            recommendation
        )


    # ========================================================
    # SUSTAINABLE BUILDING
    # ========================================================

    st.divider()

    st.subheader(
        "🌱 Sustainable Building Suggestions"
    )

    sustainable_col1, sustainable_col2 = st.columns(2)

    with sustainable_col1:

        st.write(
            "☀️ **Solar Energy**"
        )

        st.write(
            "Consider rooftop solar panels to "
            "reduce dependence on grid electricity."
        )

        st.write(
            "🌧️ **Rainwater Harvesting**"
        )

        st.write(
            "Collect rainwater for gardening and "
            "other suitable non-drinking uses."
        )

    with sustainable_col2:

        st.write(
            "💡 **Natural Lighting**"
        )

        st.write(
            "Use windows and suitable building "
            "orientation to improve daylight."
        )

        st.write(
            "🌬️ **Natural Ventilation**"
        )

        st.write(
            "Plan windows and openings to encourage "
            "natural airflow."
        )


    # ========================================================
    # AI EXPLANATION
    # ========================================================

    st.divider()

    st.subheader(
        "🧠 How BuildWise AI Works"
    )

    st.write(
        """
        BuildWise AI uses the user's house requirements,
        estimated built-up area, construction quality and
        cost level to calculate approximate material needs.

        The system applies predefined prediction factors
        to estimate cement, steel, bricks, sand, aggregate,
        tiles and paint.

        **User Input**
        ↓

        **House Area Estimation**
        ↓

        **AI Prediction Model**
        ↓

        **Material Requirement**
        ↓

        **Cost Estimation**
        ↓

        **Construction Recommendations**
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏠 BUILDWISE AI | AI-Based Construction Estimation "
    "| Educational Prototype"
)
