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

# --- Full KEYWORDS dict ---
KEYWORDS = {
    'Meat': [
        'Rump steak','Scotch fillet','Porterhouse steak','T-bone steak','Beef mince','Diced beef',
        'Beef schnitzel','Beef stir-fry strips','Beef sausages','Corned beef silverside','Beef roast',
        'Lamb chops','Lamb cutlets','Lamb leg roast','Lamb shanks','Diced lamb','Lamb mince',
        'Lamb sausages','Pork chops','Pork belly','Pork roast','Pork spare ribs','Diced pork',
        'Pork mince','Pork sausages','Pork schnitzel','Whole chicken','Chicken breast','Chicken thighs',
        'Chicken drumsticks','Chicken wings','Chicken tenderloins','Chicken mince','Chicken schnitzel',
        'Chicken marylands','Roast beef slices','Pastrami','Corned beef slices','Champagne ham',
        'Virginian ham','Honey leg ham','Triple smoked ham','Shaved chicken breast','Turkey breast slices',
        'Salami','Prosciutto','Sopressa','Mortadella','Pepperoni','Kassler','Bacon','Frankfurts',
        'Kransky','Chorizo','Cocktail sausages','Kabana','Devon','Liverwurst','Pâté',
        'Marinated chicken wings','Marinated chicken drumsticks','Meat kebabs','Rissoles',
        'Burger patties','Honey soy chicken portions','BBQ pork ribs','Pre-marinated pork belly',
        'Lemon herb chicken thighs'
    ],
    'Vegetables and Fruits': [
        'Apples','Bananas','Oranges','Mandarins','Pears','Peaches','Plums','Nectarines',
        'Grapes','Kiwifruit','Pineapple','Mangoes','Watermelon','Rockmelon','Cantaloupe',
        'Strawberries','Blueberries','Raspberries','Blackberries','Lemons','Limes','Avocados',
        'Tomatoes','Cherry tomatoes','Grape tomatoes','Cucumbers','Zucchini','Carrots','Celery',
        'Lettuce','Cos lettuce','Iceberg lettuce','Mixed salad leaves','Rocket','Spinach',
        'Silverbeet','Kale','Cabbage','Red cabbage','Savoy cabbage','Broccoli','Cauliflower',
        'Green beans','Snow peas','Sugar snap peas','Capsicum','Chillies','Eggplant','Pumpkin',
        'Sweet potato','Potatoes','Onions','Onion','Garlic','Shallots','Spring onions','Leeks','Mushrooms',
        'Corn','Green peas','Brussels sprouts','Beetroot','Radish','Fennel','Asparagus','Artichoke',
        'Parsnip','Chokos','Passionfruit','Papaya','Pomegranate','Coconut','Dates','Figs','Persimmon',
        'Lychee','Dragonfruit','Rambutan','Starfruit','Basil','Coriander','Parsley','Mint',
        'Dill','Chives','Thyme','Rosemary','Sage','Tarragon','Marjoram','Vietnamese mint',
        'Lemongrass','Kaffir lime leaves','Bay leaves','Curry leaves'
    ],
    'Dairy': [
        'Milk','Lactose-free milk','A2 milk','Long-life milk','Flavoured milk','UHT milk',
        'Buttermilk','Cream','Sour cream','Crème fraîche','Yoghurt','Yoghurt tubs','Yoghurt pouches',
        'Skyr','Kefir','Butter','Cultured butter','Spreadable butter','Margarine','Ghee',
        'Cheddar cheese','Tasty cheese','Colby cheese','Mozzarella','Parmesan','Pecorino',
        'Grana Padano','Swiss cheese','Jarlsberg','Havarti','Provolone','Edam','Gouda','Brie',
        'Camembert','Blue cheese','Feta','Goat cheese','Ricotta','Cottage cheese','Cream cheese',
        'Mascarpone','Paneer','Haloumi','Processed cheese slices','Cheese sticks','Shredded cheese blends',
        'Grated cheese','Sliced cheese packs','Parmesan shavings','Custard','Dairy desserts',
        'Milk-based smoothies','Dairy-based dips','Evaporated milk','Condensed milk','Powdered milk'
    ],
    'Bakery': [
        'White bread','Wholemeal bread','Multigrain bread','Soy and linseed bread','Rye bread',
        'Sourdough','Pane di casa','Ciabatta','Turkish bread','Brioche loaf','Vienna loaf',
        'High-fibre loaf','Gluten-free bread','Low-carb bread','Fruit loaf','Raisin toast',
        'English muffins','Crumpets','Bagels','Wraps','Tortillas','Pita bread','Lebanese bread',
        'Flatbread','Pizza bases','Burger buns','Hot dog rolls','Long rolls','Dinner rolls',
        'Seeded rolls','Mini rolls','Cheese and bacon rolls','Scrolls','Croissants',
        'Pain au chocolat','Danish pastries','Cinnamon scrolls','Apple turnovers','Custard tarts',
        'Jam tarts','Vanilla slices','Éclairs','Lamingtons','Swiss rolls','Muffins','Cupcakes',
        'Madeleines','Banana bread','Carrot cake','Mud cake','Sponge cake','Chocolate cake',
        'Birthday cake','Slab cake','Fruit cake','Pound cake','Tea cake','Butter cake',
        'Brownies','Slice bars','Cookies','Biscuits','Shortbread','Anzac biscuits','Gingerbread',
        'Melting moments','Yo-yos','Scones','Pikelets','Waffles','Donuts','Mini donuts',
        'Jam-filled donuts','Iced donuts','Cinnamon donuts','Churros'
    ],
    'Pantry': [
        'Plain flour','Self-raising flour','Wholemeal flour','Bread flour','00 flour','Rice flour',
        'Cornflour','Almond meal','Coconut flour','Polenta','Semolina','Rolled oats','Quick oats',
        'Steel-cut oats','Muesli','Granola','Cereal','Pasta','Gluten-free pasta','Rice','Couscous',
        'Quinoa','Bulgur','Barley','Lentils','Chickpeas','Black beans','Kidney beans','Cannellini beans',
        'Butter beans','Baked beans','Tinned tomatoes','Tomato paste','Tomato passata','Coconut milk',
        'Coconut cream','Canned corn','Canned mushrooms','Canned beetroot','Canned fruit','Tuna',
        'Salmon','Sardines','Anchovies','Corned beef','SPAM','Canned chicken','Soup cans','Stock',
        'Bouillon cubes','Gravy powder','Packet sauces','Instant noodles','Rice vermicelli','Egg noodles',
        'Udon noodles','Soba noodles','Nori sheets','Breadcrumbs','Crackers','Rice cakes','Corn cakes',
        'Crispbread','Biscuits','Chocolate biscuits','Wafers','Muesli bars','Nut bars','Cake mixes',
        'Brownie mix','Pudding mix','Custard powder','Gelatine','Baking powder','Baking soda','Yeast',
        'Icing sugar','Caster sugar','White sugar','Brown sugar','Golden syrup','Maple syrup','Honey',
        'Molasses','Agave syrup','Peanut butter','Almond butter','Tahini','Hazelnut spread','Jam',
        'Marmalade','Vegemite','Marmite','Chutney','Relish','Mustard','Mayonnaise','Aioli','Tomato sauce',
        'BBQ sauce','Soy sauce','Tamari','Teriyaki sauce','Hoisin sauce','Oyster sauce','Fish sauce',
        'Sriracha','Hot sauce','Curry paste','Sambal oelek','Vinegar','Olive oil','Vegetable oil',
        'Canola oil','Sunflower oil','Sesame oil','Peanut oil','Salt','Himalayan salt','Sea salt flakes',
        'Iodised salt','Black pepper','Peppercorns','Mixed herbs','Thyme','Parsley','Basil','Sage',
        'Tarragon','Marjoram','Bay leaves','Chilli flakes','Paprika','Smoked paprika',
        'Ground cumin','Ground coriander','Curry powder','Garam masala','Turmeric','Cinnamon','Nutmeg',
        'Vanilla extract','Food colouring','Sprinkles'
    ],
    'Frozen': [
        'Peas','Corn','Green beans','Mixed vegetables','Broccoli','Cauliflower','Stir-fry vegetable mix','Spinach',
        'Edamame','Sweet potato','Avocado pieces','Onions','Diced capsicum','Blueberries','Raspberries',
        'Mixed berries','Mango','Banana','Cherries','Pineapple','Fruit salad','Acai puree','Smoothie packs',
        'Oven fries','Potato wedges','Hash browns','Potato gems','Mashed potato','Onion rings',
        'Crumbed mushrooms','Battered cauliflower','Vegetable patties','Falafel','Veggie nuggets',
        'Veggie burgers','Plant-based mince','Plant-based sausages','Plant-based chicken','Beef mince',
        'Chicken breast','Chicken nuggets','Chicken schnitzels','Chicken tenders','Chicken wings',
        'Chicken kievs','Whole chicken','Turkey breast','Duck','Pork roast','Beef burgers','Steak',
        'Meat pies','Sausage rolls','Pizza','Mini pizzas','Garlic bread','Lasagna','Pasta meals',
        'Cannelloni','Ravioli','Gnocchi','Pasta sheets','Dumplings','Gyoza','Spring rolls','Samosas',
        'Roti','Naan','Paratha','Puff pastry','Shortcrust pastry','Filo pastry','Pastry sheets','Quiches',
        'Savoury pastries','Fish fillets','Salmon portions','Prawns','Calamari','Seafood marinara mix',
        'Seafood baskets','Fish fingers','Crab sticks','Dim sims','Bao buns','Pancakes','Waffles',
        'Crumpets','Croissants','Brioche buns','Muffins','Yorkshire puddings','Scones','Cakes',
        'Cheesecakes','Tarts','Desserts','Ice cream','Gelato','Sorbet','Yoghurt','Icy poles',
        'Fruit bars','Ice cubes','Baby food','Dog food','Cat food'
    ]
}

