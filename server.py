from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

customers = []
customer_id = 1

class Customer(BaseModel):
    name: str
    email: str

class CustomerOut(Customer):
    id: int

@app.get("/customers", response_model=List[CustomerOut])
def get_customers():
    return customers

@app.post("/customers", response_model=CustomerOut, status_code=201)
def create_customer(customer: Customer):
    global customer_id
    new_customer = {
        "id": customer_id,
        "name": customer.name,
        "email": customer.email
    }
    
    customers.append(new_customer)
    customer_id += 1
    return new_customer

@app.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, updated_customer: Customer):
    for customer in customers:
        if customer["id"] == customer_id:
            customer["name"] = updated_customer.name
            customer["email"] = updated_customer.email
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: int):
    for index, customer in enumerate(customers):
        if customer["id"] == customer_id:
            customers.pop(index)
            return
    raise HTTPException(status_code=404, detail="Customer not found")

