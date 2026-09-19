import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Performance AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load("student_score_model.pkl")


model = load_model()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #777;
    margin-bottom: 25px;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    text-align: center;
    margin-bottom: 10px;
}

.insight-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎓 Student Performance AI")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "📝 Student Assessment",
        "🔮 What-If Simulator",
        "📊 Performance Analytics",
        "📋 Student Report",
        "ℹ️ About Model"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "This application uses Machine Learning "
    "to estimate a student's final score."
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_performance_category(score):

    if score >= 90:
        return "🌟 Excellent"
    elif score >= 75:
        return "🟢 Good"
    elif score >= 60:
        return "🟡 Average"
    else:
        return "🔴 Needs Improvement"


def get_recommendations(
    study_hours,
    attendance,
    previous_score,
    assignment_score
):

    recommendations = []

    if study_hours < 5:
        recommendations.append(
            "📚 Try increasing your study time gradually and maintain consistency."
        )

    if attendance < 75:
        recommendations.append(
            "📅 Improve attendance because consistent class participation can support learning."
        )

    if previous_score < 70:
        recommendations.append(
            "📊 Review concepts from previous assessments and identify weak topics."
        )

    if assignment_score < 70:
        recommendations.append(
            "📝 Focus on completing assignments carefully and improving assignment quality."
        )

    if not recommendations:
        recommendations.append(
            "🎉 Your current academic indicators look strong. Focus on consistency."
        )

    return recommendations


def generate_insight(
    predicted_score,
    study_hours,
    attendance,
    previous_score,
    assignment_score
):

    strengths = []
    improvements = []

    if attendance >= 85:
        strengths.append("strong attendance")
    elif attendance < 75:
        improvements.append("attendance")

    if previous_score >= 80:
        strengths.append("strong previous academic performance")
    elif previous_score < 70:
        improvements.append("previous academic performance")

    if assignment_score >= 80:
        strengths.append("good assignment performance")
    elif assignment_score < 70:
        improvements.append("assignment performance")

    if study_hours >= 6:
        strengths.append("consistent study time")
    elif study_hours < 4:
        improvements.append("study consistency")

    if predicted_score >= 90:

        message = (
            "Your predicted performance is excellent. "
            "Continue maintaining your current academic habits."
        )

    elif predicted_score >= 75:

        message = (
            "Your predicted performance is good. "
            "With consistent effort, there is room to move toward an excellent score."
        )

    elif predicted_score >= 60:

        message = (
            "Your predicted performance is in the average range. "
            "Improving your weaker academic indicators could help increase your score."
        )

    else:

        message = (
            "Your predicted performance indicates that additional academic support "
            "and consistent study habits may be beneficial."
        )

    return message, strengths, improvements


def make_prediction(
    study_hours,
    attendance,
    previous_score,
    assignment_score
):

    input_data = pd.DataFrame([{
        "study_hours": study_hours,
        "attendance": attendance,
        "previous_score": previous_score,
        "assignment_score": assignment_score
    }])

    prediction = model.predict(input_data)[0]

    # Keep score between 0 and 100 for presentation.
    prediction = max(0, min(100, prediction))

    return prediction


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🎓 Student Performance AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Predict • Analyze • Improve your academic performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("🚀 Welcome")

    st.write(
        """
        This application uses a Machine Learning model to predict a student's
        final score using academic performance indicators.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🤖 ML Model", "Linear Regression")

    with col2:
        st.metric("📊 Features", "4")

    with col3:
        st.metric("🎯 Target", "Final Score")

    with col4:
        st.metric("📚 Application", "Academic Analysis")

    st.markdown("---")

    st.subheader("✨ What can you do?")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            📝 **Student Assessment**

            Enter your study hours, attendance,
            previous score and assignment score
            to generate a prediction.
            """
        )

        st.info(
            """
            🔮 **What-If Simulator**

            Experiment with different academic
            habits and see how the predicted score changes.
            """
        )

    with col2:

        st.info(
            """
            📊 **Performance Analytics**

            Explore your academic indicators
            and understand your performance profile.
            """
        )

        st.info(
            """
            🎯 **Improvement Plan**

            Get personalized suggestions based
            on your current academic indicators.
            """
        )

    st.markdown("---")

    st.success(
        "👉 Go to **Student Assessment** from the sidebar to make your first prediction."
    )


