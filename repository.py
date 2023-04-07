import copy
DATABASE = {
    "metals": [
        {"id": 1,"metal": "Sterling Silver", "price": 12.42},
        {"id": 2, "metal": "14K Gold","price": 736.4},
        {"id": 3, "metal": "24K Gold","price": 1258.9},
        {"id": 4, "metal": "Platinum","price": 795.45 },
        {"id": 5,"metal": "Palladium","price": 1241 }
    ],
    "sizes": [
        {"id": 1, "carets": 0.5, "price": 405},
        {"id": 2, "carets": 0.75, "price": 782},
        {"id": 3, "carets": 1, "price": 1470},
        {"id": 4, "carets": 1.5, "price": 1997},
        {"id": 5, "carets": 2, "price": 3638}],
    "styles": [
        {"id": 1, "style": "Classic", "price": 500},
        {"id": 2, "style": "Modern", "price": 710},
        {"id": 3, "style": "Vintage", "price": 965}
    ],
    "orders": [
        {"id": 1,"metalId": 3,"sizeId": 2,"styleId": 3,}
    ]
}

def all(resources):
    """gets all a resource"""
    return DATABASE[resources]

def retrieve(resources, id):
    """gets a single resource by id"""
    requested_resource = None
    for resource in DATABASE[resources]:
        if resource["id"] == id:
            requested_resource = resource

    return requested_resource

def retrieve_query(resources,id, query_params):
    requested_resource = None
    for resource in DATABASE[resources]:
        if resource["id"] == id:
            requested_resource = resource.copy()
            for query in query_params:
                if query == "size":
                    found_resource = requested_resource
                    found_resource["size"] = retrieve("sizes", requested_resource["sizeId"])
                    found_resource = requested_resource
                elif query == "metal":
                    found_resource = requested_resource
                    found_resource["metal"] = retrieve("metals", requested_resource["metalId"])
                    found_resource = requested_resource
                elif query == "style":
                    found_resource = requested_resource
                    found_resource["style"] = retrieve("styles", requested_resource["styleId"])
                    found_resource = requested_resource
    return requested_resource

def update(id, new_resource, resources):
    """updates an object"""
    for index, resource in enumerate(DATABASE[resources]):
        if resource["id"] == id:
            # Found the animal. Update the value.
            DATABASE[resources][index] = new_resource
            break
def create(resources, resource):
    """For POST requests to a collection"""
    max_id = DATABASE[resources][-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    resource["id"] = new_id

    # Add the animal dictionary to the list
    DATABASE[resources].append(resource)

    # Return the dictionary with `id` property added
    return resource
def delete(resources, id):
    """For DELETE requests to a single resource"""
        # Initial -1 value for animal index, in case one isn't found
    resource_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, resource in enumerate(DATABASE[resources]):
        if resource["id"] == id:
            # Found the animal. Store the current index.
            resource_index = index

    # If the animal was found, use pop(int) to remove it from list
    if resource_index >= 0:
        DATABASE[resources].pop(resource_index)
