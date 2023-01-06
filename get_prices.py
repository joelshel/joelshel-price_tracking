#!/usr/bin/env python3


def get_price_nike(soup):
    """Gets the price for the Nike online store.

    Args:
        soup (bs4.BeautifulSoup): HTML code where to find the price

    Returns:
        str: price inside the soup
    """
    
    # <div class="product-price css-11s12ax is--current-price css-tpaepq" data-test="product-price">€119.99</div>
    
    # Just to say that the old price exists
    
    try:
        old_price = soup.find("div", class_="is--striked-out")
        old_price.find('span').extract()
        old_price = old_price.string
    except AttributeError:
        old_price = None
    
    new_price = soup.find("div", class_="is--current-price").string
    new_price = new_price.replace("€", "").strip()
    return new_price


def get_price_adidas(soup):
    """Gets the price for the Adidas online store.

    Args:
        soup (bs4.BeautifulSoup): HTML code where to find the price

    Returns:
        str: price inside the soup
    """

    # Without sales
    # <div class="gl-price-item notranslate">€ 110</div>

    # With sales
    # <div class="gl-price-item gl-price-item--crossed notranslate">€ 130</div>
    # <div class="gl-price-item gl-price-item--sale notranslate">€ 97,50</div>
    
    old_price = soup.find("div", class_="gl-price-item--crossed")
    if not old_price:
        old_price = None
    else:
        old_price = old_price.string.replace("€", "").strip()
    
    new_price = soup.find("div", class_="gl-price-item--sale")
    if not new_price:
        new_price = soup.find("div", class_="gl-price-item")
    new_price = new_price.string.replace("€", "").strip()
    return new_price
