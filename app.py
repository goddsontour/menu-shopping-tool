import streamlit as st
import re
from streamlit.runtime.scriptrunner import RerunException  # for force rerun

# Monkey-patch st.experimental_rerun if missing
if not hasattr(st, 'experimental_rerun'):
    def experimental_rerun():
        # Force a script rerun by raising RerunException with dummy rerun_data
        raise RerunException({})
    st.experimental_rerun = experimental_rerun
from fpdf import FPDF

# Configure page before any Streamlit calls
st.set_page_config(page_title="Kind Kitchen Login")

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Render login screen
def show_login():
    st.markdown("""
    <style>
      body, .stApp {
        background-color: #f5f5f5;
        margin: 0;
        padding: 0;
      }
      .login-outer {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        margin-top: 2vh;
      }
      .welcome-circle {
        width: 40vmin;
        height: 40vmin;
        max-width: 80vh;
        max-height: 80vh;
        border-radius: 50%;
        background: white;
        box-shadow: 0 6px 48px #bbb4;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2vh auto 1vh auto;
      }
      .welcome-text {
        color: #009000;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        letter-spacing: 0.5px;
        font-family: 'DejaVu Sans', Arial, sans-serif;
      }
      .login-box {
        width: 340px;
        margin: 0 auto;
      }
      .login-box input[type="text"] {
        width: 100% !important;
      }
      .login-box div[data-testid="stTextInput"] > div > input[type="password"] {
        width: 50% !important;
        min-width: 0 !important;
        margin: 0 auto !important;
        display: block !important;
      }
    </style>
    """, unsafe_allow_html=True)

    # Ensure login session is tracked
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login only if not logged in
if not st.session_state.logged_in:
    st.markdown('<div class="login-outer">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-circle"><div class="welcome-text">Kind Kitchen</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    # Input and login button
    pwd_input = st.text_input("Password", type="password", label_visibility="visible")
    login = st.button("Login")

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Authenticate
    if login:
        if pwd_input == "kindkitchen2025":
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Incorrect password. Please try again.")

    # 🔒 Prevent running the rest of the app until logged in
    st.stop()

# If not authenticated, show login and stop
if not st.session_state.authenticated:
    show_login()
    st.stop()

# Authenticated content
st.success("You're logged in! Welcome to Kind Kitchen.")

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
        'Iodised salt', 'Himalayan salt', 'Black pepper', 'Peppercorns', 'Dried bay leaves', 'Chilli flakes',
        'Ground paprika', 'Smoked paprika', 'Ground cumin', 'Ground coriander', 'Curry powder', 'Garam masala',
        'Five spice', 'Turmeric', 'Cinnamon', 'Nutmeg', 'Allspice', 'Ground ginger', 'Cloves', 'Vanilla extract',
        'Vanilla essence', 'Almond essence', 'Food colouring', 'Sprinkles', 'Decorations', 'Cocoa powder',
        'Drinking chocolate', 'Hot chocolate mix', 'Instant coffee', 'Ground coffee', 'Coffee beans', 'Coffee pods',
        'Black tea bags', 'Green tea', 'Herbal tea', 'Chai tea', 'Iced tea', 'Cordials', 'Soft drink bottles',
        'Tonic water', 'Mineral water', 'Sparkling water', 'Long-life juice', 'Cooking wine', 'Stock concentrates',
        'Meal bases', 'Taco kits', 'Wraps', 'Tortillas', 'Bread sticks', 'Pizza bases', 'Flatbread', 'Pappadums',
        'Pickles', 'Gherkins', 'Olives', 'Sun-dried tomatoes', 'Roasted red peppers', 'Antipasto mix', 'Capers',
        'Artichoke hearts', 'Jerky', 'Popcorn', 'Potato chips', 'Corn chips', 'Pretzels', 'Nuts', 'Trail mix',
        'Dried fruit', 'Desiccated coconut', 'Shredded coconut', 'Seeds', 'Protein powder', 'Electrolyte powder',
        'Multivitamins', 'Health bars', 'Baby formula', 'Baby food jars', 'Pet food', 'Alfoil', 'Cling wrap',
        'Baking paper', 'Ziplock bags', 'Lunch bags', 'Paper towels', 'Tissues', 'Toilet paper', 'Dishwashing liquid',
        'Sponges', 'Cleaning sprays', 'Bin liners', 'Matches', 'Candles'
    ],
    'Frozen': [
        'Peas', 'Corn', 'Green beans', 'Mixed vegetables', 'Broccoli', 'Cauliflower', 'Stir-fry vegetable mix', 'Spinach',
        'Edamame', 'Sweet potato', 'Avocado pieces', 'Onions', 'Diced capsicum', 'Blueberries', 'Raspberries',
        'Mixed berries', 'Mango', 'Banana', 'Cherries', 'Pineapple', 'Fruit salad', 'Acai puree', 'Smoothie packs',
        'Oven fries', 'Potato wedges', 'Hash browns', 'Potato gems', 'Mash', 'Onion rings',
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
    return str(text).replace('\x00', '') if text is not None else ''

def categorize_ingredients(ingredients):
    categorized = {key: [] for key in KEYWORDS.keys()}
    categorized['Other'] = []
    for ing in ingredients:
        found = False
        for category, items in KEYWORDS.items():
            if any(normalize(item) in normalize(ing) for item in items):
                categorized[category].append(ing)
                found = True
                break
        if not found:
            categorized['Other'].append(ing)
    return categorized

def normalize(word):
    return ''.join(e.lower() for e in word if e.isalnum())

def parse_recipe(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0] if lines else 'Untitled'
    i1 = next((i for i, l in enumerate(lines) if l.lower().startswith('ingredients')), None)
    i2 = next((i for i, l in enumerate(lines) if l.lower().startswith('method')), None)
    if i1 is None or i2 is None or i2 <= i1:
        return title, [], []
    ingredients = lines[i1+1:i2]
    method = lines[i2+1:]
    return title, ingredients, method

def create_pdf(title, ingredients, method, shopping_categories=None, image_file=None):
    from fpdf import FPDF
    from PIL import Image
    import tempfile
    import os
    import re

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',12)
    pdf.cell(0,10,sanitize_text(title),ln=True)
    pdf.ln(2)
    pdf.set_font('Arial','B',10); pdf.cell(0,8,'Ingredients',ln=True)
    pdf.set_font('Arial','',10)
    for it in ingredients: pdf.cell(0,6,it,ln=True)
    pdf.ln(4)
    pdf.set_font('Arial','B',10); pdf.cell(0,8,'Method',ln=True)
    pdf.set_font('Arial','',10)
    for i,step in enumerate(method,1):
        stp = re.sub(r'^\d+\.\s*','',step)
        pdf.write(6,f"{i}. {stp}")
        pdf.ln(8)
    urls = re.findall(r'https?://[^\s]+', ' '.join(method))
    if urls:
        pdf.ln(4)
        pdf.set_font('Arial','B',10); pdf.cell(0,8,'Links',ln=True)
        pdf.set_font('Arial','',10)
        for u in set(urls): pdf.write(6,u,link=u); pdf.ln(6)

    pdf.add_page()
    if shopping_categories:
        pdf.set_font('Arial','B',10); pdf.cell(0,8,'Shopping List',ln=True)
        pdf.set_font('Arial','',10)
        for sec, items in shopping_categories.items():
            pdf.set_font('Arial','B',10); pdf.cell(0,6,sec,ln=True)
            pdf.set_font('Arial','',10)
            if items:
                for it in items: pdf.cell(0,6,f'- {it}',ln=True)
            else: pdf.cell(0,6,'- none',ln=True)
            pdf.ln(2)

        if image_file:
            try:
                img = Image.open(image_file)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    img.convert("RGB").save(tmp.name)
                    pdf.ln(10)
                    pdf.image(tmp.name, w=(pdf.w - 20) / 3.125)
                    os.remove(tmp.name)
            except Exception as e:
                print("Failed to insert image:", e)

    return pdf.output(dest='S').encode('latin1')

def display_recipe(title, ingredients, method, index=0, image_file=None):
    st.subheader(title)
    st.markdown('**Ingredients**')
    for it in ingredients: st.markdown(it)
    st.markdown('**Method**')
    for i,step in enumerate(method,1): st.markdown(f"{i}. {re.sub(r'^\s*\d+[\.)]?\s*','',step)}")
    cats = categorize_ingredients(ingredients)
    pdf_data = create_pdf(title, ingredients, method, cats, image_file=image_file)
    fn = f"{title.replace(' ','_').lower()}.pdf"
    st.download_button('Download PDF', data=pdf_data, file_name=fn, mime='application/pdf', key=f"pdf{index}")

def display_shopping(categories):
    if not isinstance(categories, dict):
        st.warning("No shopping list could be generated.")
        return
    st.header('Shopping List')
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

    files = st.file_uploader('Or upload up to 4 .txt files', type='txt', accept_multiple_files=True)
    if files:
        for f in files[:4]:
            recipes.append(f.read().decode())

    st.markdown("Optionally add a photo to go with your recipe — it will appear on the PDF below the shopping list.")
    image_file = st.file_uploader("Upload an image for the recipe", type=["png", "jpg", "jpeg"])


    if st.button('Generate Recipe'):
        if not recipes:
            st.info('Enter at least one recipe or upload files.')
            return

        all_ing = []
        for idx, txt in enumerate(recipes):
            if not isinstance(txt, str) or not txt.strip():
                st.warning(f"Skipping empty or invalid recipe input at index {idx+1}")
                continue
            try:
                title, ing, meth = parse_recipe(txt)
                if not ing or not meth:
                    st.warning(f"Skipping recipe: missing Ingredients or Method section.")
                    continue
            except Exception as e:
                st.warning(f"Skipping recipe due to parsing error: {e}")
                continue

            display_recipe(title, ing, meth, index=idx, image_file=image_file)
            all_ing.extend(ing)

        display_shopping(categorize_ingredients(all_ing))

if __name__ == '__main__':
    main()

