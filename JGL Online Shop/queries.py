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
    ).filter_by(service_product_id=product_id).first()
    
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