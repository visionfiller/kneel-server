from .metal_requests import get_single_metal
from .size_requests import get_single_size
from .style_requests import get_single_style

ORDERS = [
    {
        "id": 1,
        "metalId": 3,
        "sizeId": 2,
        "styleId": 3,
        
    }
]

def get_all_orders():
    return ORDERS
# Function with a single parameter
def get_single_order(id):
    # Variable to hold the found metal, if it exists
    requested_order = None

    # Iterate the METALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for order in ORDERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if order["id"] == id:
            requested_order = order
            matching_size = get_single_size(requested_order["sizeId"])
            requested_order["size"] = matching_size
            matching_style = get_single_style(requested_order["styleId"])
            requested_order["style"] = matching_style
            matching_metal = get_single_metal(requested_order["metalId"])
            requested_order["metal"] = matching_metal
            del requested_order["metalId"]
            del requested_order["sizeId"]
            del requested_order["styleId"]

    return requested_order

def create_order(order):
    max_id = ORDERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    order["id"] = new_id

    # Add the animal dictionary to the list
    ORDERS.append(order)

    # Return the dictionary with `id` property added
    return order
def delete_order(id):
    # Initial -1 value for animal index, in case one isn't found
    order_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the animal. Store the current index.
            order_index = index

    # If the animal was found, use pop(int) to remove it from list
    if order_index >= 0:
        ORDERS.pop(order_index)
def update_order(id, new_order):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the animal. Update the value.
            ORDERS[index] = new_order
            break