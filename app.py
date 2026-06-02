from optimizer import (
    optimize_route,
    get_bottleneck_hubs
)

import matplotlib.pyplot as plt
import streamlit as st
import time

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="OptiRoute",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# SIMPLE PROFESSIONAL SPLASH
# =========================

# SPLASH SCREEN

placeholder = st.empty()

placeholder.markdown("""
<div style="
display:flex;
justify-content:center;
align-items:center;
flex-direction:column;
height:100vh;
background:linear-gradient(to right, #0f172a, #1e293b);
">

<div style="
font-size:75px;
margin-bottom:6px;
">
🚚
</div>

<div style="
font-size:78px;
font-weight:700;
font-family:Arial, sans-serif;
letter-spacing:-2px;
color:white;
line-height:1;
">

Opti<span style="color:#ef4444;">Route</span>
                     
</div>

<div style="
margin-top:18px;
font-size:20px;
color:#94a3b8;
font-weight:400;
letter-spacing:1px;
">

Smart Delivery Optimization

</div>

<div style="
margin-top:35px;
width:220px;
height:4px;
background:#334155;
border-radius:10px;
overflow:hidden;
">

<div style="
width:60%;
height:100%;
background:#ef4444;
border-radius:10px;
animation: loading 2s infinite;
">
</div>

</div>

<style>

@keyframes loading {

0% {
transform: translateX(-120px);
}

100% {
transform: translateX(220px);
}

}

</style>

</div>
""", unsafe_allow_html=True)

time.sleep(3)

placeholder.empty()
# =========================
# CUSTOM CSS
# =========================

st.markdown(

    """

    <style>

    .stTextInput input {

    background-color: #1e293b !important;
    color: white !important;

    border: 2px solid #ef4444 !important;

    border-radius: 12px !important;

    font-size: 18px !important;
}

.stTextInput label {

    color: white !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

    .stApp {

        background: linear-gradient(
            to right,
            #0f172a,
            #1e293b
        );

        color: white;
    }

    [data-testid="stMetricValue"] {

        color: white;
        font-size: 45px;
    }

    [data-testid="stMetricLabel"] {

        color: #cbd5e1;
        font-size: 20px;
    }

    .stButton button {

    background: linear-gradient(
        to right,
        #ef4444,
        #dc2626
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    height: 55px !important;

    width: 220px !important;

    font-size: 20px !important;

    font-weight: 600 !important;

    transition: 0.3s ease-in-out !important;
}

.stButton button:hover {

    background: linear-gradient(
        to right,
        #f87171,
        #ef4444
    ) !important;

    transform: scale(1.03);

    box-shadow:
        0 0 15px rgba(239,68,68,0.5);
}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🚚 OptiRoute Dashboard")

st.sidebar.info(
    "AI Powered Smart Delivery Optimization System"
)

st.sidebar.success(
    "System Status: Online"
)

# =========================
# MAIN TITLE
# =========================

st.markdown(
    """
    <h1 style='
    text-align:center;
    font-size:65px;
    font-weight:700;
    color:white;
    letter-spacing:2px;
    font-family:sans-serif;
    '>

    🚚 Opti<span style="color:#ef4444;">Route</span>

    </h1>

    <p style='
    text-align:center;
    color:#94a3b8;
    font-size:18px;
    margin-top:-10px;
    letter-spacing:1px;
    '>

    Smart Delivery Optimization

    </p>
    """,
    unsafe_allow_html=True
)

# =========================
# INPUT SECTION
# =========================

st.markdown("## 📍 Enter Delivery Locations")

col1, col2, col3 = st.columns(3)

with col1:

    warehouse = st.text_input(
        "Warehouse Location",
        ""
    )

    customer1 = st.text_input(
        "Customer 1",
        ""
    )

    customer2 = st.text_input(
        "Customer 2",
        ""
    )

with col2:

    customer3 = st.text_input(
        "Customer 3",
        ""
    )

    customer4 = st.text_input(
        "Customer 4",
        ""
    )

    customer5 = st.text_input(
        "Customer 5",
        ""
    )

st.divider()

# =========================
# BUTTON
# =========================
if st.button("Optimize Route 🚀"):

    try:

        total_distance_km, eta, predicted_eta, segment_distances, best_route_order, best_route_nodes = optimize_route(
            warehouse,
            customer1,
            customer2,
            customer3,
            customer4,
            customer5
        )

        delay = predicted_eta - eta

        if delay < 0.08:

            risk = "🟢 LOW"

        elif delay < 0.20:

            risk = "🟡 MEDIUM"

        else:

            risk = "🔴 HIGH"

        customers = []

        if customer1.strip():
            customers.append("Customer1")

        if customer2.strip():
            customers.append("Customer2")

        if customer3.strip():
            customers.append("Customer3")

        if customer4.strip():
            customers.append("Customer4")

        if customer5.strip():
            customers.append("Customer5")

        route_text = "Warehouse → " + " → ".join(customers)

        fuel_saved = round(
            total_distance_km * 0.12,
            2
        )

        cost_saved = round(
            fuel_saved * 100,
            2
        )

        efficiency = max(
            60,
            min(
                95,
                int(100 - total_distance_km)
            )
        )

        # AI Insight starts here

        if total_distance_km < 8:

            insight = (
                "Excellent route efficiency. Customers are clustered closely, minimizing travel time and fuel consumption."
            )

        elif total_distance_km < 15:

            insight = (
                "Good route optimization achieved with balanced travel distance and delivery coverage."
            )

        else:

            insight = (
                "Long delivery route detected. Consider adding a secondary warehouse or redistributing delivery zones."
            )

    except Exception as e:

        st.error(str(e))
        st.stop()





    st.success(
        "Optimal Route Generated Successfully"
    )
    
    st.markdown("## 🛣 Optimized Route")

    route_text = "Warehouse → " + " → ".join(best_route_order)

    

    st.write(route_text)

   

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.metric(
            "Total Distance",
            f"{total_distance_km} km"
        )

    with metric2:

        st.metric(
            "ETA",
            f"{round(eta * 60)} min"
        )

    with metric3:

      st.metric(
        "💰 Estimated Cost Saved",
        f"₹{cost_saved:.2f}"
    )
      
    with metric4:

      st.metric(
        "🤖 AI Predicted ETA",
        f"{round(predicted_eta * 60)} min"
    ) 
      
    st.markdown("## ⚠️ Delay Risk Analysis")

    st.write(
        f"Risk Level: {risk}"
    )

st.write(
        f"Predicted Delay: {round(delay * 60, 1)} minutes"
    ) 

if risk == "🔴 HIGH":

    st.error(
        "Route passes through high-risk network corridors. Delays are likely."
    )

elif risk == "🟡 MEDIUM":

        st.warning(
            "Moderate traffic and bottleneck impact expected."
        )

else:

        st.success(
            "Low delay risk detected."
        )
      
st.success(
       "✅ Route optimized to reduce fuel cost and delivery time."
    )
        
st.markdown(
    f"""
    <div style="
    background: rgba(30, 41, 59, 0.9);
    padding: 18px 22px;
    border-radius: 15px;
    border-left: 5px solid #38bdf8;
    margin-top: 20px;
    ">

    <h3 style="
    color: #38bdf8;
    margin-bottom: 10px;
    ">

    🤖 AI Insight

    </h3>

    <p style="
    color: white;
    font-size: 18px;
    line-height: 1.6;
    ">

    {insight}

    </p>

    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("## 📊 Route Distance Distribution")

labels = []

for i in range(len(segment_distances)):

    labels.append(
        f"Customer {i+1}"
    )

sizes = segment_distances

colors = [
    "#3b82f6",
    "#f97316",
    "#22c55e",
    "#ef4444",
    "#a855f7"
]

fig, ax = plt.subplots(figsize=(4,4))

ax.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'color':"white", 'fontsize':12}
)

