import logging
#import cubepy
log = logging.getLogger('disxs')
logformat='[%(name)20s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)
log.setLevel(logging.getLevelName("INFO"))

from nudisxs.disxs import *
import vegas as vegas



class integrand_1dy(vegas.BatchIntegrand):
    def __init__(self,model = 'CT10nlo'):
        self.dis = disxs()
        self.dis.init_pdf(model)

    def __call__(self,x):
        f = np.zeros(x.shape[0])
        self.x_w = np.zeros(x.shape[0])
        self.x_w = self.x_w + self.x
        self.dis.xsdis_as_array(self.dis.enu, self.x_w, x[:], f, x.shape[0])
        return f
    
    def init_x(self,x):
        self.x = x

    def init_vegas_integrator(self):
        self.integrator = vegas.Integrator([[0.0,1.0]], nhcube_batch=2000, sync_ran=False)
        log.info('init_vegas_integrator')

    def calculate(self,enu,x):
        self.dis.init_enu(enu)
        self.init_x(x)
        result = self.integrator(self,nitn=3)
        return result.mean*self.dis.normfactor

    def calculate_as_array(self,enu,x):
        import time as time
        xsec = np.zeros([len(enu),len(x)])
        a.init_vegas_integrator()
        for i in range(len(enu)):
            tt = time.time()
            self.dis.init_enu(enu[i])
            for j in range(len(x)):
                self.init_x(x[j])
                result = self.integrator(self,nitn=3)
                xsec[i,j] = result.mean*self.dis.normfactor
            print(i,time.time()-tt)
        return xsec 

'''
a = integrand_1dy()
a.init_vegas_integrator()
a.dis.init_neutrino(14)
a.dis.init_current('cc')
a.dis.init_target(2212)
e = np.logspace(1,5,num=5)
y = np.logspace(-6,0,num = 1000)
xsec = a.calculate_as_array(e,y)
import matplotlib.pyplot as plt
fig = plt.figure(figsize = (18,12))
for i in range(len(e)):
    plt.plot(y,xsec[i],label = r'$E_{\nu} = $'+str(e[i])+'GeV')
plt.xlabel(r'$y_{Bj}$')
plt.ylabel(r'$\frac{d\sigma}{dx},cm^{-2}$')
plt.grid(True)
plt.legend()
plt.xscale('log')
#plt.yscale('log')
plt.show()
'''
