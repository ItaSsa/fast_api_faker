from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse  # Importing HTMLResponse
from fastapi.templating import Jinja2Templates  # Render templates HTML
from starlette.requests import Request  # Importing Request
from faker import Faker
import pandas as pd
import random

# Instancing 
app = FastAPI(debug=True)
fake = Faker()


# Reading products list to be use to generating the purchase(s)
file_name = 'data/products.csv'
df = pd.read_csv(file_name)
df['index'] = range(1, len(df) +1)
df.set_index('index', inplace=True)

online_store = 11

# Mounts the **static/** directory at the **/static** URL,
#  allowing the browser to access 
# files such as images, CSS, and JavaScript.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configures FastAPI to render HTML files stored in 
# the **templates/** folder using the Jinja2 library.
templates = Jinja2Templates(directory="templates")

## Store homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Generating a purchase record from products dataframe
@app.get("/gen_purchase")
async def gen_purchase():
    index = random.randint(1, len(df)-1)
    tuple = df.iloc[index]
    return {
            "client": fake.name(),
            "creditcard": fake.credit_card_provider(),
            "product": tuple["Product Name"],
            "ean": int(tuple["EAN"]),
            "price":  round(float(tuple["Price"])*1.2,2),
            "clientPosition": fake.location_on_land(),
            "store": online_store,
            "dateTime": fake.iso8601()
        }

# Generating n purchasing records
@app.get("/gen_purchase/{record_number}")
async def gen_purchase(record_number: int):
    
    if record_number < 1:
        return {"error" : "The record's number should be greater than 1"}
 
    responses = []
    for _ in range(record_number):
        try:
            index = random.randint(1, len(df)-1)
            tuple = df.iloc[index]
            purchase = {
                    "client": fake.name(),
                    "creditcard": fake.credit_card_provider(),
                    "product": tuple["Product Name"],
                    "ean": int(tuple["EAN"]),
                    "price":  round(float(tuple["Price"])*1.2,2),
                    "clientPosition": fake.location_on_land(),
                    "store": online_store,
                    "dateTime": fake.iso8601()
                    }
            responses.append(purchase)
        except IndexError as e:
            print(f"Index error: {e}")
        except ValueError as e:
            print(f"Unexpected error: {e}")
            purchase = {
                    "client": fake.name(),
                    "creditcard": fake.credit_card_provider(),
                    "product": "error",
                    "ean": 0,
                    "price":  0.0,
                    "clientPosition": fake.location_on_land(),
                    "store": online_store,
                    "dateTime": fake.iso8601()
                    }
            responses.append(purchase)
        except Exception as e:
            print(f"Unexpected error: {e}")
    return responses