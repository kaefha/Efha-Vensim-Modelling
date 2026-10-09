import math
from PIL import Image, ImageDraw, ImageFont

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

def draw_single_plot(draw, font, font_bold, x_box, y_box, w_box, h_box, 
                     x_range, y_range, y_ticks, x_ticks, curves, labels, x_title="Time (Week)"):
    # Background
    draw.rectangle([x_box, y_box, x_box + w_box, y_box + h_box], fill="white", outline="#333333", width=2)
    
    # Grid lines
    for yt in y_ticks:
        if y_range[0] <= yt <= y_range[1]:
            py = y_box + h_box - (yt - y_range[0]) / (y_range[1] - y_range[0]) * h_box
            draw.line([(x_box, py), (x_box + w_box, py)], fill="#CCCCCC", width=1)
            # Y label
            lbl = f"{int(yt):,}"
            bbox = font.getbbox(lbl)
            lw = bbox[2] - bbox[0]
            lh = bbox[3] - bbox[1]
            draw.text((x_box - lw - 12, py - lh // 2), lbl, fill="#222222", font=font)
            
    for xt in x_ticks:
        if x_range[0] <= xt <= x_range[1]:
            px = x_box + (xt - x_range[0]) / (x_range[1] - x_range[0]) * w_box
            draw.line([(px, y_box), (px, y_box + h_box)], fill="#CCCCCC", width=1)
            # X label
            lbl = f"{int(xt)}"
            bbox = font.getbbox(lbl)
            lw = bbox[2] - bbox[0]
            lh = bbox[3] - bbox[1]
            draw.text((px - lw // 2, y_box + h_box + 8), lbl, fill="#222222", font=font)
            
    # X Axis Title
    bbox = font.getbbox(x_title)
    lw = bbox[2] - bbox[0]
    draw.text((x_box + w_box // 2 - lw // 2, y_box + h_box + 30), x_title, fill="#222222", font=font)
    
    # Plot curves
    for (times, values, color, width) in curves:
        pts = []
        for t, v in zip(times, values):
            px = x_box + (t - x_range[0]) / (x_range[1] - x_range[0]) * w_box
            py = y_box + h_box - (v - y_range[0]) / (y_range[1] - y_range[0]) * h_box
            pts.append((px, py))
        if len(pts) > 1:
            draw.line(pts, fill=color, width=width)
            
    # Draw in-graph labels
    for text, (t_pos, v_pos), color in labels:
        px = x_box + (t_pos - x_range[0]) / (x_range[1] - x_range[0]) * w_box
        py = y_box + h_box - (v_pos - y_range[0]) / (y_range[1] - y_range[0]) * h_box
        draw.text((px, py), text, fill=color, font=font_bold)

def generate_graphs():
    # Load default truetype font or bitmap font
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font

    # --- MODEL 1 GRAPH ---
    t1, inv1, des_inv1, ord1, avg_ord1, prod1 = sim_model_1(dt=1.0)
    img1 = Image.new("RGB", (800, 900), "white")
    draw1 = ImageDraw.Draw(img1)
    
    # Top plot: Inventory & Desired Inventory
    curves_top1 = [
        (t1, des_inv1, "#111111", 3),
        (t1, inv1, "#444444", 2)
    ]
    labels_top1 = [
        ("Desired inventory", (12.0, 4700.0), "#111111"),
        ("Inventory", (20.0, 3650.0), "#444444")
    ]
    draw_single_plot(draw1, font, font_bold, 120, 50, 620, 340,
                     (0.0, 100.0), (2800.0, 5200.0),
                     [2800, 3400, 4000, 4600, 5200],
                     [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                     curves_top1, labels_top1)
                     
    # Bottom plot: Order rate, Average order rate, Production rate
    curves_bot1 = [
        (t1, ord1, "#555555", 2),
        (t1, avg_ord1, "#777777", 2),
        (t1, prod1, "#111111", 2)
    ]
    labels_bot1 = [
        ("Order rate", (11.0, 1115.0), "#555555"),
        ("Average order rate", (25.0, 1050.0), "#777777"),
        ("Production rate", (25.0, 1160.0), "#111111")
    ]
    draw_single_plot(draw1, font, font_bold, 120, 490, 620, 340,
                     (0.0, 100.0), (900.0, 1300.0),
                     [900, 1000, 1100, 1200, 1300],
                     [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                     curves_bot1, labels_bot1)
                     
    img1.save("sfd_model_1_simulation_graph.png", "PNG")
    print("Saved sfd_model_1_simulation_graph.png")
    
    # --- MODEL 2 GRAPH ---
    t2, inv2, des_inv2, ord2, avg_ord2, des_prod2, prod2, lab2 = sim_model_2(dt=1.0)
    img2 = Image.new("RGB", (800, 900), "white")
    draw2 = ImageDraw.Draw(img2)
    
    # Top plot: Order rate, Average order rate, Production rate, Desired production rate
    curves_top2 = [
        (t2, ord2, "#777777", 2),
        (t2, avg_ord2, "#888888", 2),
        (t2, des_prod2, "#333333", 2),
        (t2, prod2, "#111111", 2)
    ]
    labels_top2 = [
        ("Order rate", (11.0, 1115.0), "#777777"),
        ("Average order rate", (28.0, 1050.0), "#888888"),
        ("Desired production rate", (33.0, 1285.0), "#333333"),
        ("Production rate", (52.0, 1195.0), "#111111")
    ]
    draw_single_plot(draw2, font, font_bold, 120, 50, 620, 340,
                     (0.0, 100.0), (900.0, 1300.0),
                     [900, 1000, 1100, 1200, 1300],
                     [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                     curves_top2, labels_top2)
                     
    # Bottom plot: Inventory & Desired Inventory
    curves_bot2 = [
        (t2, des_inv2, "#111111", 3),
        (t2, inv2, "#333333", 2)
    ]
    labels_bot2 = [
        ("Desired inventory", (20.0, 4550.0), "#111111"),
        ("Inventory", (40.0, 3600.0), "#333333")
    ]
    draw_single_plot(draw2, font, font_bold, 120, 490, 620, 340,
                     (0.0, 100.0), (2800.0, 5200.0),
                     [2800, 3400, 4000, 4600, 5200],
                     [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                     curves_bot2, labels_bot2)
                     
    img2.save("sfd_model_2_simulation_graph.png", "PNG")
    print("Saved sfd_model_2_simulation_graph.png")

generate_graphs()

