# -*- coding: utf-8 -*-
#
#  Copyright 2018-2020 Ramil Nugmanov <nougmanoff@protonmail.com>
#  This file is part of CIMtools.
#
#  CIMtools is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
from itertools import compress
from pandas import DataFrame
from ..base import CIMtoolsTransformerMixin
from ..exceptions import ConfigurationError


class SolventVectorizer(CIMtoolsTransformerMixin):
    def __init__(self, polarizability_form1=True, polarizability_form2=True, permettivity_form1=True,
                 permettivity_form2=True, permettivity_form3=True, permettivity_form4=True,
                 permettivity_polarizability=True, alpha_kamlet_taft=True, beta_kamlet_taft=True, pi_kamlet_taft=True,
                 spp_katalan=True, sb_katalan=True, sa_katalan=True):
        self.polarizability_form1 = polarizability_form1
        self.polarizability_form2 = polarizability_form2
        self.permettivity_form1 = permettivity_form1
        self.permettivity_form2 = permettivity_form2
        self.permettivity_form3 = permettivity_form3
        self.permettivity_form4 = permettivity_form4
        self.permettivity_polarizability = permettivity_polarizability
        self.alpha_kamlet_taft = alpha_kamlet_taft
        self.beta_kamlet_taft = beta_kamlet_taft
        self.pi_kamlet_taft = pi_kamlet_taft
        self.spp_katalan = spp_katalan
        self.sb_katalan = sb_katalan
        self.sa_katalan = sa_katalan
        self.__prepare_header()

    def __getstate__(self):
        return {k: v for k, v in super().__getstate__().items() if not k.startswith('_SolventVectorizer__')}

    def __setstate__(self, state):
        if not state:  # < 4.0.5 reverse compatibility
            state = {'polarizability_form1': True, 'polarizability_form2': True, 'permettivity_form1': True,
                     'permettivity_form2': True, 'permettivity_form3': True, 'permettivity_form4': True,
                     'permettivity_polarizability': True, 'alpha_kamlet_taft': True, 'beta_kamlet_taft': True,
                     'pi_kamlet_taft': True, 'spp_katalan': True, 'sb_katalan': True, 'sa_katalan': True}
        super().__setstate__(state)
        self.__prepare_header()

    def set_params(self, **params):
        super().set_params(**params)
        self.__prepare_header()

    def __prepare_header(self):
        header = []
        index = []
        if self.polarizability_form1:
            header.append('Polarizability (form1)')
            index.append(True)
        else:
            index.append(False)
        if self.polarizability_form2:
            header.append('Polarizability (form2)')
            index.append(True)
        else:
            index.append(False)
        if self.permettivity_form1:
            header.append('Permettivity (form1)')
            index.append(True)
        else:
            index.append(False)
        if self.permettivity_form2:
            header.append('Permettivity (form2)')
            index.append(True)
        else:
            index.append(False)
        if self.permettivity_form3:
            header.append('Permettivity (form3)')
            index.append(True)
        else:
            index.append(False)
        if self.permettivity_form4:
            header.append('Permettivity (form4)')
            index.append(True)
        else:
            index.append(False)
        if self.permettivity_polarizability:
            header.append('Permettivity-Polarizability')
            index.append(True)
        else:
            index.append(False)
        if self.alpha_kamlet_taft:
            header.append('alpha Kamlet-Taft')
            index.append(True)
        else:
            index.append(False)
        if self.beta_kamlet_taft:
            header.append('beta Kamlet-Taft')
            index.append(True)
        else:
            index.append(False)
        if self.pi_kamlet_taft:
            header.append('pi Kamlet-Taft')
            index.append(True)
        else:
            index.append(False)
        if self.spp_katalan:
            header.append('SPP Katalan')
            index.append(True)
        else:
            index.append(False)
        if self.sb_katalan:
            header.append('SB Katalan')
            index.append(True)
        else:
            index.append(False)
        if self.sa_katalan:
            header.append('SA Katalan')
            index.append(True)
        else:
            index.append(False)

        if not header:
            raise ConfigurationError('required at least one parameter')
        self.__header = header
        self.__index = index

    def get_feature_names(self):
        """Get feature names.

        Returns
        -------
        feature_names : list of strings
            Names of the features produced by transform.
        """
        return self.__header

    def transform(self, x):
        x = super().transform(x)
        return DataFrame([compress(described_solvents[x], self.__index) for x in x], columns=self.__header)

    _dtype = str