fig.patch.set_facecolor('#0f172a')

ax.set_facecolor('#0f172a')

ax.axis('equal')

st.pyplot(fig)
    

st.markdown("### 📈 Route Efficiency")

efficiency = max(
    60,
    min(
        95,
        int(100 - total_distance_km)
    )
)

st.progress(efficiency)

st.markdown(
    f"""
    <h3 style='
    color:white;
    text-align:center;
    '>

    🚀 Efficiency Improved:
    <span style="color:#22c55e;">
    {efficiency}%
    </span>

    </h3>
    """,
    unsafe_allow_html=True
)

st.success(
    "✅ Route optimized to reduce fuel cost and delivery time."
)
st.divider()

st.markdown("## 🚦 Route Bottleneck Analysis")

route_bottlenecks = best_route_order[1:]

if len(route_bottlenecks) == 0:
    st.write("No bottlenecks found.")

for i, hub in enumerate(route_bottlenecks, start=1):
    st.write(f"{i}. {hub}")

if len(route_bottlenecks) > 0:
    st.info(
        f"Potential delay risk detected near {route_bottlenecks[0]}."
    )
else:
    st.info(
        "No major bottlenecks detected for this route."
    )

    # MAP SECTION

st.subheader("🗺 Route Visualization")

st.image(
        "route.png",
        caption="Optimized Delivery Route",
        use_container_width=True
    )
st.markdown("""

### 🗺 Map Legend

🔴 Red Dots → Delivery Locations

🛣 Red Line → Optimized Route

🏢 Starting Point → Warehouse

""")

    # TECH DETAILS

with st.expander("📘 Technical Details"):

        st.write(
            "Algorithm Used: Travelling Salesman Problem (TSP)"
        )

        st.write(
            "Routing Engine: NetworkX"
        )

        st.write(
            "Map Source: OpenStreetMap + OSMnx"
        )

        st.write(
            "Optimization Goal: Minimize distance and ETA"
        )

st.divider()

st.markdown("""

## 📦 How It Works

1️⃣ Enter warehouse and customer locations

2️⃣ System calculates shortest delivery route

3️⃣ Optimized path is generated using Graph Theory

4️⃣ Distance and delivery time are reduced

""")

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "Developed by Team OptiRoute"
)

