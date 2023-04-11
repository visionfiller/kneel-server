import sqlite3
import json
from models import Metal, Size, Style, Order

ORDERS = [
    {
        "id": 1,
        "metalId": 3,
        "sizeId": 2,
        "styleId": 3,
        
    }
]

def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.metal_id,
            a.size_id,
            a.style_id,
            m.metal,
            m.price,
            s.carets,
            s.price,
            t.style,
            t.price
            
        FROM orders a
        JOIN metals m ON m.id = a.metal_id
        JOIN sizes s ON s.id = a.size_id
        JOIN styles t ON t.id = a.style_id
        """)

        # Initialize an empty list to hold all animal representations
        orders = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
           

    # Create an animal instance from the current row
            order = Order(row['id'], 
                    row['metal_id'], row['size_id'], row['style_id'])

    # Create a Location instance from the current row
            metal = Metal(row['id'], row['metal'], row['price'])
            size = Size(row['id'], row['carets'], row['price'])
            style = Style(row['id'], row['style'], row['price'])
    # Add the dictionary representation of the location to the animal
            order.metal = metal.__dict__
            order.size = size.__dict__
            order.style = style.__dict__

    # Add the dictionary representation of the animal to the list
            orders.append(order.__dict__)
        return orders
# Function with a single parameter
def get_single_order(id):
   with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.metal_id,
            a.size_id,
            a.style_id
            
        FROM orders a
        WHERE a.id = ?
        """, (id, ))
        

        # Initialize an empty list to hold all animal representations
        

        # Convert rows of data into a Python list
        data = db_cursor.fetchone()

       
        order = Order(data['id'], 
                    data['metal_id'], data['size_id'], data['style_id'])

    
          
        return order.__dict__

def create_order(new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO ORDERS
            ( metal_id, size_id, style_id )
        VALUES
            ( ?, ?, ?);
        """, (new_order['metal_id'], new_order['size_id'],
              new_order['style_id'] ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_order['id'] = id


    return new_order
def delete_order(id):
       with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Orders
        WHERE id = ?
        """, (id, ))
def update_order(id, new_order):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the animal. Update the value.
            ORDERS[index] = new_order
            break