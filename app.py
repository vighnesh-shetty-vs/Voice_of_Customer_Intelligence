import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import time
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="VoC Intelligence Pro", page_icon="📈", layout="wide")

# --- SIDEBAR: SETUP & FILTERS ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # 1. API Key Input
    api_key = st.text_input(
        "Enter Google API Key", 
        type="password", 
        help="Get your free key at aistudio.google.com"
    )
    if not api_key:
        st.warning("⚠️ Enter API Key to analyze.")

    st.divider()
    
    # 2. Data Input
    st.markdown("### 📂 Data Input")
    uploaded_file = st.file_uploader("Upload Reviews (CSV/Excel)", type=["csv", "xlsx"])
    
    # Mock Data with Dates
    if st.button("🎲 Generate Demo Data (with Dates)"):
        # Create dates over the last 30 days
        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(30)]
        
        data_rows = []
        topics = ["Shipping", "Quality", "Support", "Pricing"]
        sentiments = ["Positive", "Negative", "Neutral"]
        
        # Generate 50 rows
        for i in range(50):
            data_rows.append({
                "Review_ID": 1000 + i,
                "Date": date_list[i % 30], # Cycle through dates
                "Review_Text": f"Sample review {i} regarding {topics[i%4]}. It was {sentiments[i%3]}.",
                # We add dummy columns so the app works before analysis too
                "Customer_Name": f"User_{i}"
            })
            
        st.session_state['data'] = pd.DataFrame(data_rows)
        st.success("Demo Data Loaded! Go to 'Run Analysis'.")

    st.divider()
    st.markdown("### 🔍 Global Filters")
    st.info("Run analysis first to unlock filters.")

