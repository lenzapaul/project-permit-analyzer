
import streamlit as st
import pandas as pd

def load_local_permits(state):
    if state == "West Virginia":
        return pd.read_csv("wv_local_permits_template.csv")
    elif state == "North Carolina":
        return pd.read_csv("nc_local_permits_with_alamance.csv")
    else:
        return pd.DataFrame()

def generate_pcn_checklist(state, project_type, nwp_number):
    checklist = [
        "Completed ENG Form 6082",
        "Project drawings showing impacts to Waters of the U.S.",
        "Wetland delineation report (if applicable)",
        "Jurisdictional Determination (if approved)",
        "Photos of the project site",
        "Description of avoidance and minimization efforts",
        "Stormwater pollution prevention plan (if ≥1 acre disturbed)"
    ]

    if state == "North Carolina":
        checklist.append("IPaC species list and coordination record")
        checklist.append("SHPO coordination (required for most projects)")
        checklist.append("NC Natural Heritage Program species/habitat query")
        checklist.append("Coordination with NC Wildlife Resources Commission (for in-stream or dam removal activities)")
        if project_type in ["Dam Removal", "Aquatic Habitat Restoration"]:
            checklist.append("Fish passage design (if applicable) for NC Wildlife Resources Commission review")

    if state == "West Virginia" or state == "Ohio":
        checklist.append("IPaC species list and coordination record")
        checklist.append("SHPO coordination (if applicable)")

    if project_type == "Dam Removal":
        checklist.append("Detailed demolition and removal plan for low-head dam")
        checklist.append("Stream restoration plan post-removal")

    if project_type == "Aquatic Habitat Restoration":
        checklist.append("Stream restoration design plan (if applicable)")

    return checklist

st.set_page_config(page_title="Project Permit Analyzer", layout="centered")
st.title("Project Permit Analyzer – WV, OH, NC")

state = st.selectbox("Project State", ["West Virginia", "Ohio", "North Carolina"])
county = st.text_input("County or Location Description")
project_type = st.selectbox("Project Type", [
    "Utility Line", "Solar Farm", "Bridge Replacement", "Road Project",
    "Residential Development", "Coal Mining", "Agriculture",
    "Recreation Facility", "Electric/Telecom Line", "Maintenance",
    "Shoreline Stabilization", "Aquatic Habitat Restoration", "Dam Removal", "Other"
])
water_types = st.multiselect("Impacts to Waters of the U.S.", ["Perennial Stream", "Intermittent Stream", "Ephemeral Stream", "Wetland"])
wetland_impact = st.number_input("Wetland Impact (acres)", min_value=0.0, step=0.01)
stream_length = st.number_input("Stream Impact (linear feet)", min_value=0, step=1)
permanent_fill = st.radio("Is the impact permanent?", ["Yes", "No"])
tree_clearing = st.radio("Tree Clearing ≥ 3\" DBH?", ["Yes", "No"])
endangered_species = st.radio("T&E Species Present or Nearby?", ["Yes", "No", "Unknown"])
historic_properties = st.radio("Known or Suspected Historic Properties?", ["Yes", "No", "Unknown"])
tier_3_water = st.radio("Is the project near a Tier 3 / Outstanding Water?", ["Yes", "No", "Unknown"])

