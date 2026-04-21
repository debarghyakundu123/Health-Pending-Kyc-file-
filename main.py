import streamlit as st
import pandas as pd
import base64
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Smart File Engine", layout="wide")
# =========================
# LOGO
# =========================


# Read video file
video_file = open("download.mp4", "rb")
video_bytes = video_file.read()
video_base64 = base64.b64encode(video_bytes).decode()

# Display as small logo video
st.markdown(f"""
<video id="logoVid" width="200" autoplay muted loop playsinline style="border-radius:10px;">
    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>

<script>
const vid = document.getElementById("logoVid");
vid.playbackRate =8.0;  // 🔥 speed (1 = normal, 2 = 2x, 3 = 3x)
</script>
""", unsafe_allow_html=True)
# =========================
# STYLES
# =========================
st.markdown("""
<style>
.main-title {font-size:36px;font-weight:700;}
.file-card {padding:14px;border-radius:12px;background:#fff;box-shadow:0px 2px 8px rgba(0,0,0,0.05);text-align:center;}
.file-name {font-size:12px;color:#555;margin-top:4px;word-wrap:break-word;}
.file-ok {color:green;font-weight:600;}
.file-miss {color:red;font-weight:500;}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 10px 0;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 16px;
    color: #555;
    margin-bottom: 8px;
}

.author {
    font-size: 14px;
    color: #888;
    font-weight: 500;
}
</style>

<div class="main-header">
    <div class="main-title">📊 Automatic Health Pending KYC File Maker</div>
    <div class="title">Merge • Transform • Analyze — without headaches</div>
    <div class="title"><b> Built by ❤️ Debarghya Kundu</b> | PW81594</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
# HELPERS
# =========================
@st.cache_data
def load_excel(file, sheet):
    return pd.read_excel(file, sheet_name=sheet)

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

def clean_id(df, col):
    df[col] = df[col].astype(str).str.strip().str.replace(".0", "", regex=False)
    return df

def get_sheets(file):
    return pd.ExcelFile(file).sheet_names if file else []

# =========================
# STEP 1: FILE UPLOAD
# =========================
st.markdown("### 🟢 Step 1: Upload Files")

col1, col2, col3 = st.columns(3)

with col1:
    file1 = st.file_uploader("📄 CJ Pending File", type=["xlsx"])
    file2 = st.file_uploader("📄 Data Push Status File", type=["xlsx"])

with col2:
    file3 = st.file_uploader("📄 Tech Remarks File", type=["xlsx"])
    file4 = st.file_uploader("📄 Data Push Pending File", type=["xlsx"])

with col3:
    file5 = st.file_uploader("📄 Overall Pendency File", type=["xlsx"])

# =========================
# FILE STATUS
# =========================
st.markdown("### 📂 File Status")

files = [
    ("CJ Pending File", file1),
    ("Data Push Status File", file2),
    ("Tech Remarks File", file3),
    ("Data Push Pending File", file4),
    ("Overall Pendency File", file5)
]

cols = st.columns(len(files))

for col, (label, f) in zip(cols, files):
    with col:
        if f:
            st.markdown(f"""<div class="file-card">📄 <b>{label}</b>
            <div class="file-name">{f.name}</div>
            <div class="file-ok">✔ Uploaded</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="file-card">📄 <b>{label}</b>
            <div class="file-miss">✖ Missing</div></div>""", unsafe_allow_html=True)

st.divider()

# =========================
# STEP 2: SHEETS
# =========================
# =========================
# STEP 2: SHEETS
# =========================
if all([file1, file2, file3, file4, file5]):
    st.markdown("### 🟡 Step 2: Select Sheets")

    s1, s2, s3, s4, s5 = st.columns(5)

    with s1:
        sheet1 = st.selectbox("CJ Pending File", get_sheets(file1))

    with s2:
        sheet2 = st.selectbox("Data Push Status", get_sheets(file2))

    with s3:
        sheet3 = st.selectbox("Tech Remarks File", get_sheets(file3))

    with s4:
        sheet4 = st.selectbox("Data Push Pending File", get_sheets(file4))

    with s5:
        sheet5 = st.selectbox("Overall Pendency File", get_sheets(file5))

else:
    st.warning("⚠ Please upload all files to proceed")
    st.stop()

st.divider()

# =========================
# STEP 3: MAPPING
# =========================
if all([file1, file2, file3, file4, file5]):

    st.markdown("### 🔵 Step 3: Column Mapping")

    # Show file names clearly
    st.info(f"""
    📄 CJ Pending: **{file1.name}**  
    📄 Data Push Status: **{file2.name}**  
    📄 Tech Remarks: **{file3.name}**  
    📄 Data Push Pending: **{file4.name}**  
    📄 Overall Pendency: **{file5.name}**
    """)

    f1_temp = pd.read_excel(file1, sheet_name=sheet1, nrows=5)
    f2_temp=pd.read_excel(file2, sheet_name= sheet2, nrows=5)
    f3_temp = pd.read_excel(file3, sheet_name=sheet3, nrows=5)
    f4_temp = pd.read_excel(file4, sheet_name=sheet4, nrows=5)
    f5_temp = pd.read_excel(file5, sheet_name=sheet5, nrows=5)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"#### 📄 CJ Pending File ({file1.name})")
        lead_f1 = st.selectbox("LeadID", f1_temp.columns)
        remarks_f1 = st.selectbox("Remarks", f1_temp.columns)
        status_f1 = st.selectbox("Status", f1_temp.columns)

        st.markdown(f"#### 📄 Tech Remarks File ({file3.name})")
        lead_f3 = st.selectbox("LeadID (Tech)", f3_temp.columns)
        tech_f3 = st.selectbox("Tech Remarks", f3_temp.columns)
        sales_f3 = st.selectbox("Pendency", f3_temp.columns)

    with c2:
        st.markdown(f"#### 📄 Data Push Pending File ({file4.name})")
        lead_f4 = st.selectbox("LeadID (Pending)", f4_temp.columns)

        st.markdown(f"#### 📄 Overall Pendency File ({file5.name})")
        lead_f5 = st.selectbox("LeadID (Overall)", f5_temp.columns)
        status_f5 = st.selectbox("Status Overall", f5_temp.columns)

    if st.button("✅ Lock Mapping"):
        st.session_state["mapping_done"] = True
        st.success("Mapping locked successfully ✔")

# =========================
# STEP 4: PROCESS
# =========================
if st.session_state.get("mapping_done"):

    st.markdown("### 🚀 Processing")

    with st.spinner("Running pipeline..."):

        f1 = load_excel(file1, sheet1)
        f2 = load_excel(file2,sheet2)
        f3 = load_excel(file3, sheet3)
        f4 = load_excel(file4, sheet4)
        f5 = load_excel(file5, sheet5)

        # Rename
        f1 = f1.rename(columns={lead_f1:"Leadid", remarks_f1:"Remarks", status_f1:"Status.1"})
        f3 = f3.rename(columns={lead_f3:"Leadid", tech_f3:"New Remarks", sales_f3:"Pendency on"})
        f4 = f4.rename(columns={lead_f4:"Leadid"})
        f5 = f5.rename(columns={lead_f5:"Leadid", status_f5:"Status"})

        # Clean IDs
        for df in [f1, f2, f3, f4, f5]:
            if "Leadid" in df: clean_id(df, "Leadid")
            if "LeadID" in df: clean_id(df, "LeadID")

        # REMOVE DUPLICATES (IMPORTANT)
        f1 = f1.drop_duplicates("Leadid")
        f3 = f3.drop_duplicates("Leadid")
        f2 = f2.drop_duplicates("LeadID")

        # =========================
        # FULL PIPELINE
        # =========================

        merged = f4.drop_duplicates("Leadid")
        merged = merged.merge(f5[["Leadid","Status"]], on="Leadid", how="left")
        merged["Status"] = merged["Status"].fillna("-")

        # SHORTFALL
        status_clean = merged["Status"].astype(str).str.lower().str.replace(" ","").str.replace("-","")
        mask = status_clean == "shortfall"
        merged.loc[mask,["Type","Team"]] = ["Shortfall","CRT"]

        # FILE 3
        merged["Tech"] = merged["Leadid"].map(f3.set_index("Leadid")["New Remarks"]).fillna("-")
        merged["sales"] = merged["Leadid"].map(f3.set_index("Leadid")["Pendency on"]).fillna("-")

        # TECH REVERT
        mask = merged["sales"].str.lower().str.contains("crt|data push", na=False)
        merged.loc[mask,["Type","Team"]] = ["Tech Reverted","CRT"]

        # FILE 1
        merged["sales"] = merged["Leadid"].map(f1.set_index("Leadid")["Remarks"])
        merged["X"] = merged["Leadid"].map(f1.set_index("Leadid")["Status.1"])

        merged["sales"] = merged["sales"].fillna("-").astype(str).str.strip()
        merged["X"] = merged["X"].fillna("-").astype(str).str.strip()

        merged.loc[merged["sales"].isin(["","nan"]),"sales"] = "0"
        merged.loc[merged["X"].isin(["","nan"]),"X"] = "0"

        mask_x = merged["X"] != "-"
        merged.loc[mask_x,"Type"] = merged.loc[mask_x,"X"]

        mask_sales = (merged["sales"]=="0") & (merged["X"]!="-")
        merged.loc[mask_sales,"sales"] = merged.loc[mask_sales,"X"]

        # CJ NOT MAPPED
        mask = merged["Type"].str.lower() == "pending with tech"
        merged.loc[mask,["Type","Team"]] = ["CJ Not Mapped","Tech"]

        # FILE 2
        merged["IsDataPushed"] = merged["Leadid"].map(f2.set_index("LeadID")["IsDataPushed"])
        merged["IsRejectRefundCase"] = merged["Leadid"].map(f2.set_index("LeadID")["IsRejectRefundCase"])

        merged = merged[merged["IsDataPushed"] != 1]

        mask = merged["IsRejectRefundCase"] == 1
        merged.loc[mask,["Type","Team"]] = ["Rejected In Pre Issuance","CRT"]

        merged.drop(columns=["X"], errors="ignore", inplace=True)
        merged = merged.drop_duplicates("Leadid")
        merged.rename(columns={"Status": "CRT"}, inplace=True)
        # =========================
        # OUTPUT
        # =========================
        st.success("✅ Done!")

        st.dataframe(merged.head(100), use_container_width=True)
        st.metric("Total Rows", len(merged))

        merged.to_excel("Health_Pending.xlsx", index=False)

        with open("Health_Pending.xlsx", "rb") as f:
            st.download_button("⬇ Download Result", f, "Health_Pending.xlsx")
