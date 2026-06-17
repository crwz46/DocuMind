import json
import os
import tempfile
from pathlib import Path

import streamlit as st

from documind.qa_pipeline import QAPipeline

st.set_page_config(page_title="DocuMind — Extract & Export", page_icon="📊", layout="wide")

if "user" not in st.session_state:
    st.switch_page("main.py")

user = st.session_state["user"]
pipeline = QAPipeline(user_id=user["id"])

st.markdown("# Extract & Export")

tab1, tab2 = st.tabs(["Auto Extract", "Custom Schema"])

with tab1:
    st.markdown("### Extract structured data automatically")
    st.markdown("The AI detects entities, fields, and relationships from your documents.")

    docs = pipeline.list_documents()
    if docs:
        doc_names = [d["source"] for d in docs]
        selected = st.selectbox("Select document", doc_names, key="auto_doc")
        if st.button("Extract Data", type="primary", use_container_width=True):
            with st.spinner("Extracting structured data..."):
                try:
                    result = pipeline.extract(source=selected)
                    if result:
                        st.session_state["extracted_data"] = result
                        st.success(f"Extracted {len(result)} records")
                        st.json(result[:5])
                        json_str = json.dumps(result, indent=2, default=str)
                        st.download_button(
                            "Download JSON",
                            data=json_str,
                            file_name=f"{Path(selected).stem}_extracted.json",
                            mime="application/json",
                        )
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
                        try:
                            pipeline.export_excel(result, tmp)
                            with open(tmp, "rb") as f:
                                st.download_button(
                                    "Download Excel File",
                                    data=f,
                                    file_name=f"{Path(selected).stem}_extracted.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                )
                        finally:
                            os.unlink(tmp)
                    else:
                        st.warning("No data extracted. Try a different document.")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("No documents in knowledge base. Upload documents first.")

with tab2:
    st.markdown("### Define your own schema")
    st.markdown("Specify the fields you want to extract:")

    if "schema_fields" not in st.session_state:
        st.session_state["schema_fields"] = [
            {"name": "name", "desc": "Full name or item name"},
            {"name": "date", "desc": "Date (YYYY-MM-DD)"},
            {"name": "amount", "desc": "Monetary amount"},
            {"name": "status", "desc": "Status or category"},
        ]

    fields_to_remove = []
    for i, field in enumerate(st.session_state["schema_fields"]):
        cols = st.columns([2, 2, 1])
        with cols[0]:
            st.session_state["schema_fields"][i]["name"] = st.text_input(
                "Field name", value=field["name"], key=f"schema_name_{i}", label_visibility="collapsed"
            )
        with cols[1]:
            st.session_state["schema_fields"][i]["desc"] = st.text_input(
                "Description", value=field["desc"], key=f"schema_desc_{i}", label_visibility="collapsed"
            )
        with cols[2]:
            if st.button("X", key=f"remove_{i}"):
                fields_to_remove.append(i)

    for i in reversed(fields_to_remove):
        st.session_state["schema_fields"].pop(i)
        st.rerun()

    if st.button("+ Add Field"):
        st.session_state["schema_fields"].append({"name": "", "desc": ""})
        st.rerun()

    docs2 = pipeline.list_documents()
    if docs2 and st.button("Extract with Schema", type="primary", use_container_width=True):
        schema = {f["name"].strip(): f["desc"].strip() for f in st.session_state["schema_fields"] if f["name"].strip()}
        with st.spinner("Extracting structured data..."):
            try:
                result = pipeline.extract_from_chunks(
                    " ".join(schema.values()), top_k=20, schema=schema
                )
                if result:
                    st.session_state["extracted_data"] = result
                    st.success(f"Extracted {len(result)} records")
                    st.dataframe(result[:10], use_container_width=True)
                    json_str = json.dumps(result, indent=2, default=str)
                    st.download_button(
                        "Download JSON", data=json_str, file_name="extracted_schema.json", mime="application/json"
                    )
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
                    try:
                        pipeline.export_excel(result, tmp)
                        with open(tmp, "rb") as f:
                            st.download_button(
                                "Download Excel File", data=f, file_name="extracted_schema.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )
                    finally:
                        os.unlink(tmp)
                else:
                    st.warning("No data extracted.")
            except Exception as e:
                st.error(f"Error: {e}")
