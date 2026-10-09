"""Generate CLD model for The Shrimp Fishery System."""

cld_content = '''{UTF-8}
"% of biomass increment" = 0.5
	~	1/Year
	~	|

boat efficiency = 60 + RAMP(3, 2000, 2100)
	~	tons/(boat*Year)
	~	|

catch = "catch capacity" * ("Shrimp Population" / "highest population") * RANDOM NORMAL(0.8, 1.2, 1, 0.1, 5)
	~	tons/Year
	~	|

catch capacity = "boat efficiency" * Fleet
	~	tons/Year
	~	|

cost per boat = 1000000
	~	$/(boat*Year)
	~	|

Costs = Fleet * "cost per boat"
	~	$/Year
	~	|

Earnings = catch * "price per ton"
	~	$/Year
	~	|

FINAL TIME = 2100
	~	Year
	~	|

Fleet = INTEG(fleet adjustment rate, 50)
	~	boat
	~	|

fleet adjustment rate = "net changes in the fleet" * Fleet
	~	boat/Year
	~	|

highest population = 37500
	~	tons
	~	|

INITIAL TIME = 2000
	~	Year
	~	|

margin = (Earnings - Costs) / Costs
	~	Dmnl
	~	|

net changes in the fleet = IF THEN ELSE(margin > "threshold margin", "percentage change" * margin, - "percentage change" * ABS(margin))
	~	1/Year
	~	|

percentage change = 0.05
	~	1/Year
	~	|

population increase = "% of biomass increment" * "Shrimp Population" * (1 - ("Shrimp Population" / "highest population"))
	~	tons/Year
	~	|

price per ton = 2000
	~	$/ton
	~	|

SAVEPER = 1
	~	Year
	~	|

Shrimp Population = INTEG(population increase - catch, 30000)
	~	tons
	~	|

threshold margin = 0.2
	~	Dmnl
	~	|

TIME STEP = 0.0625
	~	Year
	~	|

\\\\\\---/// Sketch information - do not modify anything except names
V300  Do not put anything below this section - it will be ignored
*View 1
$192-192-192,0,Times New Roman|12||0-0-0|0-0-0|0-0-255|-1--1--1|-1--1--1|96,96
10,1,Shrimp Population,350,90,55,18,8,3,0,0,0,0,0,0
10,2,population increase,180,90,55,18,8,3,0,0,0,0,0,0
10,3,% of biomass increment,90,160,65,18,8,3,0,0,0,0,0,0
10,4,highest population,280,180,55,18,8,3,0,0,0,0,0,0
10,5,catch,520,90,30,18,8,3,0,0,0,0,0,0
10,6,catch capacity,520,200,45,18,8,3,0,0,0,0,0,0
10,7,boat efficiency,660,200,45,18,8,3,0,0,0,0,0,0
10,8,Earnings,660,290,35,18,8,3,0,0,0,0,0,0
10,9,price per ton,720,240,40,18,8,3,0,0,0,0,0,0
10,10,Costs,520,380,25,18,8,3,0,0,0,0,0,0
10,11,cost per boat,640,430,45,18,8,3,0,0,0,0,0,0
10,12,margin,400,340,30,18,8,3,0,0,0,0,0,0
10,13,threshold margin,480,440,50,18,8,3,0,0,0,0,0,0
10,14,percentage change,350,440,55,18,8,3,0,0,0,0,0,0
10,15,net changes in the fleet,270,340,70,18,8,3,0,0,0,0,0,0
10,16,fleet adjustment rate,160,280,65,18,8,3,0,0,0,0,0,0
10,17,Fleet,260,250,30,18,8,3,0,0,0,0,0,0
10,18,R1: Reproduction,250,50,45,15,8,1,0,0,0,0,0,0
10,19,B1: Carrying Capacity,230,135,55,15,8,1,0,0,0,0,0,0
10,20,B2: Catch Availability,440,50,55,15,8,1,0,0,0,0,0,0
10,21,R2: Fleet Expansion,320,300,50,15,8,1,0,0,0,0,0,0
10,22,B3: Cost Limit,460,300,45,15,8,1,0,0,0,0,0,0
10,23,B4: Commons Depletion,400,160,65,15,8,1,0,0,0,0,0,0
1,24,1,2,1,0,43,0,0,0,0,-1--1--1,,1|(260,65)|
1,25,2,1,1,0,43,0,0,0,0,-1--1--1,,1|(260,115)|
1,26,3,2,1,0,43,0,0,0,0,-1--1--1,,1|(135,125)|
1,27,4,2,1,0,45,0,0,0,0,-1--1--1,,1|(230,135)|
1,28,1,5,1,0,43,0,0,0,0,-1--1--1,,1|(435,65)|
1,29,5,1,1,0,45,0,0,0,0,-1--1--1,,1|(435,115)|
1,30,4,5,1,0,45,0,0,0,0,-1--1--1,,1|(400,135)|
1,31,6,5,1,0,43,0,0,0,0,-1--1--1,,1|(520,145)|
1,32,7,6,1,0,43,0,0,0,0,-1--1--1,,1|(590,200)|
1,33,17,6,1,0,43,0,0,0,0,-1--1--1,,1|(390,225)|
1,34,5,8,1,0,43,0,0,0,0,-1--1--1,,1|(590,190)|
1,35,9,8,1,0,43,0,0,0,0,-1--1--1,,1|(690,265)|
1,36,17,10,1,0,43,0,0,0,0,-1--1--1,,1|(390,315)|
1,37,11,10,1,0,43,0,0,0,0,-1--1--1,,1|(580,405)|
1,38,8,12,1,0,43,0,0,0,0,-1--1--1,,1|(530,315)|
1,39,10,12,1,0,45,0,0,0,0,-1--1--1,,1|(460,360)|
1,40,12,15,1,0,43,0,0,0,0,-1--1--1,,1|(335,340)|
1,41,13,15,1,0,45,0,0,0,0,-1--1--1,,1|(375,390)|
1,42,14,15,1,0,43,0,0,0,0,-1--1--1,,1|(310,390)|
1,43,15,16,1,0,43,0,0,0,0,-1--1--1,,1|(215,310)|
1,44,17,16,1,0,43,0,0,0,0,-1--1--1,,1|(210,265)|
1,45,16,17,1,0,43,0,0,0,0,-1--1--1,,1|(210,230)|
///---\\\\
'''

with open("The Shrimp Fishery System/FirstName_UTS_CLD.mdl", "w", encoding="utf-8") as f:
    f.write(cld_content.strip() + "\\n")

with open("The Shrimp Fishery System/Shrimp_Fishery_CLD.mdl", "w", encoding="utf-8") as f:
    f.write(cld_content.strip() + "\\n")

print("Generated CLD models successfully!")
