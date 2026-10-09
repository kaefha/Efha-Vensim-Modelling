def sim_model_1(dt=0.125, tf=100.0):
    t = 0.0
    taor = 8.0
    dic = 4.0
    tci = 8.0
    
    inventory = 4000.0
    avg_order_rate = 1000.0
    
    times = []
    inv_list = []
    des_inv_list = []
    order_list = []
    avg_order_list = []
    prod_list = []
    
    while t <= tf + 1e-9:
        order_rate = 1000.0 * (1.0 + (0.1 if t >= 10.0 else 0.0))
        shipment_rate = order_rate
        
        desired_inventory = avg_order_rate * dic
        correction_for_inventory = (desired_inventory - inventory) / tci
        desired_prod_rate = avg_order_rate + correction_for_inventory
        prod_rate = desired_prod_rate
        
        times.append(t)
        inv_list.append(inventory)
        des_inv_list.append(desired_inventory)
        order_list.append(order_rate)
        avg_order_list.append(avg_order_rate)
        prod_list.append(prod_rate)
        
        d_avg_order = (order_rate - avg_order_rate) / taor
        d_inventory = prod_rate - shipment_rate
        
        avg_order_rate += d_avg_order * dt
        inventory += d_inventory * dt
        t += dt
        
    return times, inv_list, des_inv_list, order_list, avg_order_list, prod_list

def sim_model_2(dt=0.125, tf=100.0):
    t = 0.0
    taor = 8.0
    dic = 4.0
    tci = 8.0
    ade = 50.0
    alp = 20.0
    tcl = 24.0
    
    inventory = 4000.0
    labor = 50.0
    avg_order_rate = 1000.0
    
    times = []
    inv_list = []
    des_inv_list = []
    order_list = []
    avg_order_list = []
    des_prod_list = []
    prod_list = []
    labor_list = []
    
    while t <= tf + 1e-9:
        order_rate = 1000.0 * (1.0 + (0.1 if t >= 10.0 else 0.0))
        shipment_rate = order_rate
        
        desired_inventory = avg_order_rate * dic
        correction_for_inventory = (desired_inventory - inventory) / tci
        desired_prod_rate = avg_order_rate + correction_for_inventory
        
        desired_labor = desired_prod_rate / alp
        correction_for_labor = (desired_labor - labor) / tcl
        quit_rate = labor / ade
        hiring_rate = quit_rate + correction_for_labor
        normal_prod_rate = labor * alp
        prod_rate = normal_prod_rate
        
        times.append(t)
        inv_list.append(inventory)
        des_inv_list.append(desired_inventory)
        order_list.append(order_rate)
        avg_order_list.append(avg_order_rate)
        des_prod_list.append(desired_prod_rate)
        prod_list.append(prod_rate)
        labor_list.append(labor)
        
        d_avg_order = (order_rate - avg_order_rate) / taor
        d_inventory = prod_rate - shipment_rate
        d_labor = hiring_rate - quit_rate
        
        avg_order_rate += d_avg_order * dt
        inventory += d_inventory * dt
        labor += d_labor * dt
        t += dt
        
    return times, inv_list, des_inv_list, order_list, avg_order_list, des_prod_list, prod_list, labor_list

print("=== MODEL 1 ===")
t1, inv1, des_inv1, ord1, avg_ord1, prod1 = sim_model_1(dt=0.125)
min_inv1 = min(inv1)
min_inv1_t = t1[inv1.index(min_inv1)]
max_prod1 = max(prod1)
max_prod1_t = t1[prod1.index(max_prod1)]
print(f"Min Inventory: {min_inv1:.1f} at t={min_inv1_t:.1f}")
print(f"Max Production rate: {max_prod1:.1f} at t={max_prod1_t:.1f}")
print(f"Final Inventory at t=100: {inv1[-1]:.1f}, Desired Inventory: {des_inv1[-1]:.1f}")

print("\n=== MODEL 2 ===")
t2, inv2, des_inv2, ord2, avg_ord2, des_prod2, prod2, lab2 = sim_model_2(dt=0.125)
min_inv2 = min(inv2)
min_inv2_t = t2[inv2.index(min_inv2)]
max_inv2 = max(inv2)
max_inv2_t = t2[inv2.index(max_inv2)]
max_des_prod2 = max(des_prod2)
max_des_prod2_t = t2[des_prod2.index(max_des_prod2)]
min_des_prod2 = min(des_prod2[int(10/0.125):])
min_des_prod2_t = t2[des_prod2.index(min_des_prod2)]
max_prod2 = max(prod2)
max_prod2_t = t2[prod2.index(max_prod2)]

print(f"Min Inventory: {min_inv2:.1f} at t={min_inv2_t:.1f}")
print(f"Max Inventory: {max_inv2:.1f} at t={max_inv2_t:.1f}")
print(f"Max Desired Production: {max_des_prod2:.1f} at t={max_des_prod2_t:.1f}")
print(f"Min Desired Production: {min_des_prod2:.1f} at t={min_des_prod2_t:.1f}")
print(f"Max Production rate: {max_prod2:.1f} at t={max_prod2_t:.1f}")