def sanitize_text(text):
    bad_chars = ['\u200b','\u00a0','\u2028','\u2029','\u2009','\u2002','\u2003','\u2004','\u2005','\u2006','\u2007']
    for c in bad_chars:
        text = text.replace(c, ' ')
    ligatures = {'ﬀ':'ff','ﬁ':'fi','ﬂ':'fl','ﬃ':'ffi','ﬄ':'ffl'}
    for lig, rep in ligatures.items():
        text = text.replace(lig, rep)
    text = text.replace('–','-').replace('—','-')
    return ' '.join(text.split())

def categorize_ingredients(ingredients):
    categories = {sec: [] for sec in KEYWORDS}
    for item in ingredients:
        clean = sanitize_text(item)
        name = re.sub(r'^[\d/]+\s*', '', clean).lower()
        placed = False
        for sec, keys in KEYWORDS.items():
            for k in keys:
                kl = k.lower()
                variants = {kl, kl.rstrip('s')}
                for v in variants:
                    if name.startswith(v) or f' {v}' in name:
                        categories[sec].append(item)
                        placed = True
                        break
                if placed:
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
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, sanitize_text(title), ln=True)
    pdf.ln(2)

    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, 'Ingredients', ln=True)
    pdf.set_font('helvetica', '', 11)
    for item in ingredients:
        pdf.cell(0, 6, f'- {item}', ln=True)
    pdf.ln(4)

    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, 'Method', ln=True)
    pdf.set_font('helvetica', '', 11)
    url_pat = r'(https?://[^\s]+)'
    for i, step in enumerate(method, 1):
        pdf.write(6, f'{i}. ')
        parts = re.split(url_pat, step)
        for part in parts:
            if re.match(url_pat, part):
                pdf.set_text_color(0, 0, 255)
                pdf.write(6, part, link=part)
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.write(6, part)
        pdf.ln(8)
    pdf.ln(4)

    urls = []
    for step in method:
        for u in re.findall(url_pat, step):
            if u not in urls:
                urls.append(u)
    if urls:
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 8, 'Links', ln=True)
        pdf.set_font('helvetica', '', 11)
        for u in urls:
            pdf.set_text_color(0, 0, 255)
            pdf.write(6, u, link=u)
            pdf.ln(6)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

    pdf.add_page()
    if shopping_categories:
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 8, 'Shopping List', ln=True)
        pdf.set_font('helvetica', '', 11)
        for sec, items in shopping_categories.items():
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(0, 6, sec, ln=True)
            pdf.set_font('helvetica', '', 11)
            if items:
                for it in items:
                    pdf.cell(0, 6, f'- {it}', ln=True)
            else:
                pdf.cell(0, 6, '- none', ln=True)
            pdf.ln(2)

    return pdf.output(dest='S').encode('latin1')

