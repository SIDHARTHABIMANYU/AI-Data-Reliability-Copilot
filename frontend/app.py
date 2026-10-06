import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Data Reliability Copilot",
    page_icon="🤖",
    layout="wide",
)


st.title("AI Data Reliability Copilot")
st.caption("Monitor pipeline incidents and AI-assisted remediation")


# --------------------------------------------------
# Dashboard Summary
# --------------------------------------------------

st.header("Pipeline Reliability Overview")

try:
    response = requests.get(
        f"{API_URL}/dashboard/summary",
        timeout=10
    )

    response.raise_for_status()

    summary = response.json()

except requests.RequestException as error:

    st.error(
        f"Unable to connect to backend: {error}"
    )

    st.stop()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Incidents",
        summary["total_incidents"]
    )

with col2:
    st.metric(
        "Open Incidents",
        summary["open_incidents"]
    )

with col3:
    st.metric(
        "High Severity",
        summary["high_severity_incidents"]
    )

with col4:
    st.metric(
        "Pending Remediations",
        summary["pending_remediations"]
    )


st.divider()


# --------------------------------------------------
# Incident Investigation
# --------------------------------------------------

st.header("Incident Investigation")

incident_id = st.number_input(
    "Incident ID",
    min_value=1,
    step=1,
    value=1
)


if st.button("Investigate Incident"):

    with st.spinner("Collecting evidence and investigating..."):

        try:
            response = requests.get(
                f"{API_URL}/incidents/{incident_id}/investigation",
                timeout=60
            )

            response.raise_for_status()

            investigation = response.json()

        except requests.RequestException as error:

            st.error(
                f"Investigation failed: {error}"
            )

        else:

            st.subheader("AI Investigation")

            st.write(
                investigation["summary"]
            )

            st.markdown("### Root Cause")

            st.write(
                investigation["root_cause"]
            )

            st.markdown("### Evidence")

            for item in investigation["evidence"]:
                st.write(f"- {item}")

            st.markdown("### Impact")

            for item in investigation["impact"]:
                st.write(f"- {item}")

            st.markdown("### Recommended Action")

            st.info(
                investigation["recommended_action"]
            )

            st.markdown("### Confidence")

            st.success(
                investigation["confidence"]
            )


# --------------------------------------------------
# AI Remediation
# --------------------------------------------------

st.divider()

st.header("AI Suggested Remediation")


if st.button("Generate Remediation"):

    with st.spinner("Generating remediation recommendation..."):

        try:
            response = requests.get(
                f"{API_URL}/incidents/{incident_id}/remediation",
                timeout=60
            )

            response.raise_for_status()

            remediation = response.json()

        except requests.RequestException as error:

            st.error(
                f"Remediation generation failed: {error}"
            )

        else:

            st.subheader("Proposed Change")

            st.write(
                remediation["proposed_change"]
            )

            st.markdown("### Problem")

            st.write(
                remediation["problem"]
            )

            st.markdown("### Validation Steps")

            for step in remediation["validation_steps"]:
                st.write(f"- {step}")

            st.markdown("### Risk")

            st.warning(
                remediation["risk"]
            )

            st.markdown("### Approval Required")

            st.write(
                remediation["requires_approval"]
            )

            st.session_state["remediation_id"] = (
                remediation["remediation_id"]
            )


# --------------------------------------------------
# Human Approval
# --------------------------------------------------

st.divider()

st.header("Human Approval")

remediation_id = st.session_state.get(
    "remediation_id"
)

if remediation_id:

    st.write(
        f"Remediation ID: `{remediation_id}`"
    )

    approved_by = st.text_input(
        "Engineer name",
        value="Sidharth"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Approve Remediation"):

            response = requests.post(
                f"{API_URL}/remediations/{remediation_id}/approve",
                json={
                    "approved_by": approved_by
                },
                timeout=30
            )

            if response.ok:
                st.success(
                    "Remediation approved."
                )
            else:
                st.error(
                    response.text
                )

    with col2:

        if st.button("Reject Remediation"):

            response = requests.post(
                f"{API_URL}/remediations/{remediation_id}/reject",
                json={
                    "approved_by": approved_by
                },
                timeout=30
            )

            if response.ok:
                st.warning(
                    "Remediation rejected."
                )
            else:
                st.error(
                    response.text
                )

else:

    st.info(
        "Generate a remediation recommendation first."
    )