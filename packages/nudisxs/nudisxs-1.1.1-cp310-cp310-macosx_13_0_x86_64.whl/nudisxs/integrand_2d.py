import logging
#import cubepy
log = logging.getLogger('disxs')
logformat='[%(name)20s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)
log.setLevel(logging.getLevelName("INFO"))

from nudisxs.disxs import *
import vegas as vegas



class integrand_2dxy(vegas.BatchIntegrand):
    def __init__(self,model = 'CT10nlo'):
        self.dis = disxs()
        self.dis.init_pdf(model)


    def __call__(self,x):
        f = np.zeros(x.shape[0])
        self.dis.xsdis_as_array(self.dis.enu,x[:,0],x[:,1],f,x.shape[0])
        return f

    def init_vegas_integrator(self,opts):
        self.integrator = vegas.Integrator([[0.0,1.0], [0.0,1.0]],neval = opts.vegas_neval, nhcube_batch=opts.vegas_neval, sync_ran=False)
        log.info('init_vegas_integrator')

    def calculate(self,enu):
        self.dis.init_enu(enu)
        result = self.integrator(self,nitn=10)
        return result.mean*self.dis.normfactor
    

    def calculate1(self,enu):
        self.dis.init_enu(enu)
        result = self.integrator(self,nitn=10)
        return result



#a = integrand_2dxy()
#a.init_vegas_integrator()
#a.dis.init_neutrino(14)
#a.dis.init_current('cc')
#a.dis.init_target('proton')
#print(a.calculate(100))
