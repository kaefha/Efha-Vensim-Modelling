import re

def update_model2_sketch():
    with open("Model_2_Production_Inventory_Labor.mdl", "r", encoding="utf-8") as f:
        content = f.read()
        
    eq_part, sketch_part = content.split("\\\\\\---/// Sketch information")
    
    # Let's inspect object IDs in Model 2
    # Inventory = 1
    # Labor = 2
    # Cloud1 (Prod) = 3
    # Valve1 (Prod) = 4
    # Label1 (Prod rate) = 5
    # Cloud2 (Ship) = 6
    # Valve2 (Ship) = 7
    # Label2 (Ship rate) = 8
    
    # We want:
    # Quit rate on the left of Labor:
    # Cloud_quit at x=130, y=700
    # Valve_quit at x=240, y=700
    # Label_quit at x=240, y=730
    
    # Hiring rate on the right of Labor:
    # Cloud_hire at x=670, y=700
    # Valve_hire at x=560, y=700
    # Label_hire at x=560, y=730
    
    # Let's check IDs in current Model 2:
    # 9: cloud (was left: 140, 700)
    # 10: valve (was left: 270, 700)
    # 11: Hiring rate label (was left: 270, 730)
    # 12: cloud (was right: 660, 700)
    # 13: valve (was right: 530, 700)
    # 14: Quit rate label (was right: 530, 730)
    
    # We can swap IDs 10,11 (Hiring rate) and 13,14 (Quit rate) positions!
    # Valve_quit = 13 at (240, 700), Label_quit = 14 at (240, 730)
    # Cloud_quit = 9 at (130, 700)
    # Pipe for Quit rate:
    # from Labor (2) to Valve_quit (13): flow from stock to valve (physical=100)
    # from Valve_quit (13) to Cloud_quit (9): flow from valve to cloud (physical=4)
    
    # Valve_hire = 10 at (560, 700), Label_hire = 11 at (560, 730)
    # Cloud_hire = 12 at (670, 700)
    # Pipe for Hiring rate:
    # from Cloud_hire (12) to Valve_hire (10): from cloud to valve (physical=100)
    # from Valve_hire (10) to Labor (2): from valve into stock (physical=4)
    
    # Let's write out the new sketch section clearly:
    sketch_lines = [
        r"\---/// Sketch information - do not modify anything except names",
        "V300  Do not put anything below this section - it will be ignored",
        "*Production and Inventory Model 2",
        "$192-192-192,0,Vensim Sans SC|12||0-0-0|0-0-0|0-0-0|-1--1--1|-1--1--1|96,96,100,0",
        "10,1,Inventory,400,70,66,22,3,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,2,Labor,400,700,50,22,3,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "12,3,48,140,70,10,8,0,3,0,0,-1,0,0,0,0,0,0,0,0,0",
        "11,4,0,270,70,6,8,34,3,0,0,1,0,0,0,0,0,0,0,0,0",
        "10,5,Production rate,270,100,90,12,40,131,0,0,-1,0,0,0,0,0,0,0,0,0",
        "12,6,48,660,70,10,8,0,3,0,0,-1,0,0,0,0,0,0,0,0,0",
        "11,7,0,530,70,6,8,34,3,0,0,1,0,0,0,0,0,0,0,0,0",
        "10,8,Shipment rate,530,100,78,12,40,131,0,0,-1,0,0,0,0,0,0,0,0,0",
        "12,9,48,130,700,10,8,0,3,0,0,-1,0,0,0,0,0,0,0,0,0",
        "11,10,0,560,700,6,8,34,3,0,0,1,0,0,0,0,0,0,0,0,0",
        "10,11,Hiring rate,560,730,66,12,40,131,0,0,-1,0,0,0,0,0,0,0,0,0",
        "12,12,48,670,700,10,8,0,3,0,0,-1,0,0,0,0,0,0,0,0,0",
        "11,13,0,240,700,6,8,34,3,0,0,1,0,0,0,0,0,0,0,0,0",
        "10,14,Quit rate,240,730,54,12,40,131,0,0,-1,0,0,0,0,0,0,0,0,0",
        "10,15,Order rate,720,200,66,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,16,taor,620,400,32,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,17,Average order rate,520,340,114,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,18,dic,640,270,32,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,19,Desired inventory,530,220,108,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,20,tci,450,140,32,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,21,Correction for inventory,360,180,150,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,22,Desired production rate,360,390,144,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,23,ade,180,570,32,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,24,Average labor productivity,380,520,162,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,25,Desired labor,600,460,84,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,26,tcl,660,540,32,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,27,Correction for labor,580,560,126,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        "10,28,Normal production rate,180,440,138,12,8,131,0,0,0,0,0,0,0,0,0,0,0,0",
        # Pipes:
        "1,29,4,3,100,0,0,22,1,64,0,0-0-0,,1|(205,70)|", # Prod valve to cloud
        "1,30,4,1,4,0,0,22,1,64,0,0-0-0,,1|(335,70)|",   # Prod valve to Inventory
        "1,31,7,1,100,0,0,22,1,64,0,0-0-0,,1|(465,70)|", # Inventory to Ship valve
        "1,32,7,6,4,0,0,22,1,64,0,0-0-0,,1|(595,70)|",   # Ship valve to cloud
        "1,33,10,12,100,0,0,22,1,64,0,0-0-0,,1|(615,700)|", # Cloud 12 to Hire valve 10
        "1,34,10,2,4,0,0,22,1,64,0,0-0-0,,1|(480,700)|",    # Hire valve 10 into Labor 2
        "1,35,13,2,100,0,0,22,1,64,0,0-0-0,,1|(320,700)|",  # Labor 2 to Quit valve 13
        "1,36,13,9,4,0,0,22,1,64,0,0-0-0,,1|(185,700)|",    # Quit valve 13 to Cloud 9
        # Information arrows:
        "1,37,28,4,1,0,43,0,1,64,0,0-0-0,,1|(140,240)|",    # Normal prod rate -> Prod rate valve (curving up on left)
        "1,38,15,8,1,0,43,0,1,64,0,0-0-0,,1|(666,142)|",    # Order rate -> Shipment rate
        "1,39,15,17,1,0,43,0,1,64,0,0-0-0,,1|(654,318)|",   # Order rate -> Average order rate
        "1,40,16,17,1,0,45,0,1,64,0,0-0-0,,1|(569,337)|",   # taor -> Average order rate
        "1,41,17,19,1,0,43,0,1,64,0,0-0-0,,1|(525,280)|",   # Average order rate -> Desired inventory
        "1,42,18,19,1,0,43,0,1,64,0,0-0-0,,1|(614,226)|",   # dic -> Desired inventory
        "1,43,19,21,1,0,43,0,1,64,0,0-0-0,,1|(476,182)|",   # Desired inventory -> Correction for inventory
        "1,44,1,21,1,0,45,0,1,64,0,0-0-0,,1|(367,120)|",    # Inventory -> Correction for inventory
        "1,45,20,21,1,0,45,0,1,64,0,0-0-0,,1|(401,188)|",   # tci -> Correction for inventory
        "1,46,17,22,1,0,43,0,1,64,0,0-0-0,,1|(457,335)|",   # Average order rate -> Desired prod rate
        "1,47,21,22,1,0,43,0,1,64,0,0-0-0,,1|(360,285)|",   # Correction for inventory -> Desired prod rate
        "1,48,27,10,1,0,43,0,1,64,0,0-0-0,,1|(570,630)|",   # Correction for labor -> Hiring rate valve
        "1,49,14,10,1,0,43,0,1,64,0,0-0-0,,1|(400,775)|",   # Quit rate -> Hiring rate valve (curving underneath Labor!)
        "1,50,2,13,1,0,43,0,1,64,0,0-0-0,,1|(320,715)|",    # Labor -> Quit rate valve
        "1,51,23,13,1,0,45,0,1,64,0,0-0-0,,1|(210,635)|",   # ade -> Quit rate valve
        "1,52,24,25,1,0,45,0,1,64,0,0-0-0,,1|(490,490)|",   # Avg labor prod -> Desired labor
        "1,53,22,25,1,0,43,0,1,64,0,0-0-0,,1|(488,396)|",   # Desired prod rate -> Desired labor
        "1,54,25,27,1,0,43,0,1,64,0,0-0-0,,1|(590,510)|",   # Desired labor -> Correction for labor
        "1,55,2,27,1,0,45,0,1,64,0,0-0-0,,1|(490,630)|",    # Labor -> Correction for labor
        "1,56,26,27,1,0,45,0,1,64,0,0-0-0,,1|(620,550)|",   # tcl -> Correction for labor
        "1,57,24,28,1,0,43,0,1,64,0,0-0-0,,1|(280,480)|",   # Avg labor prod -> Normal prod rate
        "1,58,2,28,1,0,43,0,1,64,0,0-0-0,,1|(290,570)|",    # Labor -> Normal prod rate
        "///---\\\\",
        ""
    ]
    
    new_content = eq_part + "\\\\\\---/// Sketch information\n" + "\n".join(sketch_lines)
    with open("Model_2_Production_Inventory_Labor.mdl", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated Model 2 sketch successfully.")

update_model2_sketch()