if st.button("Analyze Permit Requirements"):
    st.subheader("Required Permits and Notifications")
    output = []

    # NWP Type Assignment
    if project_type == "Utility Line":
        nwp_number = 12
        output.append("- NWP 12 – Utility Line Activities likely applicable.")
    elif project_type == "Solar Farm":
        nwp_number = 51
        output.append("- NWP 51 – Renewable Energy Generation Activities likely applicable.")
    elif project_type == "Residential Development":
        nwp_number = 29
        output.append("- NWP 29 – Residential Developments likely applicable.")
    elif project_type == "Coal Mining":
        nwp_number = 21
        output.extend([
            "- NWP 21 – Surface Coal Mining Activities likely applicable.",
            "- NWP 44 – Mining Activities likely applicable.",
            "- NWP 50 – Underground Coal Mining Activities likely applicable."
        ])
    elif project_type == "Agriculture":
        nwp_number = 40
        output.append("- NWP 40 – Agricultural Activities likely applicable.")
    elif project_type == "Recreation Facility":
        nwp_number = 42
        output.append("- NWP 42 – Recreational Facilities likely applicable.")
    elif project_type == "Electric/Telecom Line":
        nwp_number = 57
        output.append("- NWP 57 – Electric Utility Line and Telecommunications Activities likely applicable.")
    elif project_type == "Maintenance":
        nwp_number = 3
        output.append("- NWP 3 – Maintenance Activities likely applicable.")
    elif project_type == "Shoreline Stabilization":
        nwp_number = 13
        output.append("- NWP 13 – Shoreline Stabilization Activities likely applicable.")
    elif project_type == "Aquatic Habitat Restoration":
        nwp_number = 27
        output.append("- NWP 27 – Aquatic Habitat Restoration, Establishment, and Enhancement Activities likely applicable.")
    elif project_type == "Dam Removal":
        nwp_number = 53
        output.append("- NWP 53 – Removal of Low-Head Dams likely applicable.")
    else:
        nwp_number = 0
        output.append("- Nationwide Permit applicability depends on specific activities.")

    if state == "North Carolina":
        if project_type in ["Utility Line", "Road Project", "Residential Development", "Recreation Facility", "Electric/Telecom Line"]:
            output.append("- PCN Required: This project type requires PCN in North Carolina per Wilmington District regional conditions.")
        if wetland_impact > 0.10:
            output.append("- PCN Required: Wetland impact exceeds 0.10 acre in North Carolina.")
        if stream_length > 150:
            output.append("- PCN Required: Stream impact exceeds 150 linear feet in North Carolina.")
        if endangered_species == "Yes":
            output.append("- ESA Coordination Required: Potential impact to threatened or endangered species.")
        if tree_clearing == "Yes":
            output.append("- PCN Required: Tree clearing may trigger additional review in North Carolina.")
        if project_type in ["Maintenance", "Shoreline Stabilization"]:
            output.append("- General 401 Water Quality Certification likely applies in North Carolina.")
        else:
            output.append("- Individual 401 Water Quality Certification likely required in North Carolina per Wilmington District conditions.")
        if project_type in ["Aquatic Habitat Restoration", "Dam Removal"]:
            output.append("- NC Wildlife Resources Commission coordination required.")
            output.append("- NC Natural Heritage Program species/habitat query required.")

    elif state == "West Virginia":
        if permanent_fill == "Yes" and wetland_impact > 0.10:
            output.append("- PCN Required: Loss of WOTUS > 0.10 acre.")
        elif tree_clearing == "Yes":
            output.append("- PCN Required: Tree clearing ≥ 3\" DBH triggers Regional Condition.")
        if tier_3_water == "Yes":
            output.append("- Individual 401 WQC Required: Project in Tier 3 waters.")
        else:
            output.append("- WV General 401 WQC likely applies.")

    elif state == "Ohio":
        if permanent_fill == "Yes" and wetland_impact > 0.10:
            output.append("- PCN Required: Loss of WOTUS > 0.10 acre.")
        elif tree_clearing == "Yes":
            output.append("- PCN Required: Tree clearing ≥ 3\" DBH triggers Regional Condition.")
        if wetland_impact >= 0.5:
            output.append("- Individual 401 WQC Required: Wetland impact ≥ 0.5 acre.")
        else:
            output.append("- General 401 WQC likely applies.")

    if historic_properties == "Yes":
        output.append("- Section 106 Consultation Required.")
    if endangered_species == "Yes":
        output.append("- ESA Coordination Required: Potential impact to T&E species.")
    output.append("- Stormwater NPDES Permit likely required if ≥1 acre disturbed.")

    for item in output:
        st.markdown(item)

    st.subheader("PCN Submission Checklist")
    checklist = generate_pcn_checklist(state, project_type, nwp_number)
    for item in checklist:
        st.markdown(f"- {item}")

st.subheader("Local Permitting Requirements")
local_permits = load_local_permits(state)
county_permits = local_permits[local_permits['County'].str.lower() == county.strip().lower()]

if not county_permits.empty:
    st.markdown("**Local Permits:**")
    for index, row in county_permits.iterrows():
        st.markdown(f"- **{row['Permit Name']}**: {row['Description']} (Agency: {row['Agency']}, Phone: {row['Phone']})")
    csv = county_permits.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Local Permits CSV",
        data=csv,
        file_name=f"{county}_local_permits.csv",
        mime='text/csv'
    )
else:
    st.markdown("No local permit data available for this county.")