# ============================================================
# STUDENT ASSESSMENT
# ============================================================

elif page == "📝 Student Assessment":

    st.title("📝 Student Assessment")

    st.write(
        "Enter the student's academic information below."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        study_hours = st.number_input(
            "📚 Study Hours per Day",
            min_value=0.0,
            max_value=24.0,
            value=6.0,
            step=0.5
        )

        attendance = st.number_input(
            "📅 Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=1.0
        )

    with col2:

        previous_score = st.number_input(
            "📊 Previous Score",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=1.0
        )

        assignment_score = st.number_input(
            "📝 Assignment Score",
            min_value=0.0,
            max_value=100.0,
            value=80.0,
            step=1.0
        )

    st.markdown("---")

    if st.button(
        "🔮 Predict My Score",
        type="primary",
        use_container_width=True
    ):

        predicted_score = make_prediction(
            study_hours,
            attendance,
            previous_score,
            assignment_score
        )

        category = get_performance_category(predicted_score)

        st.session_state["predicted_score"] = predicted_score
        st.session_state["study_hours"] = study_hours
        st.session_state["attendance"] = attendance
        st.session_state["previous_score"] = previous_score
        st.session_state["assignment_score"] = assignment_score

        st.markdown("---")

        st.subheader("🎯 Your Prediction")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Predicted Final Score",
                f"{predicted_score:.2f}/100"
            )

        with col2:
            st.metric(
                "Performance",
                category
            )

        with col3:
            target = 85
            gap = max(0, target - predicted_score)

            st.metric(
                "Gap to 85",
                f"{gap:.2f}"
            )

        st.progress(predicted_score / 100)

        if predicted_score >= 90:
            st.success(
                "🌟 Excellent! Keep maintaining your current performance."
            )

        elif predicted_score >= 75:
            st.success(
                "🟢 Good performance! A little improvement could push you higher."
            )

        elif predicted_score >= 60:
            st.warning(
                "🟡 Average performance. Focus on your weaker areas."
            )

        else:
            st.error(
                "🔴 Needs Improvement. Consider creating a consistent study plan."
            )

        st.markdown("---")

        st.subheader("💡 Personalized Recommendations")

        recommendations = get_recommendations(
            study_hours,
            attendance,
            previous_score,
            assignment_score
        )

        for recommendation in recommendations:
            st.write(recommendation)


# ============================================================
# WHAT-IF SIMULATOR
# ============================================================

elif page == "🔮 What-If Simulator":

    st.title("🔮 What-If Simulator")

    st.write(
        """
        Experiment with different academic habits and see
        how your predicted score changes.
        """
    )

    if "predicted_score" in st.session_state:

        current_score = st.session_state["predicted_score"]

        default_study = st.session_state["study_hours"]
        default_attendance = st.session_state["attendance"]
        default_previous = st.session_state["previous_score"]
        default_assignment = st.session_state["assignment_score"]

    else:

        current_score = make_prediction(6, 85, 75, 80)

        default_study = 6.0
        default_attendance = 85.0
        default_previous = 75.0
        default_assignment = 80.0

    st.markdown("---")

    st.subheader("🎛️ Change Your Academic Habits")

    col1, col2 = st.columns(2)

    with col1:

        whatif_study = st.slider(
            "📚 Study Hours",
            min_value=0.0,
            max_value=12.0,
            value=float(default_study),
            step=0.5
        )

        whatif_attendance = st.slider(
            "📅 Attendance (%)",
            min_value=0,
            max_value=100,
            value=int(default_attendance)
        )

    with col2:

        whatif_previous = st.slider(
            "📊 Previous Score",
            min_value=0,
            max_value=100,
            value=int(default_previous)
        )

        whatif_assignment = st.slider(
            "📝 Assignment Score",
            min_value=0,
            max_value=100,
            value=int(default_assignment)
        )

    whatif_prediction = make_prediction(
        whatif_study,
        whatif_attendance,
        whatif_previous,
        whatif_assignment
    )

    difference = whatif_prediction - current_score

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Prediction",
            f"{current_score:.2f}"
        )

    with col2:
        st.metric(
            "New Prediction",
            f"{whatif_prediction:.2f}"
        )

    with col3:

        st.metric(
            "Change",
            f"{difference:+.2f}"
        )

    st.progress(whatif_prediction / 100)

    if difference > 0:
        st.success(
            f"🎉 Your simulated changes increased the prediction by "
            f"{difference:.2f} points."
        )

    elif difference < 0:
        st.warning(
            f"Your simulated changes decreased the prediction by "
            f"{abs(difference):.2f} points."
        )

    else:
        st.info("The prediction did not change.")


