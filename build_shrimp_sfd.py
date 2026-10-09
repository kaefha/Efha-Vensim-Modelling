"""Generate SFD model for The Shrimp Fishery System."""

sfd_content = '''{UTF-8}
Shrimp Population = INTEG (
	+population increase - catch,
		30000)
	~	tons
	~	The Shrimp Population is modelled as a stock that increases through \
		population increase (natural growth) and decreases through catch (harvesting).
	|

population increase = 
	"% of biomass increment" * "Shrimp Population" * (1 - ("Shrimp Population" / "highest population"))
	~	tons/Year
	~	Reproduction rate depending on % of biomass increment and density-dependent \
		carrying capacity constraint.
	|

"% of biomass increment" = 
	0.5
	~	1/Year
	~	Intrinsic biomass increment percentage per year (0.5/year).
	|

highest population = 
	37500
	~	tons
	~	Ecosystem carrying capacity for shrimp biomass.
	|

catch = 
	"catch capacity" * ("Shrimp Population" / "highest population") * RANDOM NORMAL(0.8, 1.2, 1, 0.1, 5)
	~	tons/Year
	~	Harvesting rate determined by catch capacity, shrimp abundance, \
		and environmental noise.
	|

catch capacity = 
	"boat efficiency" * Fleet
	~	tons/Year
	~	Total theoretical harvesting capability of the operating fleet.
	|

boat efficiency = 
	60 + RAMP(3, 2000, 2100)
	~	tons/(boat*Year)
	~	Technological capability per boat starting at 60 in 2000 and increasing \
		linearly by 3 tons/boat/year until 2100 (reaching 360 tons/boat/year).
	|

price per ton = 
	2000
	~	$/ton
	~	Market revenue earned per ton of caught shrimp.
	|

Earnings = 
	catch * "price per ton"
	~	$/Year
	~	Total annual gross revenue of the fishing fleet.
	|

cost per boat = 
	1000000
	~	$/(boat*Year)
	~	Annual capital and operational cost per operating boat ($1,000,000/boat/year).
	|

Costs = 
	Fleet * "cost per boat"
	~	$/Year
	~	Total annual operating costs incurred by the entire fleet.
	|

margin = 
	(Earnings - Costs) / Costs
	~	Dmnl
	~	Economic profit margin of fishing operations ((Earnings - Costs) / Costs).
	|

threshold margin = 
	0.2
	~	Dmnl
	~	Threshold profit margin for fleet expansion (0.2).
	|

percentage change = 
	0.05
	~	1/Year
	~	Fractional adjustment rate of the fleet per year (0.05/year).
	|

net changes in the fleet = 
	IF THEN ELSE(margin > "threshold margin", "percentage change" * margin, - "percentage change" * ABS(margin))
	~	1/Year
	~	Fractional entry or exit rate based on economic profitability.
	|

fleet adjustment rate = 
	"net changes in the fleet" * Fleet
	~	boat/Year
	~	Annual net change in the number of operating boats.
	|

Fleet = INTEG (
	+fleet adjustment rate,
		50)
	~	boat
	~	Number of operating fishing boats in the fishery (initial = 50 boats).
	|

********************************************************
	.Control
********************************************************~
		Simulation Control Parameters
	|

FINAL TIME = 2100
	~	Year
	~	The final time for the simulation.
	|

INITIAL TIME = 2000
	~	Year
	~	The initial time for the simulation.
	|

SAVEPER = 
        TIME STEP
	~	Year
	~	The frequency with which output is stored.
	|

TIME STEP = 0.0625
	~	Year
	~	The time step for the simulation (Euler method).
	|

\\\\\\---/// Sketch information - do not modify anything except names
V300  Do not put anything below this section - it will be ignored
*View 1
$192-192-192,0,Times New Roman|12||0-0-0|0-0-0|0-0-255|-1--1--1|-1--1--1|96,96
10,1,Shrimp Population,350,110,65,22,3,3,0,0,0,0,0,0
12,2,48,110,110,10,8,0,3,0,0,-1,0,0,0
1,3,5,1,4,0,0,22,0,0,0,-1--1--1,,1|(270,110)|
1,4,5,2,100,0,0,22,0,0,0,-1--1--1,,1|(165,110)|
11,5,48,215,110,6,8,34,3,0,0,1,0,0,0
10,6,population increase,215,135,62,11,32,3,0,0,-1,0,0,0
12,7,48,600,110,10,8,0,3,0,0,-1,0,0,0
1,8,10,7,4,0,0,22,0,0,0,-1--1--1,,1|(545,110)|
1,9,10,1,100,0,0,22,0,0,0,-1--1--1,,1|(445,110)|
11,10,48,495,110,6,8,34,3,0,0,1,0,0,0
10,11,catch,495,135,26,11,32,3,0,0,-1,0,0,0
10,12,% of biomass increment,130,195,78,11,0,3,0,0,0,0,0,0
10,13,highest population,350,220,62,11,0,3,0,0,0,0,0,0
10,14,catch capacity,495,240,49,11,0,3,0,0,0,0,0,0
10,15,boat efficiency,630,240,49,11,0,3,0,0,0,0,0,0
10,16,price per ton,630,170,41,11,0,3,0,0,0,0,0,0
10,17,Earnings,580,310,31,11,0,3,0,0,0,0,0,0
10,18,cost per boat,700,380,47,11,0,3,0,0,0,0,0,0
10,19,Costs,580,380,22,11,0,3,0,0,0,0,0,0
10,20,margin,460,350,26,11,0,3,0,0,0,0,0,0
10,21,threshold margin,460,420,53,11,0,3,0,0,0,0,0,0
10,22,percentage change,300,420,58,11,0,3,0,0,0,0,0,0
10,23,net changes in the fleet,320,350,78,11,0,3,0,0,0,0,0,0
10,24,Fleet,180,480,40,20,3,3,0,0,0,0,0,0
12,25,48,390,480,10,8,0,3,0,0,-1,0,0,0
1,26,28,24,4,0,0,22,0,0,0,-1--1--1,,1|(240,480)|
1,27,28,25,100,0,0,22,0,0,0,-1--1--1,,1|(340,480)|
11,28,48,290,480,6,8,34,3,0,0,1,0,0,0
10,29,fleet adjustment rate,290,505,67,11,32,3,0,0,-1,0,0,0
1,30,12,6,1,0,0,0,0,0,0,-1--1--1,,1|(175,160)|
1,31,1,6,1,0,0,0,0,0,0,-1--1--1,,1|(270,165)|
1,32,13,6,1,0,0,0,0,0,0,-1--1--1,,1|(275,185)|
1,33,1,11,1,0,0,0,0,0,0,-1--1--1,,1|(435,160)|
1,34,13,11,1,0,0,0,0,0,0,-1--1--1,,1|(435,190)|
1,35,14,11,1,0,0,0,0,0,0,-1--1--1,,1|(495,190)|
1,36,15,14,1,0,0,0,0,0,0,-1--1--1,,1|(560,240)|
1,37,24,14,1,0,0,0,0,0,0,-1--1--1,,1|(325,270)|
1,38,11,17,1,0,0,0,0,0,0,-1--1--1,,1|(550,215)|
1,39,16,17,1,0,0,0,0,0,0,-1--1--1,,1|(605,245)|
1,40,18,19,1,0,0,0,0,0,0,-1--1--1,,1|(640,380)|
1,41,24,19,1,0,0,0,0,0,0,-1--1--1,,1|(370,410)|
1,42,17,20,1,0,0,0,0,0,0,-1--1--1,,1|(520,330)|
1,43,19,20,1,0,0,0,0,0,0,-1--1--1,,1|(520,365)|
1,44,20,23,1,0,0,0,0,0,0,-1--1--1,,1|(390,350)|
1,45,21,23,1,0,0,0,0,0,0,-1--1--1,,1|(390,390)|
1,46,22,23,1,0,0,0,0,0,0,-1--1--1,,1|(310,390)|
1,47,23,29,1,0,0,0,0,0,0,-1--1--1,,1|(305,435)|
1,48,24,29,1,0,0,0,0,0,0,-1--1--1,,1|(220,535)|
///---\\\\
:GRAPH BIOMASS
:TITLE Shrimp Biomass and Carrying Capacity
:SCALE
:VAR highest population
:Y-MIN 0
:Y-MAX 40000
:LINE-WIDTH 2
:VAR Shrimp Population
:Y-MIN 0
:Y-MAX 40000
:LINE-WIDTH 3
:GRAPH HARVEST
:TITLE Catch and Catch Capacity
:SCALE
:VAR catch
:VAR catch capacity
:LINE-WIDTH 2
:GRAPH FLEET
:TITLE Fleet Dynamics
:SCALE
:VAR Fleet
:Y-MIN 0
:Y-MAX 100
:LINE-WIDTH 2
:GRAPH ECONOMICS
:TITLE Economic Margin and Earnings
:SCALE
:VAR margin
:VAR Earnings
:VAR Costs
'''

with open("The Shrimp Fishery System/FirstName_UTS_SFD1.mdl", "w", encoding="utf-8") as f:
    f.write(sfd_content.strip() + "\\n")

with open("The Shrimp Fishery System/Shrimp_Fishery_SFD.mdl", "w", encoding="utf-8") as f:
    f.write(sfd_content.strip() + "\\n")

print("Generated SFD models successfully!")
