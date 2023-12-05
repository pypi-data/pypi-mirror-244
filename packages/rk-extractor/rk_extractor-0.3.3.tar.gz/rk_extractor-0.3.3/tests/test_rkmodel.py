import ROOT
import zfit

from rk_model   import rk_model
from mc_reader  import mc_reader as mc_rdr
from np_reader  import np_reader as np_rdr
from cs_reader  import cs_reader as cs_rdr

import rk.utilities as rkut
import pytest
import pprint
import os

#-----------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#----------------------------------------------------
def rename_keys(d_data, use_txs=True):
    d_rename = {}
    if use_txs:
        d_rename[  'r1_TOS'] = d_data['d1']
        d_rename[  'r1_TIS'] = d_data['d1']

        d_rename['r2p1_TOS'] = d_data['d2']
        d_rename['r2p1_TIS'] = d_data['d2']

        d_rename['2017_TOS'] = d_data['d3']
        d_rename['2017_TIS'] = d_data['d3']

        d_rename['2018_TOS'] = d_data['d4']
        d_rename['2018_TIS'] = d_data['d4']
    else:
        d_rename[  'r1']     = d_data['d1']
        d_rename['r2p1']     = d_data['d2']
        d_rename['2017']     = d_data['d3']
        d_rename['2018']     = d_data['d4']

    return d_rename
#-----------------------------
def skip_test():
    try:
        uname = os.environ['USER']
    except:
        pytest.skip()

    if uname in ['angelc', 'campoverde']:
        return

    pytest.skip()
#----------------------
def test_simple():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e4, 'd2' :          1e4, 'd3' :          1e4, 'd4' :          1e4}
    d_mcmu= {'d1' : (5000, 4900), 'd2' : (5100, 4900), 'd3' : (5100, 4800), 'd4' : (5200, 5100)}
    d_mcsg= {'d1' :      (2,  4), 'd2' :     (1, 1.8), 'd3' :       (2, 3), 'd4' :       (3, 4)}

    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)
    d_mcmu=rename_keys(d_mcmu)
    d_mcsg=rename_keys(d_mcsg)

    mod         = rk_model(preffix='simple', d_eff=d_eff, d_mcmu=d_mcmu, d_mcsg=d_mcsg, d_nent=d_nent)
    mod.out_dir = 'tests/rkmodel/simple' 
    d_dat       = mod.get_data()
    d_mod       = mod.get_model()

    delete_all_pars()
#----------------------
def main():
    test_simple()
#----------------------
if __name__ == '__main__':
    main()

