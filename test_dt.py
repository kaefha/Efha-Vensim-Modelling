def test_timesteps():
    for dt in [1.0, 0.5, 0.25, 0.125, 0.0625]:
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
        
        min_inv = 4000.0
        max_inv = 0.0
        max_des_prod = 0.0
        min_des_prod = 2000.0
        max_prod = 0.0
        
        while t <= 100.0 + 1e-9:
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
            
            if inventory < min_inv: min_inv = inventory
            if inventory > max_inv: max_inv = inventory
            if desired_prod_rate > max_des_prod: max_des_prod = desired_prod_rate
            if t > 10.0 and desired_prod_rate < min_des_prod: min_des_prod = desired_prod_rate
            if prod_rate > max_prod: max_prod = prod_rate
            
            d_avg_order = (order_rate - avg_order_rate) / taor
            d_inventory = prod_rate - shipment_rate
            d_labor = hiring_rate - quit_rate
            
            avg_order_rate += d_avg_order * dt
            inventory += d_inventory * dt
            labor += d_labor * dt
            t += dt
            
        print(f"dt={dt:6f}: MinInv={min_inv:.1f}, MaxInv={max_inv:.1f}, MaxDesProd={max_des_prod:.1f}, MinDesProd={min_des_prod:.1f}, MaxProd={max_prod:.1f}")

test_timesteps()
