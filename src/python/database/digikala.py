import json
import requests
import pandas as pd
from requests import Request, Session

from src.python.param import http, digikala as dk, product as p, product_feature as pf, product_detail as prd


product_url = "https://sirius.digikala.com/v1/product/{}/"
category_url = "https://sirius.digikala.com/v1/category/{}/"
pricechart_url = "https://www.digikala.com/ajax/product/price-chart/{}"
product_page_url = "https://www.digikala.com/product/dkp-{}"

base_dir = "/home/albert/Documents/DS1/knowledgebase/digikala/"

path = "/home/albert/Documents/DS1/knowledgebase/digikala/digikala-category-attributes.xlsx"


def get_response(api_url):
    response = requests.get(api_url, headers=headers)

    if response.status_code >= 500:
        print('[!] [{0}] Server Error'.format(response.status_code))
        return None
    elif response.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
        return None
    elif response.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(response.status_code))
        return None
    elif response.status_code == 400:
        print('[!] [{0}] Bad Request'.format(response.status_code))
        return None
    elif response.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
        return None
    elif response.status_code == 200:
        ssh_keys = json.loads(response.content.decode('utf-8'))
        return ssh_keys
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    return None


def get_headers():
    my_headers = {
        http.HEADERS_USER_AGENT: http.MODIFIED_USER_AGENT,
        http.HEADERS_CACHE_CONTROL: http.NO_CACHE,
        http.HEADERS_ACCEPT_LANGUAGE: http.DEFAULT_ACCEPT_LANGUAGE,
        http.HEADERS_INSECURE_REQUEST: http.DEFAULT_INSECURE_REQUEST,
        http.HEADERS_ACCEPT: http.DEFAULT_ACCEPT,
        http.HEADERS_PRAGMA: http.NO_CACHE,
    }
    return my_headers


def write_to_file(df, filename):
    fn = base_dir + filename + ".xlsx"
    df.to_excel(fn, index=False)


def get_category_ids():
    categories = [9233,8916,8926,8939,8948,9241,9846]
    return categories


def get_product_ids():
    products = []
    return products


def get_product_sample_ids():
    samples = [
        790118, # sobhane
        856812, # labaniat
    ]
    return samples


def select_products_in_category(response_json):
    data = select_data(response_json)
    products = data[dk.PRODUCTS]
    return products


def select_product(product_response):
    data = select_data(product_response)
    products = data[dk.PRODUCT]
    return products


def request_category(category_id):
    url = category_url.format(category_id)
    response = get_response(url)
    return response


def request_product(product_id):
    url = product_url.format(product_id)
    response = get_response(url)
    return response


def get_products_in_category(cat_id):
    category_response = request_category(cat_id)
    products = select_products_in_category(category_response)
    return products


def get_product_content(product_id):
    product_response = request_product(product_id)
    product_content = select_product(product_response)
    return product_content


def get_products_by_ids(product_ids):
    products = []
    for pid in product_ids:
        product = get_product_content(pid)
        products.append(product)
    return products


def get_products_by_categories(category_ids):
    products = []
    for cat_id in category_ids:
        candidate_products = get_products_in_category(cat_id)
        products.extend(candidate_products)
    return products


def select_features(products_content):
    contents = []
    for product in products_content:
        content = {
            p.ID: product[dk.ID],
            p.CAT_ID: product[dk.CATEGORY_ID],
            p.TITLE_EN: product[dk.TITLE_EN],
            p.TITLE_FA: product[dk.TITLE_FA],
            p.RATE_NUMBER: product[dk.RATING][dk.RATE],
            p.RATE_COUNT: product[dk.RATING][dk.COUNT],
            p.STATUS: product[dk.STATUS],
            p.IMAGES: product[dk.IMAGES][dk.MAIN], # TODO: separate database for image search
            p.IS_FAST_SHOPPING: product[dk.PROPERTIES][dk.IS_FAST_SHOPPING],
            p.IS_FAKE: product[dk.PROPERTIES][dk.IS_FAKE],
            p.IS_READY_TO_SHIP: product[dk.PROPERTIES][dk.IS_READY_TO_SHIP],
            p.HAS_GIFT: product[dk.PROPERTIES][dk.HAS_GIFT],
            p.PRICE: product[dk.PRICE][dk.SELLING_PRICE],
            p.RRP_PRICE: product[dk.PRICE][dk.RRP_PRICE],
            p.ORDER_LIMIT: product[dk.PRICE][dk.ORDER_LIMIT],
            p.IS_INCREDIBLE: product[dk.PRICE][dk.IS_INCREDIBLE],
            p.IS_PROMOTION: product[dk.PRICE][dk.IS_PROMOTION],
        }
        contents.append(content)
    return contents


def get_products_info():
    #TODO: by ids (get product ids from categories then request each product)
    #TODO: add products by ids and merge them
    products_info = get_products_by_categories(set(get_category_ids()))
    filtered_feauter_products = select_features(products_info)
    return filtered_feauter_products


def get_products():
    products = get_products_info()
    return products


def to_dataframe(data):
    df = pd.DataFrame(data)
    return df


def select_breadcrumb(json_data):
    bc = json_data[dk.BREADCRUMB]
    return bc


def supercategories():
    sample_ids = get_product_sample_ids()
    samples = get_products_by_ids(sample_ids)
    super_cats = []
    for product in samples:
        breadcrumb = select_breadcrumb(product)
        super_cats.append(breadcrumb[1])
    super_cats = pd.DataFrame(super_cats)
    return super_cats


def select_data(json_response):
    data = json_response[dk.DATA]
    return data


def get_product_data(product_id):
    product_response = request_product(product_id)
    data = select_data(product_response)
    return data


def get_products_data(product_ids):
    data = []
    for pid in product_ids:
        data.append(get_product_data(pid))
    return data


def categories_supercategoreis():
    products_ids = products_df[p.ID]
    product_samples = get_products_by_ids(products_ids)
    products = product_samples
    cat_supercats = []
    for product in products:
        breadcrumb = select_breadcrumb(product)
        cat_supercats.append({p.CAT_ID: breadcrumb[0][dk.ID], p.SUPER_CAT_ID: breadcrumb[1][dk.ID]})
    cat_supercats = pd.DataFrame(cat_supercats).drop_duplicates()
    return cat_supercats


#TODO: finally rename to get_data()
if __name__ == '__main__':
    headers = get_headers()

    # test
    # url = product_url.format(product_id)
    # url = "http://httpbin.org/anything"
    # response = get_response(url)
    # status = response[dk.STATUS]

    # product file
    dk_products = get_products()
    products_df = to_dataframe(dk_products)
    write_to_file(products_df, "digikala-products")

    # cat - supercat
    cat_sups = categories_supercategoreis()
    write_to_file(cat_sups, "digikala-categories-supercategories")

    # supercats
    super_cats = supercategories()
    write_to_file(super_cats, "digikala-super-categories")

    # product features
    # TODO*: category-features

    # product details


