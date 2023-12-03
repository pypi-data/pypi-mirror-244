# =============================================================================
# Chiller Model (Evaporator + Compressor + Desuperheater + Condenser + Expansion_Valve)
# =============================================================================

import CoolProp.CoolProp as CP
from ThermodynamicCycles.Evaporator import Evaporator
from ThermodynamicCycles.Compressor import Compressor
from ThermodynamicCycles.Desuperheater import Desuperheater
from ThermodynamicCycles.Expansion_Valve import Expansion_Valve
from ThermodynamicCycles.Condenser import Condenser
from ThermodynamicCycles.Connect import Fluid_connect

from ThermodynamicCycles import Temperature_Entropy_Chart

class Object:
    def __init__(self, fluid='R134a', evap_params=None, comp_params=None, cond_params=None):
        # Initialize chiller components
        self.EVAP = Evaporator.Object()
        self.COMP = Compressor.Object()
        self.DESURCH = Desuperheater.Object()
        self.COND = Condenser.Object()
        self.DET = Expansion_Valve.Object()

        # Set fluid for all components
        self.fluid = fluid
        self.EVAP.fluid = self.fluid
        self.COMP.fluid = self.fluid
        self.DESURCH.fluid = self.fluid
        self.COND.fluid = self.fluid
        self.DET.fluid = self.fluid

        # Set parameters for each component
        self.set_evaporator_parameters(evap_params)
        self.set_compressor_parameters(comp_params)
        self.set_condenser_parameters(cond_params)

        self.points=[]

    def set_evaporator_parameters(self, params):
        if params:
            self.EVAP.Ti_degC= params.get('Ti_degC', 5)
            self.EVAP.surchauff = params.get('surchauff', 2)
            self.EVAP.Inlet.F = params.get('F', 1)
            

    def set_compressor_parameters(self, params):
        if params:
            self.COMP.Tcond_degC = params.get('Tcond_degC', 40)
            self.COMP.eta_is = params.get('eta_is', 0.8)
            self.COMP.Tdischarge_target = params.get('Tdischarge_target', 80)
            if 'Qcomp' in params:
                self.COMP.Qcomp = params['Qcomp']

    def set_condenser_parameters(self, params):
        if params:
            self.COND.subcooling = params.get('subcooling', 2)

    def calculate_cycle(self):
        # Calculation algorithm
        self.EVAP.Inlet.h = CP.PropsSI('H', 'P', 1 * 1e5, 'T', 40 + 273.15, self.fluid)
        self.EVAP.calculate() 
        Fluid_connect(self.COMP.Inlet, self.EVAP.Outlet)
        self.COMP.calculate()
        Fluid_connect(self.DESURCH.Inlet, self.COMP.Outlet)
        self.DESURCH.calculate()
        Fluid_connect(self.COND.Inlet, self.DESURCH.Outlet)
        self.COND.calculate()
        Fluid_connect(self.DET.Inlet, self.COND.Outlet)
        Fluid_connect(self.DET.Outlet, self.EVAP.Inlet)
        self.DET.calculate()
        Fluid_connect(self.EVAP.Inlet, self.DET.Outlet)
        print("/////////////////////////////////",self.DET.Outlet.T-273.15)
        self.EVAP.calculate() # Recalculate evaporator

        self.points = [
            {"T": self.EVAP.Tsv - 273.15, "S": self.EVAP.Ssv},
            {"T": self.EVAP.Outlet.T - 273.15, "S": self.EVAP.Outlet.S},
            {"T": self.COMP.Outlet.T - 273.15, "S": self.COMP.Outlet.S},
            {"T": self.DESURCH.Outlet.T - 273.15, "S": self.DESURCH.Outlet.S},
            {"T": self.COND.Tsl- 273.15, "S": self.COND.Ssl},
            {"T": self.COND.Outlet.T - 273.15, "S": self.COND.Outlet.S},
            {"T": self.DET.df.loc['To(°C)', 'Expansion_Valve'], "S": self.DET.df.loc['So(kJ/kg-K)', 'Expansion_Valve']*1000},
            {"T": self.EVAP.Tsv - 273.15, "S": self.EVAP.Ssv}
        ]
      

    def calculate_performance(self):
        # Cycle performance
        EER = self.EVAP.Qevap / self.COMP.Qcomp
        QcondTot = self.COND.Qcond + self.DESURCH.Qdesurch
        COP = QcondTot / self.COMP.Qcomp
        return EER, QcondTot, COP

    def print_results(self):
        # Print Results
        print("COMPONENT DATAFRAMES:\n")
        print("Compressor:")
        print(self.COMP.df)
        print("\nEvaporator:")
        print(self.EVAP.df)
        print("\nDesuperheater:")
        print(self.DESURCH.df)
        print("\nCondenser:")
        print(self.COND.df)
        print("\nExpansion Valve:")
        print(self.DET.df)



    def plot_TS_diagram(self):
        # Create a Temperature-Entropy chart object
        chart = Temperature_Entropy_Chart.Object(self.fluid)

        print(self.DET.Outlet.T - 273.15,self.DET.Outlet.S)
        # Collect temperature and entropy data points from each component
        

        # Add points to the chart
        chart.add_points(self.points)

        # Display the chart
        chart.show(draw_arrows=True)