def display_recipe(title, ingredients, method):
    st.subheader(title)
    st.markdown('**Ingredients**')
    for item in ingredients:
        st.text(item)  # Each ingredient as a plain line, no dashes, no bullets
    st.markdown('**Method**')
    for i, step in enumerate(method, 1):
        st.markdown(f'{i}. {step}')

def display_shopping(categories):
    st.subheader('Shopping List')
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

    # Collect recipes via text areas or uploads
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

    # PROCESS only if button pressed
    if st.button('Generate Recipe'):
        if not recipes:
            st.info('Enter at least one recipe or upload files.')
            return

        all_pdfs = []
        for txt in recipes:
            # ... process each recipe ...
            title, ingredients, method = parse_recipe(txt)

            if not ingredients or not method:
                st.warning(f"Skipping '{title}': missing sections.")
                continue

            display_recipe(title, ingredients, method)
            cats = categorize_ingredients(ingredients)
            display_shopping(cats)

            pdf_bytes = create_pdf(title, ingredients, method, shopping_categories=cats)
            fn = f"{title.replace(' ', '_').lower()}.pdf"
            all_pdfs.append((fn, pdf_bytes))
            st.download_button('Download PDF', data=pdf_bytes, file_name=fn, mime='application/pdf')
            st.markdown('---')

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as zf:
            for fn, data in all_pdfs:
                zf.writestr(fn, data)
        st.download_button('Download All PDFs', data=buf.getvalue(), file_name='recipes.zip', mime='application/zip')

if __name__ == '__main__':
    main()