# --- HELPER FUNCTIONS ---
def analyze_batch_reviews(model, reviews):
    prompt = f"""
    Act as a Senior Data Analyst. Analyze these reviews.
    For EACH review, return a JSON object with:
    1. "sentiment": "Positive", "Negative", or "Neutral".
    2. "topic": One word category (e.g., Shipping, Pricing, Quality, Support).
    3. "keywords": A list of 2-3 key phrases (e.g., ["slow delivery", "bad packaging"]).
    4. "actionable_insight": A short recommendation (max 5 words).
    
    Return ONLY a valid JSON List.
    Reviews: {json.dumps(reviews)}
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception:
        return []

# --- MAIN APP ---
st.title("📈 VoC Intelligence Pro")
st.markdown("Real-time Customer Sentiment, Trend Analysis & Strategic Insights.")

if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
    except:
        model = genai.GenerativeModel('gemini-2.0-flash')

    # Load Data
    df = None
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    elif 'data' in st.session_state:
        df = st.session_state['data']

    if df is not None:
        # Detect Columns
        cols = df.columns
        text_col = st.sidebar.selectbox("Review Column", cols, index=0)
        
        # Date Column Detection (Optional)
        date_col = None
        date_candidates = [c for c in cols if 'date' in c.lower() or 'time' in c.lower()]
        if date_candidates:
            date_col = st.sidebar.selectbox("Date Column (Optional)", [None] + list(cols), index=list(cols).index(date_candidates[0]) + 1)
        else:
            date_col = st.sidebar.selectbox("Date Column (Optional)", [None] + list(cols))

        # --- TABS ---
        tab1, tab2, tab3 = st.tabs(["🚀 Run Analysis", "📊 Executive Dashboard", "📝 Raw Data"])

        # --- TAB 1: RUN ANALYSIS ---
        with tab1:
            st.info(f"Loaded {len(df)} rows.")
            if st.button("🚀 Start Advanced Analysis"):
                progress = st.progress(0, text="AI is analyzing trends...")
                all_results = []
                reviews = df[text_col].astype(str).tolist()
                
                # Batch Processing
                batch_size = 8 
                for i in range(0, len(reviews), batch_size):
                    batch = reviews[i:i+batch_size]
                    res = analyze_batch_reviews(model, batch)
                    if len(res) != len(batch):
                         res = [{"sentiment": "Error", "topic": "Error", "keywords": [], "actionable_insight": "Error"} for _ in batch]
                    all_results.extend(res)
                    progress.progress((i + len(batch)) / len(reviews))
                    time.sleep(0.5)
                
                progress.empty()
                
                # Merge Results
                res_df = pd.DataFrame(all_results)
                final_df = pd.concat([df.reset_index(drop=True), res_df], axis=1)
                
                # Ensure Date is datetime
                if date_col:
                    final_df[date_col] = pd.to_datetime(final_df[date_col], errors='coerce')
                
                st.session_state['analyzed_data'] = final_df
                st.success("Analysis Complete! Switch to Dashboard.")

        # --- TAB 2: DASHBOARD ---
        with tab2:
            if 'analyzed_data' in st.session_state:
                data = st.session_state['analyzed_data']
                valid_data = data[data['sentiment'] != "Error"]

                # --- SIDEBAR FILTERS (ACTIVE NOW) ---
                st.sidebar.markdown("---")
                st.sidebar.header("🎛️ Filters")
                
                # Filter by Topic
                all_topics = valid_data['topic'].unique().tolist()
                selected_topics = st.sidebar.multiselect("Filter by Topic", all_topics, default=all_topics)
                
                # Apply Filter
                filtered_data = valid_data[valid_data['topic'].isin(selected_topics)]

                # --- KPI ROW ---
                kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                
                total = len(filtered_data)
                pos = len(filtered_data[filtered_data['sentiment']=='Positive'])
                neg = len(filtered_data[filtered_data['sentiment']=='Negative'])
                neu = len(filtered_data[filtered_data['sentiment']=='Neutral'])
                
                # NPS Calculation (Proxy: %Pos - %Neg) * 100
                nps = round(((pos - neg) / total) * 100) if total > 0 else 0
                
                kpi1.metric("Total Reviews", total)
                kpi2.metric("Positive %", f"{round(pos/total*100)}%" if total else "0%")
                kpi3.metric("Negative %", f"{round(neg/total*100)}%" if total else "0%")
                kpi4.metric("NPS Score", nps, delta=nps)

                st.divider()

                # --- ROW 2: TIME SERIES & TOPICS ---
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.subheader("📈 Sentiment Over Time")
                    if date_col:
                        # Group by Date and Sentiment
                        timeline = filtered_data.groupby([filtered_data[date_col].dt.date, 'sentiment']).size().reset_index(name='count')
                        fig_line = px.line(timeline, x=date_col, y='count', color='sentiment', 
                                           color_discrete_map={'Positive':'green', 'Negative':'red', 'Neutral':'gray'},
                                           markers=True)
                        st.plotly_chart(fig_line, use_container_width=True)
                    else:
                        st.info("⚠️ No Date column selected. Time-series unavailable.")

                with c2:
                    st.subheader("🔥 Top Issues")
                    neg_only = filtered_data[filtered_data['sentiment']=='Negative']
                    if not neg_only.empty:
                        fig_bar = px.bar(neg_only['topic'].value_counts().reset_index(), 
                                         x='topic', y='count', color='topic',
                                         title="Complaints by Topic")
                        st.plotly_chart(fig_bar, use_container_width=True)
                    else:
                        st.success("No negative issues in this filter selection!")

                # --- ROW 3: DETAILED INSIGHTS ---
                st.subheader("💡 Strategic Recommendations")
                st.dataframe(
                    filtered_data[['Date' if date_col else text_col, 'sentiment', 'topic', 'keywords', 'actionable_insight']],
                    column_config={
                        "keywords": st.column_config.ListColumn("Key Phrases"),
                        "actionable_insight": st.column_config.TextColumn("AI Action Plan", width="large")
                    },
                    use_container_width=True
                )

            else:
                st.warning("Please run the analysis first.")

        # --- TAB 3: RAW DATA ---
        with tab3:
            st.dataframe(df)

elif not api_key:
    st.info("👈 Enter API Key to begin.")