from AHU.air_humide import air_humide


from AHU.AirPort.AirPort import AirPort

class Object:
    def __init__(self):
        self.Inlet=AirPort() 
        self.Outlet=AirPort()
        self.P=0
        self.P_drop=0
        self.id=2
        # données air neuf
        self.T_in=0
        self.hi=0
        self.w_in=12
        self.F=0
        self.F_dry=0
        
        #consigne
        self.T_out_target=20
        # calcul Outlet Coil
        self.ho=0
        self.Q_th=12
        self.RH_out=0
        
      
        
    def calculate(self):
        
          #connecteur  
        self.Outlet.P=self.Inlet.P-self.P_drop
      
        self.w_in=self.Inlet.w
        self.P=self.Inlet.P
        self.hi=self.Inlet.h
        self.F=self.Inlet.F
        
        self.T_in=air_humide.Temperature(self.hi,self.w_in)
        

        self.ho=air_humide.Enthalpie(self.T_out_target,self.w_in)
          #  print("ho=",self.ho)
        self.F_dry=(self.F)/(1+(self.w_in/1000))
        print("self.F_dry=",self.F_dry,"self.Inlet.P=",self.Inlet.P,"self.F=",self.F)
        self.Q_th=(self.ho-self.hi)*self.F_dry
          # print("self.Q_th=",self.Q_th)
        self.RH_out=air_humide.HR(air_humide.func_Pv_sat(self.T_out_target),self.w_in,self.Outlet.P) #parametrer la pression
          # print("self.RH_out=",self.RH_out)
        
       
            
            
            

        
        #connecteur   
      
          
        self.Outlet.w=self.Inlet.w
        
        self.Outlet.h=self.ho
        self.Outlet.F=self.Inlet.F #à corriger
#
       


