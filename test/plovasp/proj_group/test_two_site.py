
import os
import rpath
_rpath = os.path.dirname(rpath.__file__) + '/'

import numpy as np
from pytriqs.applications.dft.converters.plovasp.vaspio import VaspData
from pytriqs.applications.dft.converters.plovasp.elstruct import ElectronicStructure
from pytriqs.applications.dft.converters.plovasp.inpconf import ConfigParameters
from pytriqs.applications.dft.converters.plovasp.proj_shell import ProjectorShell
from pytriqs.applications.dft.converters.plovasp.proj_group import ProjectorGroup
import mytest

################################################################################
#
# TestProjectorGroup
#
################################################################################
class TestProjectorGroupTwoSite(mytest.MyTestCase):
    """
    Tests for a two-site problem.

    Class:

    ProjectorGroup(sh_pars, proj_raw)

    Scenarios:
    - **test** that orthogonalization with NORMION = False is correct
    - **test** that orthogonalization with NORMION = True is correct
    """
    def setUp(self):
        conf_file = _rpath + 'example_two_site.cfg'
        self.pars = ConfigParameters(conf_file)
        self.pars.parse_input()
        vasp_data = VaspData(_rpath + 'two_site/')
        self.el_struct = ElectronicStructure(vasp_data)

        efermi = self.el_struct.efermi
        self.eigvals = self.el_struct.eigvals - efermi

        self.proj_sh = ProjectorShell(self.pars.shells[0], vasp_data.plocar.plo, vasp_data.plocar.proj_params, 0)
        self.proj_gr = ProjectorGroup(self.pars.groups[0], [self.proj_sh], self.eigvals)

# Scenario 1
    def test_ortho(self):
        self.proj_gr.normion = False
        self.proj_gr.orthogonalize()

        dens_mat, overl = self.proj_sh.density_matrix(self.el_struct)

        testout = _rpath + 'projortho_2site.out.test'
        with open(testout, 'wt') as f:
            f.write("density matrix: %s\n"%(dens_mat))
            f.write("overlap matrix: %s\n"%(overl))

        self.assertEqual(overl[0, 0, ...], np.eye(5))
        self.assertEqual(overl[0, 1, ...], np.eye(5))

        expected_file = _rpath + 'projortho_2site.out'
        self.assertFileEqual(testout, expected_file)

# Scenario 2
    def test_ortho_normion(self):
        self.proj_gr.normion = True
        self.proj_gr.orthogonalize()

        dens_mat, overl = self.proj_sh.density_matrix(self.el_struct)

        testout = _rpath + 'projortho_normion.out.test'
        with open(testout, 'wt') as f:
            f.write("density matrix: %s\n"%(dens_mat))
            f.write("overlap matrix: %s\n"%(overl))

        self.assertEqual(overl[0, 0, ...], np.eye(5))
        self.assertEqual(overl[0, 1, ...], np.eye(5))

        expected_file = _rpath + 'projortho_normion.out'
        self.assertFileEqual(testout, expected_file)