# ============================================================
# PERFORMANCE ANALYTICS
# ============================================================

elif page == "📊 Performance Analytics":

    st.title("📊 Performance Analytics")

    if "predicted_score" not in st.session_state:

        st.info(
            "First make a prediction from the Student Assessment page."
        )

    else:

        predicted_score = st.session_state["predicted_score"]
        study_hours = st.session_state["study_hours"]
        attendance = st.session_state["attendance"]
        previous_score = st.session_state["previous_score"]
        assignment_score = st.session_state["assignment_score"]

        st.subheader("📈 Academic Profile")

        data = pd.DataFrame({
            "Indicator": [
                "Study Hours",
                "Attendance",
                "Previous Score",
                "Assignment Score"
            ],
            "Value": [
                study_hours,
                attendance,
                previous_score,
                assignment_score
            ]
        })

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader("📊 Performance Visualization")

        chart_data = pd.DataFrame({
            "Feature": [
                "Attendance",
                "Previous Score",
                "Assignment Score"
            ],
            "Score": [
                attendance,
                previous_score,
                assignment_score
            ]
        })

        st.bar_chart(
            chart_data.set_index("Feature")
        )

        st.markdown("---")

        st.subheader("🤖 Model Coefficients")

        try:

            coefficients = pd.DataFrame({
                "Feature": [
                    "Study Hours",
                    "Attendance",
                    "Previous Score",
                    "Assignment Score"
                ],
                "Coefficient": model.coef_
            })

            st.dataframe(
                coefficients,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Coefficients represent how the trained Linear Regression "
                "model weights each input feature. They should be interpreted "
                "carefully because this project uses a very small demonstration dataset."
            )

        except Exception:

            st.info(
                "Model coefficient information is not available."
            )

        st.markdown("---")

        st.subheader("🎯 Your Result")

        st.metric(
            "Predicted Final Score",
            f"{predicted_score:.2f}/100"
        )

        st.write(
            get_performance_category(predicted_score)
        )


# ============================================================
# STUDENT REPORT
# ============================================================

elif page == "📋 Student Report":

    st.title("📋 Student Performance Report")

    if "predicted_score" not in st.session_state:

        st.info(
            "Make a prediction first to generate your student report."
        )

    else:

        predicted_score = st.session_state["predicted_score"]
        study_hours = st.session_state["study_hours"]
        attendance = st.session_state["attendance"]
        previous_score = st.session_state["previous_score"]
        assignment_score = st.session_state["assignment_score"]

        category = get_performance_category(predicted_score)

        st.markdown("---")

        st.subheader("🎯 Prediction Summary")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Predicted Final Score",
                f"{predicted_score:.2f}/100"
            )

        with col2:

            st.metric(
                "Performance Level",
                category
            )

        st.markdown("---")

        st.subheader("📚 Academic Indicators")

        report_data = pd.DataFrame({
            "Indicator": [
                "Study Hours per Day",
                "Attendance",
                "Previous Score",
                "Assignment Score",
                "Predicted Final Score"
            ],
            "Value": [
                f"{study_hours:.1f}",
                f"{attendance:.0f}%",
                f"{previous_score:.0f}",
                f"{assignment_score:.0f}",
                f"{predicted_score:.2f}"
            ]
        })

        st.table(report_data)

        st.markdown("---")

        st.subheader("💡 Key Insights")

        insight, strengths, improvements = generate_insight(
            predicted_score,
            study_hours,
            attendance,
            previous_score,
            assignment_score
        )

        st.info(insight)

        if strengths:

            st.write("### 💪 Strengths")

            for strength in strengths:
                st.write(f"✅ {strength}")

        if improvements:

            st.write("### 🎯 Areas to Improve")

            for improvement in improvements:
                st.write(f"⚠️ {improvement}")

        st.markdown("---")

        st.subheader("🚀 Recommended Actions")

        recommendations = get_recommendations(
            study_hours,
            attendance,
            previous_score,
            assignment_score
        )

        for recommendation in recommendations:
            st.write(recommendation)

        st.markdown("---")

        # Create downloadable text report

        report_text = f"""
STUDENT PERFORMANCE REPORT
==========================

Predicted Final Score: {predicted_score:.2f}/100
Performance Level: {category}

ACADEMIC INDICATORS
-------------------

Study Hours per Day: {study_hours:.1f}
Attendance: {attendance:.0f}%
Previous Score: {previous_score:.0f}
Assignment Score: {assignment_score:.0f}

AI-STYLE INSIGHT
----------------

{insight}

RECOMMENDATIONS
---------------

"""

        for recommendation in recommendations:
            report_text += f"- {recommendation}\n"

        st.download_button(
            label="⬇️ Download Student Report",
            data=report_text,
            file_name="student_performance_report.txt",
            mime="text/plain",
            use_container_width=True
        )


