# TEST LINE 12345
import streamlit as st

# --- Page config & custom CSS (login shares home bg) ---
st.set_page_config(
    page_title="Recipe & Shopping List Generator",
    page_icon=":shallow_pan_of_food:",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
      body, .stApp { background-color: #F5F5F5 !important; }
      .centered-card {
          max-width: 400px;
          margin: 80px auto 0 auto;
          padding: 2.5rem 2.5rem 2rem 2.5rem;
          background: #ffffffcc;
          border-radius: 2rem;
          box-shadow: 0 8px 32px rgba(30,136,229,0.11);
      }
      .login-title {
          text-align: center;
          margin-bottom: 0.5rem;
          font-size: 2.1rem;
          color: #1E88E5;
          font-weight: 600;
          letter-spacing: 0.5px;
      }
      .login-desc {
          text-align: center;
          font-size: 1.04rem;
          color: #333;
          margin-bottom: 1.7rem;
      }
      .stTextInput>div>div>input {
          font-size: 1.12rem;
          padding: 0.6rem 0.9rem;
          border-radius: 0.6rem;
          border: 1.5px solid #90caf9;
          background: #fafbfc;
      }
      .stButton>button {
          background-color: #1E88E5 !important;
          color: white !important;
          border-radius: 0.7rem !important;
          font-size: 1.09rem !important;
          padding: 0.55rem 0.9rem !important;
      }
    </style>
    """, unsafe_allow_html=True
)

def show_login():
    st.markdown('<div class="centered-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Welcome to Kind Kitchen</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-desc">Enter your password to start creating menus, recipes, and shopping lists.</div>', unsafe_allow_html=True)
    # Password field is always visible
    pwd = st.text_input("Password", type="password", key="pw_input", help="Password required to access the app")
    login = st.button("Login")
    st.markdown('</div>', unsafe_allow_html=True)
    return pwd, login

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd, login = show_login()
    if login:
        if pwd == st.secrets["app_password"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")
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

# --------- FULL KEYWORDS DICTIONARY HERE! ---------
KEYWORDS = {
    'Meat': [
        'Rump steak', 'Scotch fillet', 'Porterhouse steak', 'T-bone steak', 'Beef mince', 'Diced beef',
        'Beef schnitzel', 'Beef stir-fry strips', 'Beef sausages', 'Corned beef silverside', 'Beef roast',
        'Lamb chops', 'Lamb cutlets', 'Lamb leg roast', 'Lamb shanks', 'Diced lamb', 'Lamb mince',
        'Lamb sausages', 'Pork chops', 'Pork belly', 'Pork roast', 'Pork spare ribs', 'Diced pork',
        'Pork mince', 'Pork sausages', 'Pork schnitzel', 'Whole chicken', 'Chicken breast', 'Chicken thighs',
        'Chicken drumsticks', 'Chicken wings', 'Chicken tenderloins', 'Chicken mince', 'Chicken schnitzel',
        'Chicken marylands', 'Roast beef slices', 'Pastrami', 'Corned beef slices', 'Champagne ham',
        'Virginian ham', 'Honey leg ham', 'Triple smoked ham', 'Shaved chicken breast', 'Turkey breast slices',
        'Salami', 'Prosciutto', 'Sopressa', 'Mortadella', 'Pepperoni', 'Kassler', 'Bacon', 'Frankfurts',
        'Kransky', 'Chorizo', 'Cocktail sausages', 'Kabana', 'Devon', 'Liverwurst', 'Pâté',
        'Marinated chicken wings', 'Marinated chicken drumsticks', 'Meat kebabs', 'Rissoles',
        'Burger patties', 'Honey soy chicken portions', 'BBQ pork ribs', 'Pre-marinated pork belly',
        'Lemon herb chicken thighs'
    ],
    'Vegetables and Fruits': [
        'Apples', 'Bananas', 'Oranges', 'Mandarins', 'Pears', 'Peaches', 'Parsnip', 'Plums', 'Nectarines',
        'Grapes', 'Kiwifruit', 'Pineapple', 'Mangoes', 'Watermelon', 'Rockmelon', 'Cantaloupe',
        'Strawberries', 'Blueberries', 'Raspberries', 'Blackberries', 'Lemons', 'Limes', 'Avocados',
        'Tomatoes', 'Cherry tomatoes', 'Grape tomatoes', 'Cucumbers', 'Zucchini', 'Carrots', 'Celery',
        'Lettuce', 'Cos lettuce', 'Iceberg lettuce', 'Mixed salad leaves', 'Rocket', 'Spinach',
        'Silverbeet', 'Kale', 'Cabbage', 'Red cabbage', 'Savoy cabbage', 'Broccoli', 'Cauliflower',
        'Green beans', 'Snow peas', 'Sugar snap peas', 'Capsicum', 'Chillies', 'Eggplant', 'Pumpkin',
        'Sweet potato', 'Potatoes', 'Onions', 'Garlic', 'Shallots', 'Spring onions', 'Leeks', 'Mushrooms',
        'Corn', 'Green peas', 'Brussels sprouts', 'Beetroot', 'Radish', 'Fennel', 'Asparagus', 'Artichoke',
        'Chokos', 'Passionfruit', 'Papaya', 'Pomegranate', 'Coconut', 'Dates', 'Figs', 'Persimmon',
        'Lychee', 'Dragonfruit', 'Rambutan', 'Starfruit', 'Basil', 'Coriander', 'Parsley', 'Mint',
        'Dill', 'Chives', 'Thyme', 'Rosemary', 'Oregano', 'Sage', 'Tarragon', 'Marjoram', 'Vietnamese mint',
        'Lemongrass', 'Kaffir lime leaves', 'Bay leaves', 'Curry leaves'
    ],
    'Dairy': [
        'Milk', 'Lactose-free milk', 'A2 milk', 'Long-life milk', 'Flavoured milk', 'UHT milk',
        'Buttermilk', 'Cream', 'Sour cream', 'Crème fraîche', 'Yoghurt', 'Yoghurt tubs', 'Yoghurt pouches',
        'Skyr', 'Kefir', 'Butter', 'Cultured butter', 'Spreadable butter', 'Margarine', 'Ghee',
        'Cheddar cheese', 'Tasty cheese', 'Colby cheese', 'Mozzarella', 'Parmesan', 'Pecorino',
        'Grana Padano', 'Swiss cheese', 'Jarlsberg', 'Havarti', 'Provolone', 'Edam', 'Gouda', 'Brie',
        'Camembert', 'Blue cheese', 'Feta', 'Goat cheese', 'Ricotta', 'Cottage cheese', 'Cream cheese',
        'Mascarpone', 'Paneer', 'Haloumi', 'Processed cheese slices', 'Cheese sticks', 'Shredded cheese blends',
        'Grated cheese', 'Sliced cheese packs', 'Parmesan shavings', 'Dairy desserts', 'Custard',
        'Milk-based smoothies', 'Dairy-based dips', 'Evaporated milk', 'Condensed milk', 'Powdered milk'
    ],
    'Bakery': [
        'White bread', 'Wholemeal bread', 'Multigrain bread', 'Soy and linseed bread', 'Rye bread',
        'Sourdough', 'Pane di casa', 'Ciabatta', 'Turkish bread', 'Brioche loaf', 'Vienna loaf',
        'High-fibre loaf', 'Gluten-free bread', 'Low-carb bread', 'Fruit loaf', 'Raisin toast',
        'English muffins', 'Crumpets', 'Bagels', 'Wraps', 'Tortillas', 'Pita bread', 'Lebanese bread',
        'Flatbread', 'Pizza bases', 'Burger buns', 'Hot dog rolls', 'Long rolls', 'Dinner rolls',
        'Seeded rolls', 'Mini rolls', 'Cheese and bacon rolls', 'Scrolls', 'Croissants',
        'Pain au chocolat', 'Danish pastries', 'Cinnamon scrolls', 'Apple turnovers', 'Custard tarts',
        'Jam tarts', 'Vanilla slices', 'Eclairs', 'Lamingtons', 'Swiss rolls', 'Muffins', 'Cupcakes',
        'Madeleines', 'Banana bread', 'Carrot cake', 'Mud cake', 'Sponge cake', 'Chocolate cake',
        'Birthday cake', 'Slab cake', 'Fruit cake', 'Pound cake', 'Tea cake', 'Butter cake',
        'Brownies', 'Slice bars', 'Cookies', 'Biscuits', 'Shortbread', 'Anzac biscuits', 'Gingerbread',
        'Melting moments', 'Yo-yos', 'Scones', 'Pikelets', 'Waffles', 'Donuts', 'Mini donuts',
        'Jam-filled donuts', 'Iced donuts', 'Cinnamon donuts', 'Churros'
    ],
    'Pantry': [
        'Plain flour', 'Self-raising flour', 'Wholemeal flour', 'Bread flour', '00 flour', 'Rice flour',
        'Cornflour', 'Almond meal', 'Coconut flour', 'Polenta', 'Semolina', 'Rolled oats', 'Quick oats',
        'Steel-cut oats', 'Muesli', 'Granola', 'Cereal', 'Pasta', 'Gluten-free pasta', 'Rice', 'Pearl Couscous',
        'Quinoa', 'Bulgur', 'Barley', 'Lentils', 'Chickpeas', 'Black beans', 'Kidney beans', 'Cannellini beans',
        'Butter beans', 'Baked beans', 'Tinned tomatoes', 'Tomato paste', 'Tomato passata', 'Coconut milk',
        'Coconut cream', 'Evaporated milk', 'Condensed milk', 'UHT milk', 'Canned corn', 'Canned mushrooms',
        'Canned beetroot', 'Canned fruit', 'Tuna', 'Salmon', 'Sardines', 'Anchovies', 'Corned beef', 'SPAM',
        'Canned chicken', 'Soup cans', 'Stock', 'Soup mixes', 'Bouillon cubes', 'Gravy powder', 'Packet sauces',
        'Instant noodles', '2-minute noodles', 'Rice vermicelli', 'Egg noodles', 'Udon noodles', 'Soba noodles',
        'Nori sheets', 'Breadcrumbs', 'Crackers', 'Rice cakes', 'Corn cakes', 'Crispbread', 'Biscuits',
        'Chocolate biscuits', 'Wafers', 'Muesli bars', 'Nut bars', 'Cake mixes', 'Brownie mix', 'Pudding mix',
        'Custard powder', 'Gelatine', 'Baking powder', 'Baking soda', 'Yeast', 'Icing sugar', 'Caster sugar',
        'White sugar', 'Raw sugar', 'Brown sugar', 'Demerara sugar', 'Golden syrup', 'Maple syrup', 'Honey',
        'Molasses', 'Agave syrup', 'Peanut butter', 'Almond butter', 'Tahini', 'Hazelnut spread', 'Jam',
        'Marmalade', 'Vegemite', 'Promite', 'Marmite', 'Chutney', 'Relish', 'Mustard', 'Mayonnaise', 'Aioli',
        'Tomato sauce', 'BBQ sauce', 'Sweet chilli sauce', 'Soy sauce', 'Tamari', 'Teriyaki sauce', 'Hoisin sauce',
        'Oyster sauce', 'Fish sauce', 'Sriracha', 'Hot sauce', 'Curry paste', 'Sambal oelek', 'Satay sauce',
        'Vinegar', 'Lemon juice', 'Lime juice', 'Olive oil', 'Vegetable oil', 'Canola oil', 'Sunflower oil',
        'Sesame oil', 'Peanut oil', 'Coconut oil', 'Ghee', 'Cooking spray', 'Salt', 'Sea salt flakes',
        'Iodised salt', 'Himalayan salt', 'Black pepper', 'Peppercorns', 'Dried Bay leaves', 'Chilli flakes',
        'Ground paprika', 'Smoked paprika', 'Ground cumin', 'Ground coriander', 'Curry powder', 'Garam masala',
        'Five spice', 'Turmeric', 'Cinnamon', 'Nutmeg', 'Allspice', 'Ground ginger', 'Cloves', 'Vanilla extract',
        'Vanilla essence', 'Almond essence', 'Food colouring', 'Sprinkles', 'Decorations', 'Cocoa powder',
        'Drinking chocolate', 'Hot chocolate mix', 'Instant coffee', 'Ground coffee', 'Coffee beans', 'Coffee pods',
        'Black tea bags', 'Green tea', 'Herbal tea', 'Chai tea', 'Iced tea', 'Cordials', 'Soft drink bottles',
        'Tonic water', 'Mineral water', 'Sparkling water', 'Long-life juice', 'Cooking wine', 'Stock concentrate',
        'Meal bases', 'Taco kits', 'Wraps', 'Tortillas', 'Bread', 'Pizza bases', 'Flatbread', 'Pappadums',
        'Pickles', 'Gherkins', 'Olives', 'Sun-dried tomatoes', 'Roasted red peppers', 'Antipasto mix', 'Capers',
        'Artichoke hearts', 'Jerky', 'Popcorn', 'Potato chips', 'Corn chips', 'Pretzels', 'Nuts', 'Trail mix',
        'Dried fruit', 'Desiccated coconut', 'Shredded coconut', 'Seeds', 'Protein powder', 'Electrolyte powder',
        'Multivitamins', 'Health bars', 'Baby formula', 'Baby food jars', 'Pet food', 'Alfoil', 'Cling wrap',
        'Baking paper', 'Ziplock bags', 'Lunch bags', 'Paper towels', 'Tissues', 'Toilet paper', 'Dishwashing liquid',
        'Sponges', 'Cleaning sprays', 'Bin liners', 'Matches', 'Candles', 'Dried basil', 'Dried coriander',
        'Dried parsley', 'Dried mint', 'Dried dill', 'Dried chives', 'Dried Thyme', 'Dried rosemary',
        'Dried oregano', 'Dried sage', 'Dried tarragon', 'Dried marjoram', 'Dried herbes de Provence',
        'Dried Italian herb mix', 'Dried mixed herbs', 'Dried bay leaves', 'Dried lemongrass', 'Dried fennel leaves',
        'Dried fenugreek leaves'
    ],
    'Frozen': [
        'Peas', 'Corn', 'Green beans', 'Mixed vegetables', 'Broccoli', 'Cauliflower', 'Stir-fry vegetable mix', 'Spinach',
        'Edamame', 'Sweet potato', 'Avocado pieces', 'Onions', 'Diced capsicum', 'Blueberries', 'Raspberries',
        'Mixed berries', 'Mango', 'Banana', 'Cherries', 'Pineapple', 'Fruit salad', 'Acai puree', 'Smoothie packs',
        'Oven fries', 'Potato wedges', 'Hash browns', 'Potato gems', 'Mashed potato', 'Onion rings',
        'Crumbed mushrooms', 'Battered cauliflower', 'Vegetable patties', 'Falafel', 'Veggie nuggets',
        'Veggie burgers', 'Plant-based mince', 'Plant-based sausages', 'Plant-based chicken', 'Beef mince',
        'Chicken breast', 'Chicken nuggets', 'Chicken schnitzels', 'Chicken tenders', 'Chicken wings',
        'Chicken kievs', 'Whole chicken', 'Turkey breast', 'Duck', 'Pork roast', 'Beef burgers', 'Steak',
        'Meat pies', 'Sausage rolls', 'Pizza', 'Mini pizzas', 'Garlic bread', 'Lasagna', 'Pasta meals',
        'Cannelloni', 'Ravioli', 'Gnocchi', 'Pasta sheets', 'Dumplings', 'Gyoza', 'Spring rolls', 'Samosas',
        'Roti', 'Naan', 'Paratha', 'Puff pastry', 'Shortcrust pastry', 'Filo pastry', 'Pastry sheets', 'Quiches',
        'Savoury pastries', 'Fish fillets', 'Salmon portions', 'Prawns', 'Calamari', 'Seafood marinara mix',
        'Seafood baskets', 'Fish fingers', 'Crab sticks', 'Dim sims', 'Bao buns', 'Pancakes', 'Waffles',
        'Crumpets', 'Croissants', 'Brioche buns', 'Muffins', 'Yorkshire puddings', 'Scones', 'Cakes',
        'Cheesecakes', 'Tarts', 'Desserts', 'Ice cream', 'Gelato', 'Sorbet', 'Yoghurt', 'Icy poles',
        'Fruit bars', 'Ice cubes', 'Baby food', 'Dog food', 'Cat food'
    ]
}
# --------- END KEYWORDS ---------


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
    # Makes matching more robust for veggies and more
    return re.sub(r'[^a-z0-9]', '', word.lower().strip())

def categorize_ingredients(ingredients):
    categories = {sec: [] for sec in KEYWORDS}
    # Pre-make normalized keyword sets
    keyword_lookup = {}
    for sec, items in KEYWORDS.items():
        keyword_lookup[sec] = set()
        for k in items:
            nk = k.lower().strip()
            keyword_lookup[sec].add(nk)
            if k.endswith('s'):
                keyword_lookup[sec].add(nk[:-1])  # carrot/carrots

    for item in ingredients:
        clean = sanitize_text(item)
        base = re.sub(r'^[\d/]+\s*', '', clean)
        placed = False
        for sec in KEYWORDS:
            for k in keyword_lookup[sec]:
                if f" {k} " in f" {base.lower()} ":
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

def display_recipe(title, ingredients, method, index=0):
    st.subheader(title)
    st.markdown('**Ingredients**')
    for item in ingredients:
        st.markdown(f"{item}")
    st.markdown('**Method**')
    for i, step in enumerate(method, 1):
        clean_step = re.sub(r'^\s*\d+\s*[\.\)]?\s*', '', step)
        st.markdown(f"{i}. {clean_step}")
    # Individual PDF button
    cats = categorize_ingredients(ingredients)
    pdf_bytes = create_pdf(title, ingredients, method, shopping_categories=cats)
    fn = f"{title.replace(' ', '_').lower()}.pdf"
    st.download_button('Download PDF', data=pdf_bytes, file_name=fn, mime='application/pdf', key=f"pdfbtn{index}")

def display_shopping(categories):
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
        for idx, txt in enumerate(recipes):
            title, ingredients, method = parse_recipe(txt)
            if not ingredients or not method:
                st.warning(f"Skipping '{title}': missing sections.")
                continue
            display_recipe(title, ingredients, method, index=idx)
            all_ingredients.extend(ingredients)
        combined_shopping = categorize_ingredients(all_ingredients)
        st.header("Shopping List")
        display_shopping(combined_shopping)

if __name__ == '__main__':
    main()
