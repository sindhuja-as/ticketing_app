import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from src.data.preprocess import clean_text
from src.inference.predict import predict_and_route
from db.db_utils import save_ticket

# paths
BASE_DIR = Path(__file__).resolve().parent
# DATA_PATH = BASE_DIR / "data" / "predictions" / "ticket_predictions_new.csv"
DB_PATH = BASE_DIR / "data" / "tickets.db"

if "page" not in st.session_state:
    st.session_state.page = "Home"
with st.sidebar:
    st.markdown(
    "<h2 style='text-align: center;'>Ticketing System</h2>",
    unsafe_allow_html=True
)

    if st.button("Home", width='stretch'):
        st.session_state.page = "Home"

    if st.button("Dashboard", width='stretch'):
        st.session_state.page = "Dashboard"

    if st.button("Complaint Status", width='stretch'):
        st.session_state.page = "Status"
# page config
st.set_page_config(
    page_title="Automatic Ticket Categorization",
    layout="wide"
)

# # -------------------------
# # Sidebar items
# # -------------------------
st.title("GAME-ON")
def menu_header(title):
    st.markdown(f"### {title}")
    st.markdown("---")
if st.session_state.page == "Home":
    menu_header("Automatic Ticket Categorization")
    # complaint input UI

elif st.session_state.page == "Dashboard":
    menu_header("Dashboard")
    # dashboard UI

elif st.session_state.page == "Status":
    menu_header("Complaint Status")
    # ticket lookup UI

# # -------------------------
# # Complaint Input Section
# # -------------------------
if st.session_state.page == "Home":
    st.subheader("Submit a Complaint")

    complaint_text = st.text_area(
        "Enter customer complaint",
        height=150
    )

    if st.button("Predict & Route"):
        if complaint_text.strip() == "":
            st.warning("Please enter a complaint text.")
        else:
            cleaned_text = clean_text(complaint_text)
            result = predict_and_route(cleaned_text, complaint_text)
            if result is None:
                st.warning("Please enter a valid complaint")
            else:
                # store_prediction(result)
                save_ticket(result)


                st.success("Ticket created successfully")

                st.metric("Ticket ID", result["ticket_id"])
                st.metric("Category", result["predicted_category"])
                st.metric("Confidence", result["confidence"])
                st.metric("Routed To", result["routed_to"])

# # -------------------------
# # Dashboard Section
# # -------------------------
elif st.session_state.page == "Dashboard":
    st.title("Ticket Dashboard")

    if not DB_PATH.exists():
        st.warning("Database not found. Initializing database...")
    else:
        conn = sqlite3.connect("DB_PATH")
        st.write("DB PATH:", DB_PATH)
        st.write("DB exists:", DB_PATH.exists())
        

        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print("Tables:", cursor.fetchall())
        
        df = pd.read_sql("SELECT * FROM tickets", conn)
        conn.close()

        # FILTERS
        with st.expander("Filters", expanded=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                ticket_id = st.text_input("Ticket ID")

            with col2:
                category = st.selectbox(
                    "Category",
                    options=["All"] + list(df["predicted_category"].unique())
                )

            with col3:
                routed_to = st.selectbox(
                    "Routed To",
                    options=["All"] + list(df["routed_to"].unique())
                )

            status = st.selectbox(
                "Status",
                options=["All"] + list(df["status"].unique())
            )


        # Apply filters
        filtered_df = df.copy()

        if ticket_id:
            filtered_df = filtered_df[filtered_df["ticket_id"].str.contains(ticket_id)]

        if category != "All":
            filtered_df = filtered_df[filtered_df["predicted_category"] == category]

        if routed_to != "All":
            filtered_df = filtered_df[filtered_df["routed_to"] == routed_to]

        if status != "All":
            filtered_df = filtered_df[filtered_df["status"] == status]

        # Sort latest first
        filtered_df = filtered_df.sort_values("created_at", ascending=False)

        st.dataframe(filtered_df, use_container_width=True)

    
# # -------------------------
# # Ticket status Section
# # -------------------------

elif st.session_state.page == "Status":
    st.subheader("Check Complaint Status")

    ticket_id = st.text_input("Enter Ticket ID")

    if st.button("Search"):

        if ticket_id and DB_PATH.exists():
            
            conn = sqlite3.connect("DB_PATH")
            df = pd.read_sql("SELECT * FROM tickets", conn)
            conn.close()
            match = df[df["ticket_id"] == ticket_id]

            if not match.empty:
                st.dataframe(match)
            else:
                st.warning("Ticket not found")
