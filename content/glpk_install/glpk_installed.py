from pyomo.environ import ConcreteModel, Var, Constraint, Objective, minimize
from pyomo.opt import SolverFactory

model = ConcreteModel()
model.var = Var(bounds=(0, None))

def nonsense_rule(model):
    return model.var <= 5
model.nonsense_constraint = Constraint(rule=nonsense_rule)

def objective_rule(model):
    return model.var

model.objective = Objective(rule=objective_rule, sense=minimize)

opt = SolverFactory("glpk")
try:
    results = opt.solve(model)
    print("GLPK successfully installed")
except:
    print("GLPK not properly installed")
