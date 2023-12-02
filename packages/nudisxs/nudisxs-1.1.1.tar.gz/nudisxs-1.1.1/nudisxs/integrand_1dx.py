import logging
#import cubepy
log = logging.getLogger('disxs')
logformat='[%(name)20s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)
log.setLevel(logging.getLevelName("INFO"))

from nudisxs.disxs import *
import vegas as vegas



class integrand_1dx(vegas.BatchIntegrand):
    def __init__(self,model = 'CT10nlo'):
        self.dis = disxs()
        self.dis.init_pdf(model)

    def __call__(self,y):
        f = np.zeros(y.shape[0])
        self.y_w = np.zeros(y.shape[0])
        self.y_w = self.y_w + self.y
        self.dis.xsdis_as_array(self.dis.enu, y[:], self.y_w, f, y.shape[0])
        return f
    
    def init_y(self,y):
        self.y = y

    def init_vegas_integrator(self):
        self.integrator = vegas.Integrator([[0.0,1.0]], nhcube_batch=2000, sync_ran=False)
        log.info('init_vegas_integrator')

    def calculate(self,enu,y):
        self.dis.init_enu(enu)
        self.init_y(y)
        result = self.integrator(self,nitn=3)
        return result.mean*self.dis.normfactor

    def calculate_as_array(self,enu,y):
        import time as time
        xsec = np.zeros([len(enu),len(y)])
        self.init_vegas_integrator()
        for i in range(len(enu)):
            tt = time.time()
            self.dis.init_enu(enu[i])
            for j in range(len(y)):
                self.init_y(y[j])
                result = self.integrator(self,nitn=3)
                xsec[i,j] = result.mean*self.dis.normfactor
            print(i,time.time()-tt)
        return xsec 

'''
a = integrand_1dx()
a.init_vegas_integrator()
a.dis.init_neutrino(14)
a.dis.init_current('cc')
a.dis.init_target(2212)
e = np.logspace(1,15,num=15)
y = np.logspace(-16,0,num = 170)
xsec = a.calculate_as_array(e,y)
import matplotlib.pyplot as plt
fig = plt.figure(figsize = (18,12))
for i in range(len(e)):
    plt.plot(y,xsec[i],label = r'$E_{\nu} = $'+str(e[i])+'GeV')
plt.xlabel(r'$y_{Bj}$')
plt.ylabel(r'$\frac{d\sigma}{dy},cm^{-2}$')
plt.grid(True)
plt.legend()
plt.xscale('log')
#plt.yscale('log')
plt.show()
'''
