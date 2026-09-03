import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.predictor import predict_network_data


st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)
# Sidebar
with st.sidebar:
    st.header("🛡️ SentinelAI")

    st.markdown(
        """
        ### AI Network Security

        SentinelAI analyzes network traffic
        using a Random Forest machine-learning model.

        **Detection**
        - 🚨 ATTACK
        - ✅ BENIGN

        **Risk Levels**
        - 🟢 LOW
        - 🟡 MEDIUM
        - 🟠 HIGH
        - 🔴 CRITICAL
        """
    )

    st.divider()

    st.caption("SentinelAI v1.0")
    st.caption("AI-Powered Network Intrusion Detection System")


# Scan history
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []


st.title("🛡️ SentinelAI")
st.subheader("AI-Powered Network Intrusion Detection System")

st.divider()


uploaded_file = st.file_uploader(
    "Upload Network Traffic CSV",
    type=["csv"]
)


if uploaded_file is not None:

    try:

        data = pd.read_csv(uploaded_file)

        st.success("Dataset loaded successfully!")

        # Basic dataset information
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Records",
                f"{len(data):,}"
            )

        with col2:
            st.metric(
                "Features",
                len(data.columns)
            )

        with col3:
            st.metric(
                "Status",
                "Analyzing"
            )

        st.divider()


        # AI prediction
        with st.spinner(
            "SentinelAI is analyzing network traffic..."
        ):

            result = predict_network_data(data)


        attack_count = int(
            (result["Prediction"] == "ATTACK").sum()
        )

        benign_count = int(
            (result["Prediction"] == "BENIGN").sum()
        )

        total = len(result)


        attack_percentage = (
            attack_count / total * 100
            if total > 0 else 0
        )

        benign_percentage = (
            benign_count / total * 100
            if total > 0 else 0
        )


        # Threat Detection Results
        st.subheader("🛡️ Threat Detection Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🚨 Attacks Detected",
                f"{attack_count:,}"
            )

        with col2:
            st.metric(
                "✅ Benign Traffic",
                f"{benign_count:,}"
            )

        with col3:
            st.metric(
                "⚠️ Threat Percentage",
                f"{attack_percentage:.2f}%"
            )

        st.divider()


        # Security Level
        if attack_percentage >= 50:
            security_level = "🔴 CRITICAL"
        elif attack_percentage >= 20:
            security_level = "🟠 HIGH"
        elif attack_percentage >= 5:
            security_level = "🟡 MEDIUM"
        else:
            security_level = "🟢 LOW"


        st.subheader("🔐 Security Assessment")

        st.metric(
            "Security Level",
            security_level
        )


        # Threat Alert
        if attack_percentage >= 50:

            st.error(
                "🚨 CRITICAL THREAT: High volume of malicious "
                "network traffic detected!"
            )

        elif attack_percentage >= 20:

            st.warning(
                "⚠️ HIGH THREAT: Suspicious network activity detected."
            )

        elif attack_percentage >= 5:

            st.warning(
                "🟡 MODERATE THREAT: Some suspicious traffic detected."
            )

        else:

            st.success(
                "✅ NETWORK STATUS: Traffic appears mostly safe."
            )


        # Security Summary
        st.subheader("🔐 Security Summary")

        if attack_count > 0:
            security_status = "🚨 THREAT DETECTED"
        else:
            security_status = "🟢 SYSTEM SAFE"


        highest_confidence = (
            result["Confidence"].max()
            if len(result) > 0
            else 0
        )


        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Security Status",
                security_status
            )

        with col2:
            st.metric(
                "Traffic Analyzed",
                f"{total:,}"
            )

        with col3:
            st.metric(
                "Highest Confidence",
                f"{highest_confidence:.2f}%"
            )

        st.divider()


        # Detection chart
        st.subheader("📊 Traffic Classification")

        chart_data = pd.DataFrame(
            {
                "Traffic Type": [
                    "BENIGN",
                    "ATTACK"
                ],
                "Records": [
                    benign_count,
                    attack_count
                ]
            }
        )

        st.bar_chart(
            chart_data.set_index("Traffic Type"),
            width="stretch"
        )

        st.divider()


        # Threat Severity & Risk Score
        st.subheader("🚦 Threat Severity")

        if attack_percentage >= 50:
            severity = "🔴 HIGH"
        elif attack_percentage >= 10:
            severity = "🟠 MEDIUM"
        else:
            severity = "🟢 LOW"


        risk_score = min(
            100,
            attack_percentage
        )


        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Current Threat Level",
                severity
            )

        with col2:
            st.metric(
                "Risk Score",
                f"{risk_score:.2f}/100"
            )


        st.progress(
            int(risk_score),
            text=f"Risk Level: {risk_score:.2f}%"
        )

        st.divider()


        # Model Performance
        st.subheader("🧠 AI Model Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Algorithm",
                "Random Forest"
            )

        with col2:
            st.metric(
                "Features Used",
                "78"
            )

        with col3:
            st.metric(
                "Detection Type",
                "DDoS Detection"
            )

        st.info(
            "SentinelAI uses a Random Forest machine-learning "
            "model to classify network traffic as BENIGN or ATTACK."
        )

        st.divider()


        # ML Evaluation
        if "Actual" in result.columns:

            with st.expander("📈 ML Model Evaluation", expanded=False):

                actual = result["Actual"]
            predicted = result["Prediction"]

            evaluation_accuracy = accuracy_score(
                actual,
                predicted
            )

            evaluation_precision = precision_score(
                actual,
                predicted,
                pos_label="ATTACK",
                zero_division=0
            )

            evaluation_recall = recall_score(
                actual,
                predicted,
                pos_label="ATTACK",
                zero_division=0
            )

            evaluation_f1 = f1_score(
                actual,
                predicted,
                pos_label="ATTACK",
                zero_division=0
            )


            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Accuracy",
                    f"{evaluation_accuracy * 100:.2f}%"
                )

            with col2:
                st.metric(
                    "Precision",
                    f"{evaluation_precision * 100:.2f}%"
                )

            with col3:
                st.metric(
                    "Recall",
                    f"{evaluation_recall * 100:.2f}%"
                )

            with col4:
                st.metric(
                    "F1 Score",
                    f"{evaluation_f1 * 100:.2f}%"
                )


            st.markdown("### Confusion Matrix")

            matrix = confusion_matrix(
                actual,
                predicted,
                labels=["BENIGN", "ATTACK"]
            )

            matrix_df = pd.DataFrame(
                matrix,
                index=["Actual BENIGN", "Actual ATTACK"],
                columns=["Predicted BENIGN", "Predicted ATTACK"]
            )

            st.dataframe(
                matrix_df,
                width="stretch"
            )

            st.caption(
                "Evaluation is calculated on the uploaded dataset "
                "using its available ground-truth labels."
            )

            st.divider()


        # AI Prediction Preview
        st.subheader("🤖 AI Prediction Preview")

        preview = result[
            ["Prediction", "Confidence"]
        ].head(20).copy()


        preview["Confidence"] = (
            preview["Confidence"]
            .round(2)
            .astype(str)
            + "%"
        )


        st.dataframe(
            preview,
            width="stretch"
        )

        st.divider()


        # Attack Details
        st.subheader("🚨 Detected Attack Traffic")

        attack_data = result[
            result["Prediction"] == "ATTACK"
        ].copy()


        if len(attack_data) > 0:

            st.warning(
                f"{len(attack_data):,} suspicious network "
                "records detected by SentinelAI."
            )


            attack_preview = attack_data.copy()

            attack_preview["Confidence"] = (
                attack_preview["Confidence"]
                .round(2)
                .astype(str)
                + "%"
            )


            preferred_columns = [
                "Destination Port",
                "Flow Duration",
                "Total Fwd Packets",
                "Total Backward Packets",
                "Prediction",
                "Confidence"
            ]


            display_columns = [
                column
                for column in preferred_columns
                if column in attack_preview.columns
            ]


            st.dataframe(
                attack_preview[display_columns].head(100),
                width="stretch"
            )


            st.caption(
                "Showing the first 100 detected attack records."
            )

        else:

            st.success(
                "✅ No attack traffic detected."
            )

        st.divider()


        # Visual Analytics
        st.subheader("📊 Visual Analytics")

        st.markdown("### 🚨 Attack Distribution")

        distribution_data = pd.DataFrame(
            {
                "Traffic Type": [
                    "BENIGN",
                    "ATTACK"
                ],
                "Records": [
                    benign_count,
                    attack_count
                ]
            }
        )

        st.bar_chart(
            distribution_data.set_index("Traffic Type"),
            width="stretch"
        )

        st.caption(
            "Distribution of benign and potentially malicious "
            "network traffic detected by SentinelAI."
        )

        st.divider()


        st.markdown("### 🎯 Confidence Distribution")

        # Limit visualization to avoid rendering hundreds of thousands of points
        confidence_sample = result["Confidence"].head(5000)

        confidence_data = pd.DataFrame(
            {
                "Confidence": confidence_sample
            }
        )

        st.line_chart(
            confidence_data,
            width="stretch"
        )

        st.caption(
            "Confidence distribution shown for a sample of up to 5,000 records "
            "to maintain dashboard performance."
        )

        st.caption(
            "Model confidence for each network traffic prediction."
        )

        st.divider()


      

        # Recommended Security Actions
        st.subheader("🛡️ Recommended Security Actions")

        if attack_percentage >= 50:

            st.error(
                "🚨 IMMEDIATE ACTION REQUIRED"
            )

            st.markdown("""
            **Recommended Actions:**
            - 🔴 Isolate the affected network/system
            - 🔴 Review and block suspicious sources
            - 🔴 Enable appropriate firewall protection
            - 🔴 Monitor incoming and outgoing traffic
            - 🔴 Investigate the detected malicious traffic
            """)

        elif attack_percentage >= 20:

            st.warning(
                "⚠️ HIGH RISK ACTIVITY DETECTED"
            )

            st.markdown("""
            **Recommended Actions:**
            - 🟠 Review suspicious network connections
            - 🟠 Check firewall and security logs
            - 🟠 Monitor unusual traffic patterns
            - 🟠 Consider blocking suspicious sources
            """)

        elif attack_percentage >= 5:

            st.warning(
                "🟡 MODERATE RISK DETECTED"
            )

            st.markdown("""
            **Recommended Actions:**
            - 🟡 Continue monitoring network traffic
            - 🟡 Review detected attack records
            - 🟡 Check unusual connection patterns
            - 🟡 Keep firewall and security systems enabled
            """)

        else:

            st.success(
                "🟢 NETWORK TRAFFIC APPEARS SAFE"
            )

            st.markdown("""
            **Recommended Actions:**
            - 🟢 Continue normal network monitoring
            - 🟢 Keep security systems updated
            - 🟢 Maintain firewall protection
            """)

        st.divider()


        # Scan History
        scan_record = {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "File": uploaded_file.name,
            "Records": total,
            "Attacks": attack_count,
            "Benign": benign_count
        }


        existing_files = [
            item["File"]
            for item in st.session_state.scan_history
        ]


        if uploaded_file.name not in existing_files:

            st.session_state.scan_history.append(
                scan_record
            )


        st.subheader("📋 Scan History")

        if st.session_state.scan_history:

            history_df = pd.DataFrame(
                st.session_state.scan_history
            )

            st.dataframe(
                history_df,
                width="stretch"
            )

        else:

            st.info(
                "No scans performed yet."
            )

        st.divider()


        # Download results
        csv_data = result.to_csv(
            index=False
        )


        st.download_button(
            label="📥 Download Prediction Results",
            data=csv_data,
            file_name="sentinelai_predictions.csv",
            mime="text/csv"
        )


    except Exception as error:

        st.error(
            f"SentinelAI could not analyze the dataset: {error}"
        )


else:

    st.info(
        "Upload a network traffic CSV to start SentinelAI analysis."
    )