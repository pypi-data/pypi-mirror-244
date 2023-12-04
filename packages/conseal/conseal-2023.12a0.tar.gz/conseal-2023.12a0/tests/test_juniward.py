
import conseal as cl
import jpeglib
import logging
import os
from parameterized import parameterized
import sys
import time
import unittest
import numpy as np
from scipy.io import loadmat

from defs import ASSETS_DIR
STEGO_DIR = ASSETS_DIR / 'juniward'
COVER_DIR = STEGO_DIR / 'cover'


class TestJUNIWARD(unittest.TestCase):
    """Test suite for J-UNIWARD embedding."""
    _logger = logging.getLogger(__name__)

    @staticmethod
    def read_costmap(costmap_filename, height, width):
        """
        Read binary file produced by modified J-UNIWARD C++ implementation
        :param costmap_filename: path to binary file
        :param height: of the original image
        :param width: of the original image
        :return: ndarray of shape [height, width, 3]
            Channel 0: If the cover pixel is at the minimum -1023 already, the pixel contains the wet cost; otherwise rho.
            Channel 1: Always 0.
            Channel 2: If the cover pixel is at the maximum 1023 already, the pixel contains the wet cost; otherwise rho.
        """
        count = height * width * 3
        with open(costmap_filename, 'rb') as f:
            costmap = np.fromfile(f, dtype=np.float32, count=count, sep='')
            costmap = costmap.reshape(height, width, 3)
        return costmap

    @parameterized.expand([[f'{i:05d}'] for i in range(1, 6)])
    def test_costmap_matlab_python_original_equivalence(self, filepath):
        self._logger.info(f'TestJUNIWARD.test_costmap_matlab_python_original_equivalence({filepath=})')

        cover_filepath = COVER_DIR / f'{filepath}.jpg'
        costmap_matlab_filepath = STEGO_DIR / 'costmap-matlab' / f'{filepath}.mat'

        img_spatial = np.squeeze(jpeglib.read_spatial(cover_filepath).spatial[..., 0]).astype(np.float64)
        img_dct = jpeglib.read_dct(cover_filepath)
        qt = img_dct.qt[0]

        costs = cl.juniward.compute_cost(
            spatial=img_spatial,
            quant_table=qt,
            implementation=cl.JUNIWARD_ORIGINAL,
        )
        costs_jpegio = cl.tools.dct.jpeglib_to_jpegio(costs)

        # compare to reference
        costmap_matlab = loadmat(costmap_matlab_filepath)['cost_map']
        self.assertTrue(np.allclose(costs_jpegio, costmap_matlab))

    @parameterized.expand([[f'{i:05d}'] for i in range(1, 6)])
    def test_costmap_python_cpp_fixed_equivalence(self, filepath):
        self._logger.info(f'TestJUNIWARD.test_costmap_python_cpp_fixed_equivalence({filepath=})')

        cover_filepath = COVER_DIR / f'{filepath}.jpg'
        costmap_cpp_filepath = STEGO_DIR / 'costmap-cpp-fixed' / f'{filepath}.costmap'

        img_spatial = np.squeeze(jpeglib.read_spatial(cover_filepath).spatial[..., 0]).astype(np.float64)
        height, width = img_spatial.shape
        img_dct = jpeglib.read_dct(cover_filepath)
        dct_coeffs = img_dct.Y
        qt = img_dct.qt[0]

        costs = cl.juniward.compute_cost(
            spatial=img_spatial,
            quant_table=qt,
            implementation=cl.JUNIWARD_FIX_OFF_BY_ONE,
        )
        costs_jpegio = cl.tools.dct.jpeglib_to_jpegio(costs)

        costmap_cpp = self.read_costmap(costmap_cpp_filepath, height=height, width=width)

        # Take min channel
        costmap_cpp = costmap_cpp[:, :, 0]

        # Compare only pixels that were not marked as wet
        wet_cost = 10 ** 13
        mask = costmap_cpp < wet_cost

        assert np.allclose(costs_jpegio[mask], costmap_cpp[mask])

    @parameterized.expand([[f'{i:05d}'] for i in range(1, 6)])
    def test_embedding_probability_map_matlab(self, filepath):
        self._logger.info(f'TestJUNIWARD.test_embedding_probability_map_matlab({filepath=})')
        cover_filepath = COVER_DIR / f'{filepath}.jpg'
        probability_matlab_filepath = STEGO_DIR / 'probability-map-matlab' / f'{filepath}.mat'

        cover_spatial = np.squeeze(
            jpeglib.read_spatial(cover_filepath).spatial[..., 0]
        ).astype(np.float64)
        img_dct = jpeglib.read_dct(cover_filepath)
        cover_dct_coeffs = img_dct.Y

        rho_p1, rho_m1 = cl.juniward.compute_distortion(
            cover_spatial=cover_spatial,
            cover_dct_coeffs=cover_dct_coeffs,
            quant_table=img_dct.qt[0],
            implementation=cl.JUNIWARD_ORIGINAL,
            wet_cost=10**10,
        )
        (pChangeP1, pChangeM1), lbda = cl.simulate._ternary.probability(
            rhoP1=cl.tools.dct.jpeglib_to_jpegio(rho_p1),
            rhoM1=cl.tools.dct.jpeglib_to_jpegio(rho_m1),
            alpha=.4,
            n=cl.tools.dct.nzAC(cover_dct_coeffs),
        )

        # compare to refernece Matlab
        mat = loadmat(probability_matlab_filepath)
        self.assertTrue(np.allclose(pChangeP1, mat['pChangeP1']))
        self.assertTrue(np.allclose(pChangeM1, mat['pChangeM1']))

    @parameterized.expand([[f'{i:05d}.jpg'] for i in range(1, 6)])
    def test_simulation_python_matlab_equivalence(self, filepath):
        self._logger.info(f'TestJUNIWARD.test_simulation_python_matlab_equivalence('
                          f'{filepath=})')

        cover_filepath = COVER_DIR / filepath
        stego_matlab_filepath = STEGO_DIR / 'stego-matlab' / filepath

        # Read grayscale image
        cover_spatial = jpeglib.read_spatial(cover_filepath).spatial[:, :, 0]
        cover_spatial = cover_spatial.astype(np.float64)

        # Read DCT coefficients and quantization table
        img_dct = jpeglib.read_dct(cover_filepath)
        cover_dct_coeffs = img_dct.Y
        qt = img_dct.qt[0]

        # Simulate stego embedding using fixed seed and generator
        stego_dct_coeffs = cl.juniward.simulate_single_channel(
            cover_spatial=cover_spatial,
            cover_dct_coeffs=cover_dct_coeffs,
            quantization_table=qt,
            embedding_rate=0.4,
            implementation=cl.JUNIWARD_ORIGINAL,
            generator='MT19937',
            seed=6020)

        # Read stego images created using Matlab
        stego_matlab_im = jpeglib.read_dct(stego_matlab_filepath)
        stego_matlab_dct_coeffs = stego_matlab_im.Y

        # Compare stego images
        self.assertTrue(np.allclose(stego_dct_coeffs, stego_matlab_dct_coeffs))

    def test_juniward_simulation_time(self):
        self._logger.info('TestJUNIWARD.test_juniward_simulation_time')

        # load cover
        cover_filepath = ASSETS_DIR / 'cover' / 'lizard.jpeg'
        # Read grayscale image
        cover_spatial = jpeglib.read_spatial(cover_filepath).spatial[:, :, 0]
        cover_spatial = cover_spatial.astype(np.float64)

        # Read DCT coefficients and quantization table
        img_dct = jpeglib.read_dct(cover_filepath)
        cover_dct_coeffs = img_dct.Y
        qt = img_dct.qt[0]

        # time the simulation
        start = time.perf_counter()

        # Simulate stego embedding using fixed seed and generator
        cl.juniward.simulate_single_channel(
            cover_spatial=cover_spatial,
            cover_dct_coeffs=cover_dct_coeffs,
            quantization_table=qt,
            embedding_rate=0.4,
            implementation=cl.JUNIWARD_ORIGINAL,
            seed=12345)

        end = time.perf_counter()
        # test speed
        delta = end - start

        self.assertLess(delta, 30)  # faster than 10s
        self._logger.info(f'J-UNIWARD embedding 0.4 bpnzAC in 512x512: {delta*1000:.02f} ms')


__all__ = ["TestJUNIWARD"]
