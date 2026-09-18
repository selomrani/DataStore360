import pandas as pd
import numpy as np

#get raw data via csv



# we start cleaning data here based on the issues found during the exploration

#Dropping the 34 duplicated row we found
def drop_df_duplicates(data):
    data = data.drop_duplicates()
    return data

#filling the missing postal codes , i will put 0000 as a filler
def fix_missing_postal_code(data):
    data["Postal Code"] = (
        data["Postal Code"].fillna(0).astype(int).astype(str).str.zfill(5)
    )
    return data
# converting Dates from strings to calcaulatable elements

def make_dates_calculable(data):
 data["Order Date"] = pd.to_datetime(data["Order Date"], format="mixed")
 data["Ship Date"] = pd.to_datetime(data["Ship Date"], format="mixed")
 return data

# Normalizing all Categories into Capital letters

def normalize_categories_naming(data):
    data['Category'] = data['Category'].str.title()
    return data


# fill missing ship mode values with the most frequent value
def fix_missing_ship_modes(data):
 data['Ship Mode'] = data['Ship Mode'].fillna(data['Ship Mode'].mode()[0])
 return data

# fixing missing Ship dates
def fix_ship_dates(data: pd.DataFrame) -> pd.DataFrame:
    data["Order Date"] = pd.to_datetime(data["Order Date"], format="mixed")
    data["Ship Date"] = pd.to_datetime(data["Ship Date"], format="mixed")

    transit_days = (data["Ship Date"] - data["Order Date"]).dt.days
    avg_transit_days = transit_days.dropna().mean()

    data["Ship Date"] = data["Ship Date"].fillna(
        data["Order Date"] + pd.to_timedelta(round(avg_transit_days), unit="D")
    )
    return data
def fix_quantities(data: pd.DataFrame) -> pd.DataFrame:
    denom_unit = (data['Quantity'] * (1 - data['Discount'])).replace(0, np.nan)
    data['Unit Price'] = data['Sales'] / denom_unit
    price_map = data['Unit Price'].groupby(data['Product ID']).median()
    denom_qty = (data['Product ID'].map(price_map) * (1 - data['Discount'])).replace(0, np.nan)
    calc_qty = data['Sales'] / denom_qty
    data['Quantity'] = data['Quantity'].fillna(calc_qty).round()
    return data

def fix_customer_names(data):
    customer_id_to_customer_name = (
    data.dropna(subset=['Customer Name'])
    .drop_duplicates(subset=['Customer ID'])
    .set_index('Customer ID')['Customer Name']
    .to_dict())
    data['Customer Name'] = data['Customer Name'].fillna(data['Customer ID'].map(customer_id_to_customer_name))
    return data


# fixing missing sales numbers
def fix_sales_numbers(data: pd.DataFrame) -> pd.DataFrame:
    calc_sales = data['Unit Price'] * data['Quantity'] * (1 - data['Discount'].fillna(0))
    data['Sales'] = data['Sales'].fillna(calc_sales).round(2)
    return data

def fix_seguement_naming(data):
    data['Segment'] = data['Segment'].replace({'consumerr': 'Consumer'})
    return data

def pseudonomise_customer_names(data):
    import hashlib
    data['Customer Name'] = data['Customer Name'].astype(str).apply(
        lambda name: hashlib.sha256(name.encode()).hexdigest()
    )
    return data

def delete_crazy_discounts(data:pd.DataFrame):
    return data[data['Discount'] <= 1.0]


