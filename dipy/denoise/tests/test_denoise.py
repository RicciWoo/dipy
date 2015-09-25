import numpy as np
import numpy.testing as npt
from dipy.denoise.noise_estimate import estimate_sigma
from dipy.denoise.nlmeans import nlmeans
import dipy.data as dpd
import nibabel as nib

def test_denoise():
    """

    """
    fdata, fbval, fbvec = dpd.get_data()
    data = nib.load(fdata).get_data()
    sigma = estimate_sigma(data)
    denoised = nlmeans(data, sigma=sigma)
