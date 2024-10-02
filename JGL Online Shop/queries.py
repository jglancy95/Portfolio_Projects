"""In charge of querying the database"""

import online_shop as sh
# Create charge report session for queries
shop_session = sh.SHOP_SESSION

def find_product_list():
    """Returns a list of available product/service list"""
    
    products_and_services = shop_session.query(
        sh.ProductsAndServices
    ).all()
    
    print(products_and_services)
    
    return products_and_services

def find_product_by_id(product_id):
    """Queries a database for a product using its ID"""
    
    product_or_service = shop_session.query(
        sh.ProductsAndServices
    ).filter_by(service_product_id=product_id).one_or_none()
    
    return product_or_service


def find_leather_goods():
    """Returns a list of leather goods"""
    
    leather_goods = shop_session.query(
        sh.LeatherGoods
    ).all()
    
    return leather_goods

def look_up_leather_colors():
    """Returns a list of leather colors"""
    
    leather_colors = shop_session.query(
        sh.LeatherColors
    ).all()
    
    return leather_colors

def find_sizes():
    """Returns a list of sizes of leather products"""
    
    sizes = shop_session.query(
        sh.Sizes
    ).all()
    
    return sizes

def look_up_metal_colors():
    """Returns a list of metal colors"""
    
    metal_colors = shop_session.query(
        sh.MetalColors
    ).all()
    
    return metal_colors

def writing(product_ids):
    """Returns a list of written products"""
    
    written_products = shop_session.query(
        sh.WritingOptions.option_id,
        sh.WritingOptions.product_type
    ).filter(
        sh.WritingOptions.option_id.in_(product_ids)
    ).all()
    
    return written_products

def software():
    """Returns a list of software goods"""
    
    software_goods = shop_session.query(
        sh.SoftwareOptions
    ).all()
    
    return software_goods

def find_user(name):
    """Looks up the user by name"""
    
    user_search = shop_session.query(
        sh.Users
    ).filter_by(username=name).first()
    
    return user_search

def find_email(form_email):
    """Looks up the user by email"""
    
    user_search = shop_session.query(
        sh.Users
    ).filter_by(email=form_email).first()
    
    return user_search

def find_user_id(username):
    """Looks up ID by username"""
    
    user_search = shop_session.query(
        sh.Users
    ).filter_by(username=username).first()
    
    return user_search

def find_product_price(product_id):
    """Returns the price of an item"""
    
    price_search = shop_session.query(
        sh.ProductsAndServices
    ).filter_by(service_product_id=product_id).first()
    
    if price_search:
        item_price = price_search.rate
        
        return item_price
    
    return price_search

def shopping_session_search(session_id):
    """Finds any shopping session"""
    
    shopping_session = shop_session.query(
        sh.ShoppingSessions
    ).filter_by(session_id=session_id).first()
    
    return shopping_session

def find_cart(shopping_session_id):
    """Returns the cart items associated with
    a shopping session"""
    
    cart_items = shop_session.query(
        sh.CartItems
    ).filter_by(session_id=shopping_session_id).all()
    
    return cart_items

def cart_price(shopping_session_id):
    """Grabs the total of the cart"""
    
    session_totals = shop_session.query(
        sh.ShoppingSessions
    ).filter_by(session_id=shopping_session_id).one_or_none()

    return session_totals

def find_option_text(product_id, option_id):
    """Find text for an option based on ID"""
    
    option = None
    
    if product_id == 1:
        # Leather items
        
        try:
            option_results = shop_session.query(
                sh.LeatherGoods
            ).filter_by(leather_item_id=option_id).first()

            if option_results is None:
                print("No matching leather good found")
            
            option = option_results.item
            print(f"Option: {option}")
        
        except Exception as e:
            print(f"Exception: {e}")
        
    elif product_id == 2 or product_id == 3:
        # Written items      
        
        try:
            option_results = shop_session.query(
                sh.WritingOptions
            ).filter_by(option_id=option_id).first()
        
            if option_results is None:
                print("No matching writing option found")

                
            option = option_results.product_type
            
            print(f"Option: {option}")

        except Exception as e:
            print(f"Exception: {e}")
        
    elif product_id == 4:
        # Software items
        
        try:
            option_results = shop_session.query(
                sh.SoftwareOptions
            ).filter_by(option_id=option_id).first()

            if option_results is None:
                print("No matching software option found")
                

            option = option_results.product_type
            
            print(f"Option: {option}")
        
        except Exception as e:
            print(f"Exception: {e}")
            
    return option
    
def find_leather_color(color_id):
    """Query leather color by ID"""

    color = None
    
    try:
        color_results = shop_session.query(
            sh.LeatherColors
        ).filter_by(leather_color_id=color_id).first()

        if color_results is None:
            print("No matching color found")
            
        color = color_results.color_string
        
        print(f"Option: {color}")
    
    except Exception as e:
        print(f"Exception: {e}")
        
    return color

def find_metal_color(color_id):
    """Query metal color by ID"""

    color = None
    
    try:
        color_results = shop_session.query(
            sh.MetalColors
        ).filter_by(metal_color_id=color_id).first()

        if color_results is None:
            print("No matching metal color found")
            
        color = color_results.metal_type
        
        print(f"Option: {color}")
    
    except Exception as e:
        print(f"Exception: {e}")
        
    return color

def get_size(size_id):
    """Query size table"""

    size = None
    
    try:
        size_results = shop_session.query(
            sh.Sizes
        ).filter_by(size_id=size_id).first()

        if size_results is None:
            print("No matching sizes found")
            
        size_inches = size_results.size_inches
        size_centi = size_results.size_centimeters
    
        size = f"{size_inches} inches ({size_centi} centimeters)"
        print(f"Option: {size}")
    
    except Exception as e:
        print(f"Exception: {e}")
        
    return size
