import pandas as pd

def parse_busy_day(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Parse grid and simulation info
    grid_info = list(map(int, lines[0].split()))
    grid_row, grid_col, num_drones, deadline, max_payload = grid_info

    # Save grid info
    grid_df = pd.DataFrame(
        [{
            'grid_row': grid_row,
            'grid_col': grid_col,
            'num_drones': num_drones,
            'deadline': deadline,
            'max_payload': max_payload
        }]
    )
    grid_df.to_csv('grid.csv', index=False)

    # Products
    num_products = int(lines[1])
    product_weights = list(map(int, lines[2].split()))
    products_df = pd.DataFrame({
        'product_id': list(range(num_products)),
        'weight': product_weights
    })
    products_df.to_csv('products.csv', index=False)

    # Warehouses
    warehouse_ptr = 3
    num_warehouses = int(lines[warehouse_ptr])
    warehouses = []
    for i in range(num_warehouses):
        location = list(map(int, lines[warehouse_ptr + 1 + i*2].split()))
        stock = list(map(int, lines[warehouse_ptr + 2 + i*2].split()))
        warehouse_row = [i] + location + stock
        warehouses.append(warehouse_row)
    warehouse_columns = ['warehouse_id', 'row', 'col'] + [f'product_{j}_qty' for j in range(num_products)]
    warehouses_df = pd.DataFrame(warehouses, columns=warehouse_columns)
    warehouses_df.to_csv('warehouses.csv', index=False)

    # Orders
    orders_start = warehouse_ptr + 1 + num_warehouses*2
    num_orders = int(lines[orders_start])
    orders = []
    line_idx = orders_start + 1
    for oid in range(num_orders):
        loc = list(map(int, lines[line_idx].split()))
        line_idx += 1
        num_items = int(lines[line_idx])
        line_idx += 1
        prod_list = list(map(int, lines[line_idx].split()))
        line_idx += 1
        order_row = [oid] + loc + [num_items] + prod_list
        orders.append(order_row)
    # Category columns for products ordered
    max_order_items = max(len(row[4:]) for row in orders)
    order_cols = ['order_id', 'row', 'col', 'num_items'] + [f'product_{i}_id' for i in range(max_order_items)]
    # Pad product list for each order to match length
    for order in orders:
        while len(order) < 4 + max_order_items:
            order.append('')
    orders_df = pd.DataFrame(orders, columns=order_cols)
    orders_df.to_csv('orders.csv', index=False)

    print("CSV files saved: grid.csv, products.csv, warehouses.csv, orders.csv")

parse_busy_day('busy_day.in')
