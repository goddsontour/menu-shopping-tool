import streamlit as st
import io
import zipfile
import re
from fpdf import FPDF

# --- Password protection in sidebar ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd = st.sidebar.text_input("Enter password:", type="password")
    if pwd == st.secrets["app_password"]:
        st.session_state.authenticated = True
        st.rerun()
    elif pwd:
        st.sidebar.error("Incorrect password")
        st.stop()
    else:
        st.stop()

# --- Page config & custom CSS ---
st.set_page_config(
    page_title="Recipe & Shopping List Generator",
    page_icon=":shallow_pan_of_food:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
      .stApp { background-color: #F5F5F5; }
      header, footer { background-color: #B3E5FC !important; }
      .stDownloadButton>button { background-color: #1E88E5 !important; color: white !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# [KEYWORDS omitted for brevity, use your existing KEYWORDS dict here!]

def sanitize_text(text):
    bad_chars = ['\u200b','\u00a0','\u2028','\u2029','\u2009','\u2002','\u2003','\u2004','\u2005','\u2006','\u2007']
    for c in bad_chars:
        text = text.replace(c, ' ')
    ligatures = {'ﬀ':'ff','ﬁ':'fi','ﬂ':'fl','ﬃ':'ffi','ﬄ':'ffl'}
    for lig, rep in ligatures.items():
        text = text.replace(lig, rep)
    text = text.replace('–','-').replace('—','-')
    return ' '.join(text.split())

def normalize(word):
    return re.sub(r'[^a-z0-9]', '', word.lower().strip())

def categorize_ingredients(ingredients):
    categories = {sec: [] for sec in KEYWORDS}
    keyword_lookup = {}
    for sec, items in KEYWORDS.items():
        keyword_lookup[sec] = set()
        for k in items:
            keyword_lookup[sec].add(normalize(k))
            if k.endswith('s'):
                keyword_lookup[sec].add(normalize(k[:-1]))
    for item in ingredients:
        clean = sanitize_text(item)
        base = re.sub(r'^[\d/]+\s*', '', clean)
        words = normalize(base)
        placed = False
        for sec in KEYWORDS:
            for k in keyword_lookup[sec]:
                if k and (words.startswith(k) or k in words):
                    categories[sec].append(item)
                    placed = True
                    break
            if placed:
                break
        if not placed:
            categories['Pantry'].append(item)
    return categories

def parse_recipe(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return "Untitled", [], []
    title = lines[0]
    i1 = i2 = None
    for idx, line in enumerate(lines):
        low = line.lower().replace(' ', '')
        if i1 is None and low.startswith("ingredients"):
            i1 = idx
        elif i1 is not None and low.startswith("method"):
            i2 = idx
            break
    if i1 is None or i2 is None or i2 <= i1:
        return title, [], []
    raw_ing = lines[i1+1:i2]
    ingredients = []
    for line in raw_ing:
        parts = re.split(r"[–—\-•]", line)
        for part in parts:
            clean = sanitize_text(part)
            if clean:
                ingredients.append(clean)
    method = []
    for step in lines[i2+1:]:
        clean = sanitize_text(step)
        if clean:
            method.append(clean)
    return title, ingredients, method

def create_pdf(title, ingredients, method, shopping_categories=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, sanitize_text(title), ln=True)
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Ingredients', ln=True)
    pdf.set_font('Arial', '', 11)
    for item in ingredients:
        pdf.cell(0, 6, f"{item}", ln=True)
    pdf.ln(4)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Method', ln=True)
    pdf.set_font('Arial', '', 11)
    url_pat = r'(https?://[^\s]+)'
    for i, step in enumerate(method, 1):
        clean_step = re.sub(r'^\d+\.\s*', '', step)
        pdf.write(6, f"{i}. {clean_step}")
        pdf.ln(8)
    pdf.ln(4)
    urls = []
    for step in method:
        for u in re.findall(url_pat, step):
            if u not in urls:
                urls.append(u)
    if urls:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, 'Links', ln=True)
        pdf.set_font('Arial', '', 11)
        for u in urls:
            pdf.set_text_color(0, 0, 255)
            pdf.write(6, u, link=u)
            pdf.ln(6)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)
    pdf.add_page()
    if shopping_categories:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, 'Shopping List', ln=True)
        pdf.set_font('Arial', '', 11)
        for sec, items in shopping_categories.items():
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 6, sec, ln=True)
            pdf.set_font('Arial', '', 11)
            if items:
                for it in items:
                    pdf.cell(0, 6, f'- {it}', ln=True)
            else:
                pdf.cell(0, 6, '- none', ln=True)
            pdf.ln(2)
    return pdf.output(dest='S').encode('latin1')

def display_recipe(title, ingredients, method, index):
    st.subheader(title)
    st.markdown('**Ingredients**')
    for item in ingredients:
        st.markdown(f"{item}")
    st.markdown('**Method**')
    for i, step in enumerate(method, 1):
        clean_step = re.sub(r'^\s*\d+\s*[\.\)]?\s*', '', step)
        st.markdown(f"{i}. {clean_step}")

def display_shopping(categories):
    st.subheader('Combined Shopping List')
    for sec, items in categories.items():
        st.markdown(f'**{sec}**')
        if items:
            for it in items:
                st.markdown(f'- {it}')
        else:
            st.markdown('- none')

def main():
    st.title('Recipe & Shopping List Generator')
    recipes = []
    tabs = st.tabs([f'Recipe {i+1}' for i in range(4)])
    for i, tab in enumerate(tabs):
        with tab:
            txt = st.text_area(f'Paste Recipe #{i+1}', key=f'r{i}', height=150)
            if txt.strip():
                recipes.append(txt)
    uploaded = st.file_uploader('Or upload up to 4 .txt files', type='txt', accept_multiple_files=True)
    if uploaded:
        for f in uploaded[:4]:
            recipes.append(f.read().decode('utf-8'))

    if st.button('Generate Recipe'):
        if not recipes:
            st.info('Enter at least one recipe or upload files.')
            return

        all_ingredients = []
        for index, txt in enumerate(recipes):
            title, ingredients, method = parse_recipe(txt)
            if not ingredients or not method:
                st.warning(f"Skipping '{title}': missing sections.")
                continue
            display_recipe(title, ingredients, method, index)
            cats = categorize_ingredients(ingredients)
            pdf_bytes = create_pdf(title, ingredients, method, shopping_categories=cats)
            fn = f"{title.replace(' ', '_').lower()}.pdf"
            st.download_button('Download PDF', data=pdf_bytes, file_name=fn, mime='application/pdf', key=f"pdfbtn{index}")
            st.markdown('---')
            all_ingredients.extend(ingredients)

        combined_shopping = categorize_ingredients(all_ingredients)
        st.header("Combined Shopping List")
        display_shopping(combined_shopping)

if __name__ == '__main__':
    main()
