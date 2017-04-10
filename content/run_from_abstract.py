from abstract_trnsprt import model
from pyomo.opt import SolverFactory

instance = model.create_instance(filename='data/trnsprt/trnsprt.dat')

opt = SolverFactory("glpk")
results = opt.solve(instance)
results.write()