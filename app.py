from PIL import Image
import streamlit as st
from utils.preprocess import load_file
from utils.rag_utils import SimpleVectorStore
from utils.web_search import serpapi_search
from utils.groq_utils import query_groq
from config.config import Config
import os

# --- Streamlit page setup ---
st.set_page_config(page_title='InterviewPal AI', layout='wide')
logo = Image.open('assets/InterviewPal_logo.png')
st.image(logo, width=160)

st.title('InterviewPal — Personalized Interview Coach')
st.write('Upload resumes, job descriptions, and ask practice interview questions.')

# Show path to the case-study PDF (provided)
st.info('Case study template (provided): /mnt/data/NeoStats AI Engineer Case Study.pdf')

# --- File uploader ---
uploaded = st.file_uploader(
    'Upload resume(s) or job descriptions (pdf / txt)',
    accept_multiple_files=True
)

# --- Vector store session ---
if 'vs' not in st.session_state:
    st.session_state.vs = SimpleVectorStore()

# --- Process uploads ---
docs = []
if uploaded:
    os.makedirs('data', exist_ok=True)
    for f in uploaded:
        dest = os.path.join('data', f.name)
        with open(dest, 'wb') as out:
            out.write(f.getbuffer())

        try:
            txt = load_file(dest)
            docs.append(txt)
        except Exception as e:
            st.error(f'Failed to read {f.name}: {e}')

    if docs:
        st.session_state.vs.upsert_documents(docs)
        st.success('Documents indexed for retrieval.')

# --- Response mode selector ---
mode = st.radio('Response Mode', ['Concise', 'Detailed'])

# --- User prompt ---
prompt = st.text_input('Ask a question or start a mock-interview:')

# --- Handle query ---
if st.button('Submit') and prompt:

    # Combine uploaded document text for Groq context
    doc_text = "\n".join(docs[:5])  # limit to first 5 docs to avoid huge prompts

    # 1️⃣ Query Groq with document context
    groq_results = []
    if Config.GROQ_API_KEY:
        groq_prompt = f"Here are the user's uploaded documents:\n{doc_text}\n\nQuestion: {prompt}" if doc_text else prompt
        groq_results = query_groq(groq_prompt)

        if groq_results:
            st.subheader(f'Result — {mode} (Groq)')
            if mode == 'Concise':
                for r in groq_results[:6]:
                    st.write(f"• {r}")
            else:
                for r in groq_results:
                    st.write(f"- {r}\n")

    # 2️⃣ Fallback to local documents if Groq returned nothing
    if not groq_results and docs:
        hits = st.session_state.vs.retrieve(prompt, k=6)
        if hits:
            st.subheader(f'Result — {mode} (Local Documents)')
            if mode == 'Concise':
                for h in hits:
                    st.write(f"• {h}")
            else:
                for h in hits:
                    st.write(f"- {h}\n")

    # 3️⃣ Fallback to web search if nothing else
    if not groq_results and (not docs or not hits):
        web = serpapi_search(prompt, num=3)
        st.subheader(f'Result — {mode} (Web Fallback)')
        fallback_answer = "No matching information found in your uploaded documents.\nHere is what I found online:\n\n"
        for r in web:
            fallback_answer += f"- {r['title']}: {r['snippet']}\n"
        st.write(fallback_answer)
