# 🎓 Student Marks Analysis Dashboard

A feature-rich, interactive **Student Marks Analysis Dashboard** built using **Python** and **Streamlit**. 

This application provides real-time academic performance insights, KPI metrics, subject trend visualizations, and individual student progress tracking.

---

## 🚀 Key Features & Streamlit Functions Used

This project specifically demonstrates key Streamlit UI components:

1. **`st.file_uploader()`**:
   - Allows users to upload custom CSV files containing student marksheets.
   - Provides instant validation and fallback to built-in sample data.
   - Features a downloadable sample CSV template for quick testing.

2. **`st.dataframe()`**:
   - Displays student records in an interactive, searchable, and sortable data table.
   - Column formatting with visual progress bars for percentage scores and status badges.
   - One-click export button (`st.download_button()`) to download processed reports.

3. **`st.line_chart()`**:
   - Interactive line charts visualizing:
     - **Subject Average Trends**: Overall mean scores across subjects.
     - **Multi-Student Comparison**: Side-by-side performance lines for selected students.
     - **Semester Progress**: Academic trajectory across multiple exam terms.

4. **Interactive Filters & Metrics**:
   - KPI metric scorecards (`st.metric()`) for Total Students, Class Average, Pass Rate, and Top Scorer.
   - Sidebar filters by Class, Semester, and Student Name/ID.
   - Grade Distribution breakdown (A+, A, B, C, D, F).

---

## 🛠️ Local Installation & Running Guide

### Prerequisites
- Python 3.9+ installed

### Step 1: Install Required Packages
Open your terminal in the `Presentation` folder and run:
```bash
pip install -r requirements.txt
```
*(Or install manually: `pip install streamlit pandas numpy`)*

### Step 2: Run the Streamlit Application
Launch the app with:
```bash
streamlit run app.py
```
The application will automatically open in your web browser at `http://localhost:8501`.

---

## 🐙 How to Host & Publish on GitHub

Follow these steps to host your project on GitHub and optionally deploy it live for free on Streamlit Cloud:

### Step 1: Initialize Git Repository
Open PowerShell or Command Prompt inside the `Presentation` folder (`c:\Users\letss\OneDrive\Desktop\Advanced Python\Presentation`):

```bash
# Initialize git in the Presentation folder
git init

# Stage all project files
git add .

# Create initial commit
git commit -m "Initial commit: Student Marks Analysis Dashboard Streamlit App"
```

### Step 2: Create Repository on GitHub
1. Go to [GitHub](https://github.com/) and sign in.
2. Click the **`+`** icon in the top right corner and select **"New repository"**.
3. Name your repository (e.g., `student-marks-analysis-dashboard`).
4. Keep it **Public** (required for free Streamlit Cloud hosting).
5. Do **NOT** initialize with a README, .gitignore, or license (since we already created them).
6. Click **"Create repository"**.

### Step 3: Link Remote & Push Code
Copy the commands shown on GitHub after repo creation and execute them in your terminal:

```bash
# Rename branch to main
git branch -M main

# Link to your remote GitHub repository (replace with your URL)
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/student-marks-analysis-dashboard.git

# Push code to GitHub
git push -u origin main
```

---

## 🌐 Bonus: Deploy Live on Streamlit Cloud (Free)

1. Visit [Streamlit Community Cloud](https://streamlit.io/cloud) and click **Sign Up / Log In** using your GitHub account.
2. Click **"New App"**.
3. Select your GitHub repository (`student-marks-analysis-dashboard`), set Main file path to `app.py`.
4. Click **"Deploy!"**
5. Your dashboard will be live on the web with a public URL! 🎉

---

## 📁 Project Structure

```
Presentation/
├── app.py                     # Main Streamlit dashboard script
├── sample_student_marks.csv   # Pre-loaded sample dataset
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation & GitHub guide
└── .gitignore                 # Git ignore configuration
```
