Documentation
=============
While this documentation aims to go beyond a simple listing of parameters and instead attempts to explain some of the
principles behind the functions, please see the section ":ref:`Usage`" for more details and usage examples including
code and flow field visualisations.

Using the Flow Class
~~~~~~~~~~~~~~~~~~~~
This section documents the custom flow class and all its class methods. It is the recommended way of using
``oflibnumpy`` and makes the full range of functionality available to the user.

Flow Constructors and Operators
-------------------------------
.. autoclass:: oflibnumpy.Flow
    :members: zero, from_matrix, from_transforms, from_kitti, from_sintel, vecs, ref, mask, shape, copy
    :special-members: __str__, __getitem__, __add__, __sub__, __mul__, __truediv__, __pow__, __neg__

    .. automethod:: __init__

Manipulating the Flow
---------------------
.. currentmodule:: oflibnumpy
.. automethod:: Flow.resize
.. automethod:: Flow.pad
.. automethod:: Flow.invert
.. automethod:: Flow.switch_ref
.. automethod:: Flow.combine_with

Applying the Flow
-----------------
.. currentmodule:: oflibnumpy
.. automethod:: Flow.apply
.. automethod:: Flow.track

Evaluating the Flow
-------------------
.. currentmodule:: oflibnumpy
.. automethod:: Flow.is_zero
.. automethod:: Flow.matrix
.. automethod:: Flow.valid_target
.. automethod:: Flow.valid_source
.. automethod:: Flow.get_padding

Visualising the Flow
--------------------
.. currentmodule:: oflibnumpy
.. automethod:: Flow.visualise
.. automethod:: Flow.visualise_arrows
.. automethod:: Flow.show
.. automethod:: Flow.show_arrows
.. autofunction:: oflibnumpy.visualise_definition

Using NumPy Arrays
~~~~~~~~~~~~~~~~~~
This section contains functions that take NumPy arrays as inputs, instead of making use of the custom flow class. On
the one hand, this avoids having to define flow objects. On the other hand, it requires keeping track of flow
attributes manually, and it does not avail itself of the full scope of functionality oflibnumpy can offer: most
importantly, flow masks are not considered or tracked.

Flow Loading
------------
.. autofunction:: oflibnumpy.from_matrix
.. autofunction:: oflibnumpy.from_transforms
.. autofunction:: oflibnumpy.load_kitti
.. autofunction:: oflibnumpy.load_sintel
.. autofunction:: oflibnumpy.load_sintel_mask

Flow Manipulation
-----------------
.. autofunction:: oflibnumpy.resize_flow
.. autofunction:: oflibnumpy.invert_flow
.. autofunction:: oflibnumpy.switch_flow_ref
.. autofunction:: oflibnumpy.combine_flows

Flow Application
----------------
.. autofunction:: oflibnumpy.apply_flow
.. autofunction:: oflibnumpy.track_pts

Flow Evaluation
---------------
.. autofunction:: oflibnumpy.is_zero_flow
.. autofunction:: oflibnumpy.get_flow_matrix
.. autofunction:: oflibnumpy.valid_target
.. autofunction:: oflibnumpy.valid_source
.. autofunction:: oflibnumpy.get_flow_padding

Flow Visualisation
------------------
.. autofunction:: oflibnumpy.visualise_flow
.. autofunction:: oflibnumpy.visualise_flow_arrows
.. autofunction:: oflibnumpy.show_flow
.. autofunction:: oflibnumpy.show_flow_arrows