described_solvents = dict((
    ('1-phenylethan-1-one',   (0.31,    0.237,    0.845,    0.943,    0.458,    0.891,    0.109,    0.04,    0.49,    0.9,    0.9,    0.37,    0.04,    475,    293)),
    ('1,2-dichloroethane',   (0.266,    0.21,    0.757,    0.903,    0.431,    0.824,    0.091,    0.0,    0.1,    0.81,    0.89,    0.13,    0.03,    356.5,    237.5)),
    ('1,2-dimethoxyethane',   (0.23,    0.19,    0.67,    0.86,    0.4,    0.76,    0.08,    0.0,    0.41,    0.53,    0.79,    0.64,    0.0,    358,    215)),
    ('propane-1,2,3-triol',   (0.28,    0.22,    0.94,    0.98,    0.48,    0.96,    0.11,    1.21,    0.51,    0.62,    0.95,    0.31,    0.65,    563,    291.2)),
    ('1,3-dimethylbenzene',   (0.293,    0.226,    0.318,    0.583,    0.241,    0.412,    0.055,    0.0,    0.11,    0.47,    0.62,    0.16,    0.0,    412.1,    225.2)),
    ('1,3,5‐trimethylbenzene',   (0.294,    0.227,    0.318,    0.583,    0.241,    0.412,    0.055,    0.0,    0.13,    0.41,    0.58,    0.19,    0.0,    437.7,    228.3)),
    ('1,4-dioxane',   (0.253,    0.202,    0.287,    0.548,    0.223,    0.377,    0.045,    0.0,    0.37,    0.49,    0.7,    0.44,    0.0,    374.5,    284.8)),
    ('2-methylbutan-2-ol',   (0.245,    0.197,    0.614,    0.827,    0.381,    0.705,    0.075,    0.28,    0.93,    0.4,    0.83,    0.94,    0.1,    375.4,    263.9)),
    ('2-methylpropan-1-ol',   (0.24,    0.194,    0.84,    0.94,    0.456,    0.887,    0.088,    0.79,    0.84,    0.4,    0.83,    0.83,    0.31,    380.8,    165)),
    ('2-methylpropan-2-ol',   (0.234,    0.19,    0.793,    0.92,    0.442,    0.852,    0.084,    0.42,    0.93,    0.41,    0.83,    0.93,    0.15,    355.4,    298.4)),
    ('2,2,4-trimethylpentane',   (0.237,    0.191,    0.242,    0.49,    0.195,    0.324,    0.037,    0.0,    0.0,    0.04,    0.53,    0.04,    0.0,    372.2,    165.7)),
    ('3-methylbutan-1-ol',   (0.245,    0.197,    0.825,    0.934,    0.452,    0.876,    0.089,    0.84,    0.86,    0.4,    0.81,    0.86,    0.32,    404.1,    155.8)),
    ('acetic acid',   (0.226,    0.184,    0.632,    0.837,    0.387,    0.72,    0.071,    1.12,    0.45,    0.64,    0.78,    0.39,    0.69,    390.9,    289.6)),
    ('acetonitrile',   (0.21,    0.174,    0.921,    0.972,    0.479,    0.946,    0.083,    0.19,    0.4,    0.66,    0.9,    0.29,    0.04,    354.6,    229.2)),
    ('benzene',   (0.293,    0.227,    0.297,    0.559,    0.229,    0.388,    0.052,    0.0,    0.1,    0.55,    0.67,    0.12,    0.0,    353,    278.5)),
    ('benzenecarbonitrile',   (0.31,    0.24,    0.89,    0.96,    0.47,    0.93,    0.11,    0.0,    0.37,    0.9,    0.96,    0.28,    0.05,    464.1,    260.3)),
    ('bromobenzene',   (0.323,    0.244,    0.595,    0.815,    0.373,    0.688,    0.091,    0.0,    0.06,    0.79,    0.82,    0.19,    0.0,    429,    242.4)),
    ('butan-1-ol',   (0.241,    0.194,    0.846,    0.943,    0.458,    0.892,    0.089,    0.84,    0.84,    0.47,    0.84,    0.81,    0.34,    390.85,    183.2)),
    ('butan-2-ol',   (0.24,    0.193,    0.838,    0.94,    0.456,    0.886,    0.088,    0.69,    0.8,    0.4,    0.84,    0.89,    0.22,    372.5,    158.3)),
    ('butan-2-one',   (0.23,    0.187,    0.851,    0.945,    0.46,    0.895,    0.086,    0.06,    0.48,    0.6,    0.88,    0.52,    0.0,    352.5,    186.4)),
    ('chlorobenzene',   (0.304,    0.233,    0.606,    0.822,    0.377,    0.698,    0.088,    0.0,    0.07,    0.68,    0.82,    0.18,    0.0,    141.3,    227.8)),
    ('cyclohexane',   (0.255,    0.203,    0.254,    0.505,    0.202,    0.338,    0.041,    0.0,    0.0,    0.0,    0.56,    0.07,    0.0,    353.7,    279.6)),
    ('dichloromethane',   (0.254,    0.202,    0.726,    0.888,    0.42,    0.799,    0.085,    0.13,    0.1,    0.82,    0.88,    0.18,    0.04,    313,    177.9)),
    ('ethane-1,2-diol',   (0.259,    0.205,    0.924,    0.973,    0.48,    0.948,    0.099,    0.9,    0.52,    0.92,    0.93,    0.53,    0.72,    470.3,    260)),
    ('ethanol',   (0.22,    0.181,    0.887,    0.959,    0.47,    0.922,    0.085,    0.86,    0.75,    0.54,    0.85,    0.66,    0.4,    351.2,    158.9)),
    ('ethoxybenzene',   (0.3,    0.23,    0.52,    0.76,    0.34,    0.62,    0.08,    0.0,    0.3,    0.69,    0.74,    0.3,    0.0,    442.8,    243.5)),
    ('ethoxyethane',   (0.215,    0.177,    0.516,    0.762,    0.34,    0.615,    0.06,    0.0,    0.47,    0.24,    0.69,    0.56,    0.0,    307.6,    156.7)),
    ('ethyl acetate',   (0.228,    0.19,    0.63,    0.83,    0.38,    0.72,    0.071,    0.0,    0.45,    0.55,    0.8,    0.54,    0.0,    350.1,    189.4)),
    ('ethyl benzoate',   (0.297,    0.229,    0.625,    0.833,    0.385,    0.714,    0.088,    0.0,    0.41,    0.74,    0.84,    0.42,    0.0,    485,    239)),
    ('formamide',   (0.267,    0.211,    0.973,    0.991,    0.493,    0.982,    0.104,    0.71,    0.48,    0.97,    0.83,    0.41,    0.55,    493,    275.55)),
    ('deuterium oxide',   (0.203,    0.169,    0.963,    0.987,    0.49,    0.975,    0.083,    1.17,    0.47,    1.09,    0.96,    0.44,    1.06,    374.42,    276.81)),
    ('heptan-1-ol',   (0.255,    0.203,    0.775,    0.912,    0.437,    0.838,    0.089,    0.79,    0.82,    0.4,    0.8,    0.91,    0.3,    449.4,    239)),
    ('heptane',   (0.236,    0.19,    0.235,    0.479,    0.19,    0.315,    0.036,    0.0,    0.0,    -0.08,    0.53,    0.08,    0.0,    371.5,    182.4)),
    ('hexamethylphosphoramide',   (0.277,    0.217,    0.906,    0.967,    0.475,    0.935,    0.103,    0.0,    1.05,    0.87,    0.93,    0.81,    0.0,    505.5,    280.2)),
    ('hexan-1-ol',   (0.251,    0.201,    0.804,    0.925,    0.446,    0.86,    0.089,    0.8,    0.84,    0.4,    0.81,    0.88,    0.32,    430.6,    228.4)),
    ('hexane',   (0.227,    0.185,    0.227,    0.468,    0.185,    0.306,    0.034,    0.0,    0.0,    -0.11,    0.52,    0.06,    0.0,    341.7,    177.7)),
    ('methanedithione',   (0.355,    0.262,    0.348,    0.615,    0.258,    0.444,    0.068,    0.0,    0.07,    0.61,    0.59,    0.1,    0.0,    319,    161.5)),
    ('methanesulfinylmethane',   (0.283,    0.22,    0.938,    0.978,    0.484,    0.958,    0.107,    0.0,    0.76,    1.0,    1.0,    0.65,    0.07,    462,    291.5)),
    ('methanol',   (0.202,    0.168,    0.913,    0.969,    0.477,    0.941,    0.08,    0.98,    0.66,    0.6,    0.86,    0.55,    0.61,    337.7,    175.4)),
    ('methoxybenzene',   (0.3,    0.23,    0.52,    0.77,    0.34,    0.62,    0.08,    0.0,    0.32,    0.73,    0.82,    0.3,    0.08,    426.7,    235.5)),
    ('N,N-dimethylacetamide',   (0.26,    0.21,    0.92,    0.97,    0.48,    0.95,    0.1,    0.0,    0.76,    0.88,    0.97,    0.61,    0.03,    438,    253)),
    ('N,N-dimethylformamide',   (0.257,    0.205,    0.923,    0.973,    0.48,    0.947,    0.098,    0.0,    0.69,    0.88,    0.95,    0.61,    0.03,    426,    212.6)),
    ('nitrobenzene',   (0.319,    0.242,    0.918,    0.971,    0.479,    0.944,    0.116,    0.0,    0.3,    0.86,    0.97,    0.24,    0.06,    483.8,    278.7)),
    ('nitromethane',   (0.231,    0.188,    0.921,    0.972,    0.479,    0.946,    0.09,    0.22,    0.06,    0.75,    0.91,    0.24,    0.08,    374.1,    244.5)),
    ('octan-1-ol',   (0.257,    0.204,    0.757,    0.903,    0.431,    0.824,    0.088,    0.77,    0.81,    0.4,    0.79,    0.92,    0.3,    468.1,    257.5)),
    ('oxolan-2-one',   (0.26,    0.207,    0.927,    0.974,    0.481,    0.95,    0.099,    0.0,    0.49,    0.85,    0.99,    0.4,    0.06,    477,    229.7)),
    ('1,4-epoxybutane',   (0.245,    0.197,    0.687,    0.868,    0.407,    0.767,    0.08,    0.0,    0.55,    0.55,    0.84,    0.59,    0.0,    338,    164.7)),
    ('1,4-dimethylbenzene',   (0.29,    0.226,    0.302,    0.565,    0.232,    0.394,    0.052,    0.0,    0.12,    0.43,    0.62,    0.16,    0.0,    411.3,    286.2)),
    ('pentan-1-ol',   (0.247,    0.198,    0.811,    0.928,    0.448,    0.866,    0.089,    0.84,    0.86,    0.4,    0.82,    0.86,    0.32,    410.9,    194.1)),
    ('phenylmethanol',   (0.313,    0.238,    0.796,    0.921,    0.443,    0.854,    0.106,    0.6,    0.52,    0.98,    0.89,    0.46,    0.41,    478.3,    257.8)),
    ('piperidine',   (0.27,    0.213,    0.62,    0.83,    0.383,    0.71,    0.081,    0.0,    1.04,    0.3,    0.74,    0.93,    0.0,    379,    266)),
    ('propan-1-ol',   (0.234,    0.189,    0.866,    0.951,    0.464,    0.907,    0.088,    0.84,    0.9,    0.52,    0.85,    0.78,    0.37,    370.2,    146.9)),
    ('propan-2-ol',   (0.229,    0.186,    0.863,    0.95,    0.463,    0.904,    0.086,    0.76,    0.84,    0.48,    0.85,    0.83,    0.28,    355.9,    183.5)),
    ('propan-2-one',   (0.218,    0.179,    0.867,    0.951,    0.464,    0.907,    0.083,    0.08,    0.48,    0.62,    0.88,    0.48,    0.0,    328.75,    177.45)),
    ('propanenitrile',   (0.222,    0.182,    0.901,    0.965,    0.474,    0.932,    0.086,    0.0,    0.37,    0.64,    0.88,    0.37,    0.03,    370.1,    180.2)),
    ('pyridine',   (0.298,    0.229,    0.799,    0.923,    0.444,    0.856,    0.102,    0.0,    0.64,    0.87,    0.92,    0.58,    0.03,    388.2,    231.4)),
    ('tetrachloromethane',   (0.272,    0.214,    0.292,    0.554,    0.226,    0.383,    0.048,    0.0,    0.1,    0.21,    0.63,    0.04,    0.0,    349.8,    250)),
    ('tetrahydrothiophene 1,1-dioxide',   (0.285,    0.222,    0.934,    0.977,    0.483,    0.955,    0.107,    0.0,    0.39,    0.9,    1.0,    0.37,    0.05,    558,    300.6)),
    ('toluene',   (0.291,    0.226,    0.315,    0.58,    0.24,    0.408,    0.054,    0.0,    0.11,    0.49,    0.66,    0.13,    0.0,    383.6,    178.1)),
    ('trichloromethane',   (0.265,    0.209,    0.565,    0.796,    0.361,    0.66,    0.076,    0.2,    0.1,    0.58,    0.79,    0.07,    0.05,    334.1,    209.4)),
    ('water',   (0.205,    0.17,    0.963,    0.987,    0.49,    0.975,    0.084,    1.17,    0.47,    1.09,    0.96,    0.03,    1.06,    373,    273))))


__all__ = ['SolventVectorizer']
