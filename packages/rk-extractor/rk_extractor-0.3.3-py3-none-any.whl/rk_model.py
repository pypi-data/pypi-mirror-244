import zfit

from rkex_model import model

from builder    import builder as cb_builder

#---------------------------------------------------------------
class rk_model(model):
    def _get_dset_trig(self, preffix):
        [chan, dset, kind, _ ] = preffix.split('_')
    
        if   chan == 'mm':
            trig = 'MTOS'
        elif chan == 'ee' and kind == 'TOS': 
            trig = 'ETOS'
        elif chan == 'ee' and kind == 'TIS': 
            trig = 'GTIS'
        else:
            log.error(f'Invalid channel: {chan}')
            raise ValueError
    
        return dset, trig
    #---------------------------------------------------------------
    def _get_combinatorial(self, preffix, nent):
        dset, trig    = self._get_dset_trig(preffix) 
        obj           = cb_builder(dset=dset, trigger=trig, vers='v5', q2bin='high', const=False)
        obj.cache_path= './cb_buider.tar.gz'
        cmb,l_cns     = obj.get_pdf(obs=self._obs, preffix=f'cb_{preffix}') 

        ncb           = zfit.Parameter(f'ncb_{preffix}', 10 * nent, 0, 100000)
        cbkg          = cmb.create_extended(ncb)

        return cbkg
    #---------------------------------------------------------------
    def _get_signal(self, preffix, mu=None, sg=None, nent=None):
        mu, sg = self._get_peak_pars(preffix, mu=mu, sg=sg)

        gauss  = zfit.pdf.Gauss(obs=self._obs, mu=mu, sigma=sg)
        nsg    = zfit.Parameter(f'nsg_{preffix}', nent, 0, 100000)
        esig   = gauss.create_extended(nsg)

        return esig
    #---------------------------------------------------------------
    def _get_pdf(self, preffix='', mu=None, sg=None, nent=None):
        preffix= f'{preffix}_{self._preffix}'

        cbkg   = self._get_combinatorial(preffix, nent)
        esig   = self._get_signal(preffix, mu=mu, sg=sg, nent=nent)
        pdf    = zfit.pdf.SumPDF([esig, cbkg]) 

        return pdf 
#---------------------------------------------------------------

