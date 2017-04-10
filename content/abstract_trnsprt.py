from pyomo.environ import AbstractModel, Set, Param, Var, Constraint, Objective, minimize
 
model = AbstractModel()

model.plants = Set(doc="Canning plants")
model.markets = Set(doc="Markets")

model.capacity_plant = Param(model.plants, doc='Capacity of a plant in cases')
model.demand_market = Param(model.markets, doc='Demand of a market in cases')
model.distance_in_thousand_miles = \
    Param(model.plants, model.markets, doc='Distance between plant and marekt in thousands of miles')
model.freight_costs_per_case_and_thousand_miles = \
    Param(initialize=90, doc='Freight in dollars per case per thousand miles')

	
def freight_costs_per_case_in_thousands(model, plant, market):
    return model.freight_costs_per_case_and_thousand_miles * model.distance_in_thousand_miles[plant,market] / 1000

model.freight_costs_per_case_in_thousands = Param(model.plants, 
                                                  model.markets, 
                                                  initialize=freight_costs_per_case_in_thousands, 
                                                  doc='Transport cost in thousands of dollar per case')

model.shipment_quantities_in_cases = Var(model.plants, model.markets, bounds=(0, None), doc='Shipment quantities in case')


def supply_rule(model, plant):
  return sum(model.shipment_quantities_in_cases[plant,market] for market in model.markets) \
            <= model.capacity_plant[plant]

def demand_rule(model, market):
  return sum(model.shipment_quantities_in_cases[plant, market] for plant in model.plants) \
            >= model.demand_market[market] 

model.supply_constraint = Constraint(model.plants, rule=supply_rule, doc='Limit supply limit at each plant')
model.demand_constraint = Constraint(model.markets, rule=demand_rule, doc='Satisfy demand at each market')

def objective_rule(model):
  return sum(model.freight_costs_per_case_in_thousands[plant,market] *
             model.shipment_quantities_in_cases[plant,market] 
                 for plant in model.plants for market in model.markets)

model.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')