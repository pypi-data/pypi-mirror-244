import pathlib
import os
import openmc
import math

import CAD_to_OpenMC.assembly as ab

from tests.OMC_DAGMC_run import DAGMC_template
from tests.harnessRun import HarnessRun

class OMC_DAGMC_harness(HarnessRun):
  def __init__(self, step):
    self.path = pathlib.Path(step)
    self.h5m = self.path.with_suffix('.h5m')
    self.nuclear_lib = pathlib.Path('tests/nuclear_data_testlib/cross_sections.xml').absolute()
    self.aa = ab.Assembly([str(self.path)], verbose = 2)
    self.tt = DAGMC_template(self.h5m)

  def run(self):
    self.aa.run(backend='stl2', merge = True, h5m_filename = self.h5m)
    assert self.h5m.exists()
    self.tt.run()
    assert pathlib.Path('statepoint.5.h5').exists()
    self.tt.check_results()
    self.tt.cleanup()
    self.cleanup()

def test_h5m_neutronics_p1():
  o = OMC_DAGMC_harness('examples/pincell1.step')
  openmc.config['cross_sections']=str(o.nuclear_lib)
  o.tt.results={'keff':(0.08651,0.00446)}
  o.run()

def test_h5m_neutronics_p2():
  o = OMC_DAGMC_harness('examples/pincell2.step')
  openmc.config['cross_sections']=str(o.nuclear_lib)
  o.tt.results={'keff':(0.08735,0.00802)}
  o.run()

def test_h5m_neutronics_tors():
  o = OMC_DAGMC_harness('examples/toroids.step')
  # override source spatial distribution
  o.tt.settings.source.space=openmc.stats.CylindricalIndependent(
    openmc.stats.Discrete([100,85,77.5],[1.0/3.0,1.0/3.0, 1.0/3.0]), openmc.stats.Uniform(0.0,2.0*math.pi), openmc.stats.Discrete([0.0],[1.0])
  )
  openmc.config['cross_sections']=str(o.nuclear_lib)
  o.tt.results={'keff':(1.16942,0.47448)}
  o.run()

def test_h5m_neutronics_spheroids():
  o = OMC_DAGMC_harness('examples/spheroids.step')
  openmc.config['cross_sections']=str(o.nuclear_lib)
  o.run()

def test_h5m_neutronics_ellipsoids():
  o = OMC_DAGMC_harness('examples/oblate_ellipsoids.step')
  openmc.config['cross_sections']=str(o.nuclear_lib)
  o.tt.results={'keff':(1.12592,0.03893)}
  o.run()

if __name__=='__main__':
  test_h5m_neutronics_p1()
  test_h5m_neutronics_p2()
  test_h5m_neutronics_tors()
  test_h5m_neutronics_spheroids()
  test_h5m_neutronics_ellipsoids()
