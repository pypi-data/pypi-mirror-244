#! /usr/bin/env python

# SPDX-FileCopyrightText: Copyright 2021, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the license found in the LICENSE.txt file in the root
# directory of this source tree.


# =======
# Imports
# =======

import sys
import time
import numpy
from imate.sample_matrices import toeplitz
from imate import eigencount


# ==============
# relative error
# ==============

def relative_error(estimate, exact):
    """
    Compute the relative error of an estimate, in percent.
    """

    tol = 1e-15
    if numpy.abs(exact) < tol:
        if numpy.abs(estimate - exact) < tol:
            relative_error = 0.0
        else:
            relative_error = numpy.inf
    else:
        relative_error = numpy.abs((estimate - exact) / exact) * 100.0

    return relative_error


# =======================
# test eigencount methods
# =======================

def _test_eigencount_methods(K, matrix, gram, p, interval, assume_matrix):
    """
    Computes the eigencount of matrix ``K`` with multiple method.

    :param K: Square matrix.
    :type K: numpy.ndarray
    """

    # Settings
    min_num_samples = 100
    max_num_samples = 200
    lanczos_degree = 30
    error_rtol = 1e-2

    # Use eigenvalue method
    time10 = time.time()
    eigencount1 = eigencount(K, gram=gram, p=p, interval=interval,
                             method='eigenvalue', assume_matrix=assume_matrix,
                             non_zero_eig_fraction=0.95)
    time11 = time.time()

    # Use Stochastic Lanczos Quadrature method
    time20 = time.time()
    eigencount2 = eigencount(K, gram=gram, p=p, interval=interval,
                             method='slq', min_num_samples=min_num_samples,
                             max_num_samples=max_num_samples, orthogonalize=-1,
                             lanczos_degree=lanczos_degree,
                             error_rtol=error_rtol, verbose=False)
    time21 = time.time()

    # Elapsed times
    elapsed_time1 = time11 - time10
    elapsed_time2 = time21 - time20

    # Exact solution of eigencount for band matrix
    eigencount_exact = eigencount1

    # error
    error1 = relative_error(eigencount1, eigencount_exact)
    error2 = relative_error(eigencount2, eigencount_exact)

    # Print results
    print('')
    print('-------------------------------------------------------------')
    print('Method      Options                      trace   error   time')
    print('----------  ------------------------  --------  ------  -----')
    print('eigenvalue  N/A                       %8.3f  %5.2f%%  %5.2f'
          % (eigencount1, error1, elapsed_time1))
    print('slq         N/A                       %8.3f  %5.2f%%  %5.2f'
          % (eigencount2, error2, elapsed_time2))
    print('-------------------------------------------------------------')
    print('')


# ===============
# test eigencount
# ===============

def test_eigencount():
    """
    A test for :mod:`imate.eigencount` sub-package.
    """

    matrix = {
        'a': 2.0,
        'b': 1.0,
        'size': 50
    }

    exponents = [0, 1, 2]
    interval = [0.0, 10.0]
    dtypes = [r'float32', r'float64']
    grams = [True, False]
    sparses = [True, False]

    for dtype in dtypes:
        for gram in grams:

            if gram:
                assume_matrix = 'gen'
            else:
                assume_matrix = 'sym'

            # When gram is True:
            #     1. We generate a 2-band nonsymmetric matrix K (hence we set
            #        gram=False in toeplitz).
            #     2. We compute eigencount of K.T @ K using only K (hence we
            #        set gram=True in eigencount method).
            #
            # When gram is False:
            #     1. We generate a 3-band symmetric matrix K (hence we set
            #        gram=True in toeplitz).
            #     2. We compute eigencount of K using K (hence we set
            #        gram=False in eigencount method).
            K = toeplitz(matrix['a'], matrix['b'], matrix['size'],
                         gram=(not gram), dtype=dtype)

            for sparse in sparses:
                if not sparse:
                    K = K.toarray()

                for p in exponents:
                    print('dtype: %s, ' % (dtype) +
                          'sparse: %5s, ' % (sparse) +
                          'gram: %5s, ' % (gram) +
                          'exponent: %0.4f,\n' % (p) +
                          'assume_matrix: %s.' % (assume_matrix))

                    _test_eigencount_methods(K, matrix, gram, p, interval,
                                             assume_matrix)


# ===========
# System Main
# ===========

if __name__ == "__main__":
    sys.exit(test_eigencount())
