# -*- coding: utf-8 -*-

# configure logging for the library with a null handler (nothing is printed by default). See
# http://docs.pthon-guide.org/en/latest/writing/logging/

"""Top-level package for SDV."""

# This package is extended from ctgan and SDV
# https://github.com/sdv-dev/SDV
# https://github.com/sdv-dev/CTGAN
# Modified the conditional matrix and cost functions
# The main changes are in ctgan/synthesizers/ctgan.py ../data_sampler.py ../data_transformer.py
__author__ = 'Chang Sun'
__email__ = 'chang.sun@maastrichtuniversity.nl'
__version__ = '0.0.6'


from dp_cgans import constraints, metadata
# from dp_cgans.metadata import Table
from dp_cgans.dp_cgan_init import DP_CGAN
from dp_cgans.synthesizers.dp_cgan import DPCGANSynthesizer

__all__ = (
    'constraints',
    'metadata',
    # 'Table',
    'DP_CGAN',
    'RDF_to_Tabular',
    'DPCGANSynthesizer'
)