import numpy as np
from scipy.spatial.transform import Rotation

from orbit2d import get_2dtrajectory


def _rotation(rin: np.ndarray, vin: np.ndarray) -> np.ndarray:
    v0 = np.linalg.norm(vin)
    b = np.linalg.norm(np.cross(rin, vin)) / v0
    d0 = np.sqrt(np.linalg.norm(rin)**2 - b**2)

    r2d, v2d = np.array([d0, b, 0.]), np.array([-v0, 0., 0.])
    rotation, loss = Rotation.align_vectors(np.array([rin, vin]), np.array([r2d, v2d]))
    assert loss == 0., "Rotation has non-zero loss."

    return (d0, b, v0), rotation

def get_3dtrajectory(rin: np.ndarray, vin: np.ndarray, k: float) -> tuple:
    (d0, b, v0), rotation = _rotation(rin, vin)
    (thetai, thetaf), rs, ts = get_2dtrajectory(d0, b, v0, k)

    r2d = lambda thetas: np.array([rs(thetas) * np.cos(thetas),
                                rs(thetas) * np.sin(thetas),
                                np.zeros(len(thetas))]).T
    
    return (thetai, thetaf), \
        lambda thetas: rotation.apply(r2d(thetas)), \
        ts
