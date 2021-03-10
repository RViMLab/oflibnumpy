from __future__ import annotations
from typing import Union
import numpy as np
from .utils import get_valid_ref, flow_from_matrix, matrix_from_transform


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
            if not input_mask.ndim == 2:
                raise ValueError("Error setting flow mask: Input not 2-dimensional")
            if not input_mask.shape == self.shape:
                raise ValueError("Error setting flow mask: Input has a different shape than the flow vectors")
            if ((input_mask != 0) & (input_mask != 1)).any():
                raise ValueError("Error setting flow mask: Values must be 0 or 1")
            self._mask = input_mask.astype('bool')

    @property
    def shape(self) -> tuple:
        """Gets shape (resolution) of the flow

        :return: Shape (resolution) of the flow field as a tuple
        """

        return self.vecs.shape[:2]

    @classmethod
    def zero(cls, size: list, ref: str = None, mask: np.ndarray = None) -> Flow:
        """Flow object constructor, zero everywhere

        :param size: List [H, W] of flow field size
        :param ref: Flow referencce, 't'arget or 's'ource. Defaults to 't'
        :param mask: Numpy array H-W containing a boolean mask indicating where the flow vectors are valid. Defaults to
            True everywhere.
        :return: Flow object
        """

        return cls(np.zeros((size[0], size[1], 2), 'float32'), ref, mask)

    @classmethod
    def from_matrix(cls, matrix: np.ndarray, size: list, ref: str = None, mask: np.ndarray = None) -> Flow:
        """Flow object constructor, based on transformation matrix input

        :param matrix: Transformation matrix to be turned into a flow field, as Numpy array 3-3
        :param size: List [H, W] of flow field size
        :param ref: Flow referencce, 't'arget or 's'ource. Defaults to 't'
        :param mask: Numpy array H-W containing a boolean mask indicating where the flow vectors are valid. Defaults to
            True everywhere.
        :return: Flow object
        """

        ref = get_valid_ref(ref)
        if ref == 's':
            # Coordinates correspond to the meshgrid of the original ('s'ource) image. They are transformed according
            # to the transformation matrix. The start points are subtracted from the end points to yield flow vectors.
            flow_vectors = flow_from_matrix(matrix, size)
            return cls(flow_vectors, ref, mask)
        elif ref == 't':
            # Coordinates correspond to the meshgrid of the warped ('t'arget) image. They are inversely transformed
            # according to the transformation matrix. The end points, which correspond to the flow origin for the
            # meshgrid in the warped image, are subtracted from the start points to yield flow vectors.
            flow_vectors = -flow_from_matrix(np.linalg.pinv(matrix), size)
            return cls(flow_vectors, ref, mask)

    @classmethod
    def from_transforms(cls, transform_list: list, size: list, ref: str = None, mask: np.ndarray = None) -> Flow:
        """Flow object constructor, zero everywhere.

        :param transform_list: List of transforms to be turned into a flow field. Options for each transform in list:
            ['translation', horizontal shift in px, vertical shift in px]
            ['rotation', horizontal centre in px, vertical centre in px, angle in degrees, counter-clockwise]
            ['scaling', horizontal centre in px, vertical centre in px, scaling fraction]
        :param size: List [H, W] of flow field size
        :param ref: Flow referencce, 't'arget or 's'ource. Defaults to 't'
        :param mask: Numpy array H-W containing a boolean mask indicating where the flow vectors are valid. Defaults to
            True everywhere.
        :return: Flow object
        """

        # Process for flow reference 's' is straightforward: get the transformation matrix for each given transform in
        #   the transform_list, and get the final transformation matrix by multiplying the transformation matrices for
        #   each individual transform sequentially. Finally, call flow_from_matrix to get the corresponding flow field,
        #   which works by applying that final transformation matrix to a meshgrid of vector locations, and subtracting
        #   the start points from the end points.
        #   flow_s = transformed_coords - coords
        #          = final_transform * coords - coords
        #          = t_1 * ... * t_n * coords - coords
        #
        # Process for flow reference 't' can be done in two ways:
        #   1) get the transformation matrix for each given transform in the transform_list, and get the final
        #     transformation matrix by multiplying the transformation matrices for each individual transform in inverse
        #     order. Then, call flow_from_matrix on the *inverse* of this final transformation matrix to get the
        #     negative of the corresponding flow field, which means applying the inverse of that final transformation
        #     matrix to a meshgrid of vector locations, and subtracting the end points from the start points.
        #     flow_t = coords - transformed_coords
        #            = coords - inv(final_transform) * coords
        #            = coords - inv(t_1 * ... * t_n) * coords
        #   2) get the transformation matrix for the reverse of each given transform in the "inverse inverse order",
        #     i.e. in the given order of the transform_list, and get the final transformation matrix by multiplying the
        #     results sequentially. Then, call flow_from_matrix on this final transformation matrix (already
        #     corresponding to the inverse as in method 1)) to get the negative of the corresponding flow field as
        #     before. This method is more complicated, but avoids any numerical issues potentially arising from
        #     calculating the inverse of a matrix.
        #     flow_t = coords - transformed_coords
        #            = coords - final_transform * coords
        #            = coords - inv(t_n) * ... * inv(t_1) * coords
        #     ... because: inv(t_n) * ... * inv(t_1) = inv(t_1 * ... * t_n)

        # Here implemented: method 1, via calling from_matrix where the inverse of the matrix is used if reference 't'
        ref = get_valid_ref(ref)
        matrix = np.identity(3)
        for transform in reversed(transform_list):
            matrix = matrix @ matrix_from_transform(transform[0], transform[1:])
        return cls.from_matrix(matrix, size, ref, mask)

    def __getitem__(self, item: Union[int, list, slice]) -> Flow:
        """Mimics __getitem__ of a numpy array, returning a flow object cut accordingly

        Will throw an error if mask.__getitem__(item) or vecs.__getitem__(item) throw an error

        :param item: Slice used to select a part of the flow
        :return: New flow cut as a corresponding numpy array would be cut
        """

        return Flow(self.vecs.__getitem__(item), self.ref, self.mask.__getitem__(item))