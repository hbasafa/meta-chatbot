
import pandas as pd

product_path = "/home/albert/Documents/DS1/knowledgebase/product-sample.xlsx"
product_features_path = "/home/albert/Documents/DS1/knowledgebase/product-features-sample.xlsx"
product_details_path = "/home/albert/Documents/DS1/knowledgebase/product-details-sample.xlsx"


def get_products():
    data = pd.read_excel(product_path)
    return data


def get_products_features():
    data = pd.read_excel(product_features_path)
    return data


def get_product_details():
    data = pd.read_excel(product_details_path)
    return data


