import streamlit as st
import pandas as pd
import numpy as np 
import os

# Set page layout & configuration
st.set_page_config(
    page_title="Student Marks Analysis Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
        .main-header {
            font-size: 2.3rem;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #64748B;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2563EB;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .stAlert {
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)


def calculate_grade(percentage):
    """Assign letter grade based on overall percentage."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


@st.cache_data
def load_default_data():
    """Load default sample dataset from local CSV file if available."""
    default_path = os.path.join(os.path.dirname(__file__), "sample_student_marks.csv")
    if os.path.exists(default_path):
        return pd.read_csv(default_path)
    else:
        # Fallback generated dataframe if sample CSV is missing
        data = {
            "Student_ID": ["STD101", "STD101", "STD102", "STD102", "STD103", "STD103"],
            "Name": ["Aarav Sharma", "Aarav Sharma", "Ananya Patel", "Ananya Patel", "Rohan Verma", "Rohan Verma"],
            "Class": ["Class 10"] * 6,
            "Semester": ["Semester 1", "Semester 2"] * 3,
            "Mathematics": [88, 92, 95, 98, 72, 78],
            "Science": [92, 95, 89, 94, 68, 74],
            "English": [85, 88, 92, 95, 75, 80],
            "History": [78, 82, 90, 93, 80, 84],
            "Computer_Science": [95, 98, 94, 97, 82, 88]
        }
        return pd.DataFrame(data)


def process_dataframe(df):
    """Clean data and add calculated fields (Total Marks, Percentage, Grade, Status)."""
    df = df.copy()
    
    # Standardize column names
    subject_cols = [col for col in ["Mathematics", "Science", "English", "History", "Computer_Science"] if col in df.columns]
    
    if not subject_cols:
        # Auto-detect numeric columns as subjects if standard names aren't present
        subject_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Convert subject columns to numeric
    for col in subject_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Calculate totals & percentages
    max_possible_per_subject = 100
    total_max_marks = len(subject_cols) * max_possible_per_subject
    
    df["Total_Marks"] = df[subject_cols].sum(axis=1)
    df["Percentage"] = (df["Total_Marks"] / total_max_marks * 100).round(2)
    df["Grade"] = df["Percentage"].apply(calculate_grade)
    df["Status"] = df["Percentage"].apply(lambda p: "Pass" if p >= 50 else "Fail")
    
    return df, subject_cols


# ==========================================
# SIDEBAR CONTROLS & FILE UPLOADER
# ==========================================
st.sidebar.image("https://img.icons8.com/isometric-folders/100/graduation-cap.png", width=70)
st.sidebar.title("Dashboard Options")

st.sidebar.subheader("📁 Data Input Source")
# Feature 1: st.file_uploader()
uploaded_file = st.sidebar.file_uploader(
    "Upload Student Marks CSV",
    type=["csv"],
    help="Upload a CSV file containing student marks to analyze custom data."
)

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        st.sidebar.success("Custom CSV uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading CSV file: {e}")
        raw_df = load_default_data()
else:
    raw_df = load_default_data()
    st.sidebar.info("Using Sample Student Marks Dataset")

# Download sample template button
sample_df = load_default_data()
st.sidebar.download_button(
    label="📥 Download Sample CSV Template",
    data=sample_df.to_csv(index=False).encode('utf-8'),
    file_name="sample_student_marks_template.csv",
    mime="text/csv",
    help="Download this sample CSV to test uploading your own format."
)

st.sidebar.markdown("---")

# Process dataframe
df, subject_cols = process_dataframe(raw_df)

# Dynamic Filters in Sidebar
st.sidebar.subheader("🔍 Data Filters")

# Filter by Class
all_classes = ["All"] + sorted(df["Class"].astype(str).unique().tolist()) if "Class" in df.columns else ["All"]
selected_class = st.sidebar.selectbox("Select Class/Grade", all_classes)

# Filter by Semester
all_semesters = ["All"] + sorted(df["Semester"].astype(str).unique().tolist()) if "Semester" in df.columns else ["All"]
selected_semester = st.sidebar.selectbox("Select Semester", all_semesters)

# Filter by Search Name
search_query = st.sidebar.text_input("Search Student Name or ID", "")

# Apply Filters
filtered_df = df.copy()

if selected_class != "All" and "Class" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Class"].astype(str) == selected_class]

if selected_semester != "All" and "Semester" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Semester"].astype(str) == selected_semester]

if search_query.strip():
    name_match = filtered_df["Name"].astype(str).str.contains(search_query, case=False, na=False) if "Name" in filtered_df.columns else False
    id_match = filtered_df["Student_ID"].astype(str).str.contains(search_query, case=False, na=False) if "Student_ID" in filtered_df.columns else False
    filtered_df = filtered_df[name_match | id_match]


# ==========================================
# MAIN DASHBOARD CONTENT
# ==========================================
st.markdown('<div class="main-header">🎓 Student Marks Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive analytics, academic performance metrics, and subject trend visualizations</div>', unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No student records match the selected filter criteria. Please adjust sidebar filters.")
    st.stop()

# ------------------------------------------
# SECTION 1: KEY PERFORMANCE METRICS
# ------------------------------------------
col1, col2, col3, col4 = st.columns(4)

total_students = filtered_df["Student_ID"].nunique() if "Student_ID" in filtered_df.columns else len(filtered_df)
avg_percentage = filtered_df["Percentage"].mean() if not filtered_df.empty else 0
pass_rate = (filtered_df[filtered_df["Status"] == "Pass"].shape[0] / len(filtered_df) * 100) if not filtered_df.empty else 0

top_student_row = filtered_df.loc[filtered_df["Percentage"].idxmax()] if not filtered_df.empty else None
top_scorer = top_student_row["Name"] if top_student_row is not None and "Name" in top_student_row else "N/A"
top_score = top_student_row["Percentage"] if top_student_row is not None else 0

col1.metric("Total Students", f"{total_students}", help="Unique students in current filter view")
col2.metric("Overall Class Avg", f"{avg_percentage:.2f}%", delta=f"{avg_percentage - 75.0:.1f}% vs Target (75%)")
col3.metric("Pass Rate", f"{pass_rate:.1f}%", delta=f"{pass_rate - 90.0:.1f}% vs Goal (90%)")
col4.metric("Top Performer", f"{top_scorer}", f"{top_score:.1f}%")

st.markdown("---")

# ------------------------------------------
# SECTION 2: INTERACTIVE DATA TABLE (st.dataframe)
# ------------------------------------------
st.subheader("📋 Student Marks Data Table")
st.caption("Interactive data table supported by Streamlit `st.dataframe()`. Sort, search, or view detailed marks.")

# Display option toggle
table_view_col, export_col = st.columns([3, 1])
with table_view_col:
    show_subjects_only = st.checkbox("Hide metadata columns (show only Subject Marks & Totals)", value=False)

if show_subjects_only:
    display_cols = [c for c in ["Name"] + subject_cols + ["Total_Marks", "Percentage", "Grade"] if c in filtered_df.columns]
    data_to_show = filtered_df[display_cols]
else:
    data_to_show = filtered_df

# Feature 2: st.dataframe()
st.dataframe(
    data_to_show,
    use_container_width=True,
    column_config={
        "Percentage": st.column_config.ProgressColumn(
            "Overall %",
            help="Student total percentage score",
            format="%.2f%%",
            min_value=0,
            max_value=100,
        ),
        "Total_Marks": st.column_config.NumberColumn("Total Marks", format="%d"),
        "Grade": st.column_config.TextColumn("Grade Badge"),
        "Status": st.column_config.TextColumn("Pass Status")
    },
    hide_index=True,
    height=320
)

# Download processed CSV button
with export_col:
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Processed Data CSV",
        data=csv_bytes,
        file_name="processed_student_marks_report.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")

# ------------------------------------------
# SECTION 3: PERFORMANCE TREND LINE CHARTS (st.line_chart)
# ------------------------------------------
st.subheader("📈 Subject Performance & Mark Trends")
st.caption("Visualizing performance trends using Streamlit `st.line_chart()`.")

chart_tab1, chart_tab2, chart_tab3 = st.tabs([
    "📊 Subject Average Trends", 
    "👨‍🎓 Student Marks Comparison", 
    "📅 Semester Progress Trend"
])

# Feature 3: st.line_chart() - Tab 1: Subject Averages
with chart_tab1:
    st.write("##### Subject-wise Mean Score Across Students")
    if subject_cols:
        subject_means = filtered_df[subject_cols].mean().to_frame(name="Average Score")
        
        # Display st.line_chart for subject averages
        st.line_chart(
            subject_means,
            use_container_width=True,
            color="#2563EB"
        )
        
        # Summary description
        highest_sub = subject_means["Average Score"].idxmax()
        lowest_sub = subject_means["Average Score"].idxmin()
        st.info(f"💡 **Insight**: Students performed highest in **{highest_sub}** ({subject_means.loc[highest_sub, 'Average Score']:.1f} avg) and need support in **{lowest_sub}** ({subject_means.loc[lowest_sub, 'Average Score']:.1f} avg).")
    else:
        st.warning("No subject columns detected for line chart visualization.")

# Feature 3: st.line_chart() - Tab 2: Individual Student Marks Comparison
with chart_tab2:
    st.write("##### Compare Subject Marks for Selected Students")
    if "Name" in filtered_df.columns:
        available_students = filtered_df["Name"].unique().tolist()
        default_selected = available_students[:5] if len(available_students) >= 5 else available_students
        
        selected_students = st.multiselect(
            "Select Students to Compare:",
            options=available_students,
            default=default_selected
        )
        
        if selected_students:
            student_df = filtered_df[filtered_df["Name"].isin(selected_students)]
            # Pivot data so Subjects are index and Students are columns for line_chart
            pivot_df = student_df.melt(
                id_vars=["Name"], 
                value_vars=subject_cols, 
                var_name="Subject", 
                value_name="Marks"
            )
            pivot_chart_data = pivot_df.pivot_table(index="Subject", columns="Name", values="Marks", aggfunc='mean')
            
            # Display st.line_chart for multi-student comparison
            st.line_chart(
                pivot_chart_data,
                use_container_width=True
            )
        else:
            st.warning("Please select at least one student from the dropdown above to display the line chart.")

# Feature 3: st.line_chart() - Tab 3: Semester Progress Trend
with chart_tab3:
    st.write("##### Semester-over-Semester Academic Progression")
    if "Semester" in df.columns and "Name" in df.columns:
        sem_student = st.selectbox(
            "Select Student for Progression Line Chart:",
            options=df["Name"].unique().tolist()
        )
        
        sem_df = df[df["Name"] == sem_student].sort_values("Semester")
        
        if not sem_df.empty:
            sem_chart_data = sem_df.set_index("Semester")[subject_cols]
            
            # Display st.line_chart for student semester trend
            st.line_chart(
                sem_chart_data,
                use_container_width=True
            )
        else:
            st.info("No semester progression data available for selected student.")
    else:
        st.info("Semester or Student Name columns not present in dataset.")

st.markdown("---")

# ------------------------------------------
# SECTION 4: STATISTICAL SUMMARY & GRADE DISTRIBUTION
# ------------------------------------------
col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.subheader("📊 Subject Descriptive Statistics")
    if subject_cols:
        stats_df = filtered_df[subject_cols].describe().T[["mean", "std", "min", "max"]]
        stats_df.columns = ["Average", "Std Dev", "Min Mark", "Max Mark"]
        st.dataframe(stats_df.round(2), use_container_width=True)

with col_stat2:
    st.subheader("🏆 Grade Distribution Summary")
    grade_counts = filtered_df["Grade"].value_counts().reset_index()
    grade_counts.columns = ["Grade", "Student Count"]
    
    # Display grade distribution
    st.dataframe(grade_counts, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94A3B8; font-size: 0.85rem;">
        Student Marks Analysis Dashboard • Built with Streamlit, Pandas & Python • Hosted on GitHub
    </div>
    """,
    unsafe_allow_html=True
)
