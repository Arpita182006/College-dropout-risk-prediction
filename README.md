# College-dropout-risk-prediction
A machine learning project to predict the risk of college student dropout using regression models and a Streamlit web app for real-time risk scoring.

🎓 College Dropout Risk Prediction
Predicting which students are at risk of dropping out using machine learning models like Multiple Linear Regression, Decision Tree, and Random Forest. This project helps educational institutions take proactive steps to support students.

🧠 Objective
Build a predictive model to estimate dropout risk based on student data including academics, attendance, financial background, and psychological stress.

📁 Dataset
🔢 Rows: ~500+ student records

📌 Format: .csv (custom/synthetic)

🎯 Target Variable: dropout_risk_score (continuous value or probability)

Example Features:
attendance rate
current GPA
study hours per week
mental health score(scale 1-10)
stress level (scale 1–10)
parental support(yes/no)
part time job

| Model                      | Type       | Purpose                        |
| -------------------------- | ---------- | ------------------------------ |
| Multiple Linear Regression | Regression | Baseline model                 |
| Decision Tree Regressor    | Regression | Non-linear modeling            |
| Random Forest Regressor    | Regression | Best-performing ensemble model |


🔍 Tools & Libraries
Python
Pandas, NumPy
scikit-learn
Matplotlib / Seaborn
Streamlit (optional frontend)