# ============================================================
# ABOUT MODEL
# ============================================================

elif page == "ℹ️ About Model":

    st.title("🧠 About Student Performance AI")

    st.markdown(
        """
        <div style="
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #444;
            margin-bottom: 25px;
        ">
            <h2>🎓 Machine Learning Based Student Analysis</h2>
            <p>
                This application uses Machine Learning to estimate a student's
                final score from four academic performance indicators.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MODEL OVERVIEW
    # ========================================================

    st.subheader("🤖 Model Overview")

    st.markdown(
        """
        <div style="
            display:grid;
            grid-template-columns:repeat(4, 1fr);
            gap:18px;
            margin-top:20px;
            margin-bottom:25px;
        ">

            <!-- Algorithm -->
            <div style="
                padding:24px;
                border-radius:18px;
                border:1px solid rgba(128,128,128,0.35);
                background:rgba(128,128,128,0.08);
                min-height:180px;
            ">

                <div style="font-size:38px;">
                    🤖
                </div>

                <div style="
                    font-size:14px;
                    margin-top:12px;
                    opacity:0.7;
                ">
                    MACHINE LEARNING
                </div>

                <div style="
                    font-size:22px;
                    font-weight:700;
                    margin-top:5px;
                ">
                    Linear Regression
                </div>

                <div style="
                    font-size:14px;
                    margin-top:10px;
                    opacity:0.75;
                ">
                    Predicts a continuous final score
                    from academic performance features.
                </div>

            </div>


            <!-- Features -->
            <div style="
                padding:24px;
                border-radius:18px;
                border:1px solid rgba(128,128,128,0.35);
                background:rgba(128,128,128,0.08);
                min-height:180px;
            ">

                <div style="font-size:38px;">
                    📥
                </div>

                <div style="
                    font-size:14px;
                    margin-top:12px;
                    opacity:0.7;
                ">
                    INPUT FEATURES
                </div>

                <div style="
                    font-size:32px;
                    font-weight:700;
                    margin-top:5px;
                ">
                    4
                </div>

                <div style="
                    font-size:14px;
                    margin-top:5px;
                    opacity:0.75;
                ">
                    Study hours · Attendance
                    · Previous score · Assignment score
                </div>

            </div>


            <!-- Target -->
            <div style="
                padding:24px;
                border-radius:18px;
                border:1px solid rgba(128,128,128,0.35);
                background:rgba(128,128,128,0.08);
                min-height:180px;
            ">

                <div style="font-size:38px;">
                    🎯
                </div>

                <div style="
                    font-size:14px;
                    margin-top:12px;
                    opacity:0.7;
                ">
                    PREDICTION TARGET
                </div>

                <div style="
                    font-size:22px;
                    font-weight:700;
                    margin-top:5px;
                ">
                    Final Score
                </div>

                <div style="
                    font-size:14px;
                    margin-top:10px;
                    opacity:0.75;
                ">
                    The model estimates the student's
                    expected final academic score.
                </div>

            </div>


            <!-- Technology -->
            <div style="
                padding:24px;
                border-radius:18px;
                border:1px solid rgba(128,128,128,0.35);
                background:rgba(128,128,128,0.08);
                min-height:180px;
            ">

                <div style="font-size:38px;">
                    🐍
                </div>

                <div style="
                    font-size:14px;
                    margin-top:12px;
                    opacity:0.7;
                ">
                    DEVELOPMENT
                </div>

                <div style="
                    font-size:22px;
                    font-weight:700;
                    margin-top:5px;
                ">
                    Python
                </div>

                <div style="
                    font-size:14px;
                    margin-top:10px;
                    opacity:0.75;
                ">
                    The core programming language
                    powering the ML pipeline.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # TECHNOLOGIES
    # ========================================================

    st.subheader("🛠️ Technologies Used")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            ### 🐍 Python

            Used as the primary programming language
            for data processing and Machine Learning.
            """
        )

        st.markdown(
            """
            ### 🐼 Pandas

            Used for loading, cleaning and analyzing
            the student dataset.
            """
        )

        st.markdown(
            """
            ### 🔢 NumPy

            Used for numerical operations and
            mathematical computations.
            """
        )

    with col2:

        st.markdown(
            """
            ### 🤖 Scikit-learn

            Used to build, train and evaluate
            the Linear Regression model.
            """
        )

        st.markdown(
            """
            ### 💾 Joblib

            Used to save and load the trained
            Machine Learning model.
            """
        )

        st.markdown(
            """
            ### 📓 Jupyter Notebook

            Used during experimentation,
            EDA and model development.
            """
        )

    with col3:

        st.markdown(
            """
            ### 📊 Matplotlib

            Used for exploratory data visualization
            and model analysis.
            """
        )

        st.markdown(
            """
            ### 🎨 Streamlit

            Used to build the interactive web
            application.
            """
        )

        st.markdown(
            """
            ### 📂 CSV Dataset

            Contains the academic information
            used by the Machine Learning model.
            """
        )

    st.markdown("---")


    # ========================================================
    # MACHINE LEARNING WORKFLOW
    # ========================================================

    st.subheader("🔄 Machine Learning Workflow")

    st.write(
        "Follow the complete journey from raw student data to prediction."
    )

    workflow = [
        ("📂", "Dataset", "Student academic data"),
        ("🔍", "EDA", "Explore & understand data"),
        ("🎯", "Features", "Select input variables"),
        ("✂️", "Train/Test", "Split the dataset"),
        ("🤖", "Training", "Train Linear Regression"),
        ("📊", "Evaluation", "Measure performance"),
        ("💾", "Save Model", "Store trained model"),
        ("🌐", "Streamlit", "Build web application"),
        ("🎯", "Prediction", "Predict final score")
    ]

    for i in range(0, len(workflow), 3):

        cols = st.columns(3)

        for j, col in enumerate(cols):

            if i + j < len(workflow):

                icon, title, description = workflow[i + j]

                with col:

                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #555;
                            border-radius: 15px;
                            padding: 18px;
                            text-align: center;
                            margin-bottom: 10px;
                        ">

                        <div style="font-size: 35px;">
                            {icon}
                        </div>

                        <h4>{title}</h4>

                        <p style="font-size: 14px;">
                            {description}
                        </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        if i + 3 < len(workflow):

            st.markdown(
                "<div style='text-align:center; font-size:25px;'>⬇️</div>",
                unsafe_allow_html=True
            )


    st.markdown("---")


    # ========================================================
    # PREDICTION PIPELINE
    # ========================================================

    st.subheader("🔮 Prediction Pipeline")

    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            gap:15px;
            flex-wrap:wrap;
            margin:25px 0;
        ">

            <div style="
                padding:20px;
                border:1px solid #555;
                border-radius:15px;
                text-align:center;
            ">
                <div style="font-size:35px;">📚</div>
                <b>Student Inputs</b>
                <br>
                <small>4 Features</small>
            </div>

            <div style="font-size:30px;">
                ➡️
            </div>

            <div style="
                padding:20px;
                border:1px solid #555;
                border-radius:15px;
                text-align:center;
            ">
                <div style="font-size:35px;">🤖</div>
                <b>ML Model</b>
                <br>
                <small>Linear Regression</small>
            </div>

            <div style="font-size:30px;">
                ➡️
            </div>

            <div style="
                padding:20px;
                border:1px solid #555;
                border-radius:15px;
                text-align:center;
            ">
                <div style="font-size:35px;">🎯</div>
                <b>Prediction</b>
                <br>
                <small>Final Score</small>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # INPUT FEATURES
    # ========================================================

    st.subheader("📥 Model Input Features")

    feature_info = {
        "📚 Study Hours": "Number of hours the student studies.",
        "📅 Attendance": "Student attendance percentage.",
        "📊 Previous Score": "Score obtained in previous assessment.",
        "📝 Assignment Score": "Score obtained in assignments."
    }

    for feature, description in feature_info.items():

        with st.expander(feature):

            st.write(description)

    st.markdown("---")


    # ========================================================
    # MODEL COEFFICIENTS
    # ========================================================

    st.subheader("📊 Model Feature Influence")

    st.write(
        """
        Linear Regression assigns a coefficient to each feature.
        These coefficients represent how the trained model weights
        the features when making predictions.
        """
    )

    try:

        coefficients = pd.DataFrame({
            "Feature": [
                "Study Hours",
                "Attendance",
                "Previous Score",
                "Assignment Score"
            ],
            "Coefficient": model.coef_
        })

        st.bar_chart(
            coefficients.set_index("Feature")
        )

        with st.expander("🔍 Understand these coefficients"):

            st.write(
                """
                A positive coefficient means that, within this trained
                model, increasing that feature is associated with an
                increase in the predicted final score, while a negative
                coefficient indicates the opposite relationship.

                However, coefficients should not be interpreted as proof
                of causation. This project uses a very small demonstration
                dataset.
                """
            )

        st.dataframe(
            coefficients,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.warning(
            "Model coefficient visualization is currently unavailable."
        )

    st.markdown("---")


    # ========================================================
    # MODEL FORMULA
    # ========================================================

    st.subheader("🧮 How Linear Regression Works")

    with st.expander("📖 Show the mathematical idea"):

        st.latex(
            r"""
            \hat{y} =
            b_0 +
            b_1x_1 +
            b_2x_2 +
            b_3x_3 +
            b_4x_4
            """
        )

        st.write(
            """
            The model combines the four input features using learned
            coefficients and an intercept to calculate the predicted score.
            """
        )


    # ========================================================
    # MODEL FILE
    # ========================================================

    st.subheader("💾 Trained Model")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            **Model file**

            `student_score_model.pkl`

            The trained model is stored using Joblib.
            """
        )

    with col2:

        st.info(
            """
            **Model type**

            Linear Regression

            The saved model is loaded when the Streamlit
            application starts.
            """
        )

    st.markdown("---")


    # ========================================================
    # PROJECT LIMITATION
    # ========================================================

    st.subheader("⚠️ Important Project Limitation")

    st.warning(
        """
        This project currently uses a very small demonstration dataset.
        Therefore, the predictions are intended for demonstrating the
        Machine Learning workflow and application, not for making reliable
        real-world academic decisions.

        A production version should use a much larger and representative
        dataset and undergo proper validation.
        """
    )

    st.markdown("---")


    # ========================================================
    # TECHNOLOGY STACK SUMMARY
    # ========================================================

    st.subheader("🚀 Complete Technology Stack")

    st.code(
        """
Python
│
├── Pandas
├── NumPy
├── Matplotlib
│
├── Scikit-learn
│   └── Linear Regression
│
├── Joblib
│   └── Model Persistence
│
├── Jupyter Notebook
│   └── Model Development
│
└── Streamlit
    └── Interactive Web Application
        """,
        language="text"
    )

    st.success(
        "🎓 Student Performance AI — From Data → Machine Learning → Prediction → Insights"
    )