import numpy as np
from .utils import get_valid_ref


class Flow(object):
    def __init__(self, flow_vectors: np.ndarray, ref: str = None, mask: np.ndarray = None):
        """Flow object constructor

        :param flow_vectors: Numpy array H-W-2 containing the flow vector in OpenCV convention: [..., 0] are horizontal,
            [..., 1] are vertical vector components (rather than the numpy vertical first, horizontal second convention)
        :param ref: Flow referencce, 't'arget or 's'ource. Defaults to 't'
        :param mask: Numpy array H-W containing a boolean mask indicating where the flow vectors are valid. Defaults to
            True everywhere.
        """
        self.vecs = flow_vectors
        self.ref = ref
        self.mask = mask

    @property
    def vecs(self) -> np.ndarray:
        """Gets flow vectors

        :return: Flow vectors as numpy array of shape H-W-2 and type 'float32'
        """

        return self._vecs

    @vecs.setter
    def vecs(self, input_vecs: np.ndarray):
        """Sets flow vectors, after checking validity

        :param input_vecs: Numpy array of shape H-W-2
        """

        if not isinstance(input_vecs, np.ndarray):
            raise TypeError("Error setting flow vectors: Input is not a numpy array")
        if not input_vecs.ndim == 3:
            raise ValueError("Error setting flow vectors: Input not 3-dimensional")
        if not input_vecs.shape[2] == 2:
            raise ValueError("Error setting flow vectors: Input does not have 2 channels")
        f = input_vecs.astype('float32')
        self._vecs = f

    @property
    def ref(self) -> str:
        """Gets flow reference

        :return: Flow reference 't' or 's'
        """

        return self._ref

    @ref.setter
    def ref(self, input_ref: str = None):
        """Sets flow reference, after checking validity

        :param input_ref: Flow reference 't' or 's'. Defaults to 't'
        """

        self._ref = get_valid_ref(input_ref)

    @property
    def mask(self) -> np.ndarray:
        """Gets flow mask

        :return: Flow mask as numpy array of shape H-W and type 'bool'
        """

        return self._mask

    @mask.setter
    def mask(self, input_mask: np.ndarray = None):
        """Sets flow mask, after checking validity

        :param input_mask: bool numpy array of size H-W (self.shape), matching flow vectors with size H-W-2
        """

        if input_mask is None:
            self._mask = np.ones(self.shape[0:2], 'bool')
        else:
            if not isinstance(input_mask, np.ndarray):
                raise TypeError("Error setting flow mask: Input is not a numpy array")
            if not input_mask.ndim == 3:
                raise ValueError("Error setting flow mask: Input not 3-dimensional")
            if not input_mask.shape[2] == 2:
                raise ValueError("Error setting flow mask: Input does not have 2 channels")
            if any((input_mask != 0) & (input_mask != 1)):
                raise ValueError("Error setting flow mask: Values must be 0 or 1")
            self._mask = input_mask.astype('bool')

    @property
    def shape(self) -> list:
        """Gets shape (resolution) of the flow

        :return: Shape (resolution) of the flow field as a list
        """

        return list(self.vecs.shape[:2])
