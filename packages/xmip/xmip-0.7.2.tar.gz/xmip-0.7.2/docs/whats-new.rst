.. currentmodule:: xmip

What's New
===========
.. _whats-new.0.7.2:

v0.7.2 (unreleased)
-------------------

Internal Changes
~~~~~~~~~~~~~~~~
- Added PR template (:pull:`304`). By `Julius Busecke <https://github.com/jbusecke>`


.. _whats-new.0.7.0:

v0.7.0 (2023/01/03)
-------------------

New Features
~~~~~~~~~~~~
- :py:func:`~xmip.postprocessing.match_metrics` Now allows more flexible metric matching (accepting e.g. already merged members) + better error for missing match_attrs (:pull:`275`). By `Julius Busecke <https://github.com/jbusecke>`_
- Postprocessing functions can now easily be nested on top of each other (:pull:`187`). By `Julius Busecke <https://github.com/jbusecke>`_


Breaking Changes
~~~~~~~~~~~~~~~~
- Requires xarray>=0.17.0 and drops support for python 3.6 (:pull:`170`, :pull:`173`). By `Julius Busecke <https://github.com/jbusecke>`_
- :py:func:`~xmip.utils.cmip6_dataset_id` not includes the attribute `variable_id` (:pull:`166`) By `Julius Busecke <https://github.com/jbusecke>`_
- Dropped support for python 3.7 (:pull:`268`, :issue:`267`). By `Julius Busecke <https://github.com/jbusecke>`_

Internal Changes
~~~~~~~~~~~~~~~~

- Unit correction logic now uses pint-xarray under the hood (:pull:`160`, :issue:`31`).
By `Tom Nicholas <https://github.com/TomNicholas>`_ and `Julius Busecke <https://github.com/jbusecke>`_

- License changed to Apache-2.0 (:pull:`272`, :issue:`256`). By `Julius Busecke <https://github.com/jbusecke>`_

Bugfixes
~~~~~~~~
- :py:func:`~xmip.postprocessing.concat_members` now accepts datasets which already have 'member_id' as a dimension (maintain compatibility with recent intake-esm changes) (:pull:`277`). By `Julius Busecke <https://github.com/jbusecke>`_

- :py:func:`~xmip.postprocessing.match_metrics` now accepts single variables as str input (:issue:`229`, :pull:`245`). By `Julius Busecke <https://github.com/jbusecke>`_

- :py:func:`~xmip.postprocessing.concat_members` now returns a dataset with labelled `member_id` dimension (:issue:`196` , :pull:`197`). By `Julius Busecke <https://github.com/jbusecke>`_

- Fixes incompatibility with upstream changes in xarray>=0.19.0 (:issue:`173`, :pull:`174`). By `Julius Busecke <https://github.com/jbusecke>`_

- :py:func:`~xmip.drift_removal.match_and_remove_drift` does now work with chunked (dask powered) datasets (:pull:`164`).By `Julius Busecke <https://github.com/jbusecke>`_

Internal Changes
~~~~~~~~~~~~~~~~

- Unit correction logic now uses pint-xarray under the hood (:pull:`160`, :issue:`31`).
By `Tom Nicholas <https://github.com/TomNicholas>`_ and `Julius Busecke <https://github.com/jbusecke>`_


.. _whats-new.0.5.0:

v0.5.0 (2021/7/9)
-------------------

New Features
~~~~~~~~~~~~
- :py:func:`~xmip.postprocessing.interpolate_grid_labels` enables batch combination of different grid_labels
(e.g. from native to regridded and vice versa) using xesmf (:pull:`161`). By `Julius Busecke <https://github.com/jbusecke>`_

- :py:func:`~xmip.drift_removal.match_and_remove_drift` enables batch detrending/drift-drift_removal
from a dictionary of datasets (:pull:`155`). By `Julius Busecke <https://github.com/jbusecke>`_

.. _whats-new.0.4.0:

v0.4.0 (2021/6/9)
-------------------

New Features
~~~~~~~~~~~~

- Started implementing metadata fixes in `combined_preprocessing` (:pull:`147`). By `Julius Busecke <https://github.com/jbusecke>`_

- Added `drift_removal` which adds ability to align time of branched runs and remove drift from the parent (e.g. control) run (:pull:`126`, :pull:`148`). By `Julius Busecke <https://github.com/jbusecke>`_

.. _whats-new.0.3.0:

v0.3.0 (2021/6/9)
-------------------

New Features
~~~~~~~~~~~~
- Added `postprocessing` module and added ability to parse metrics to multiple datasets in a dictionary (:pull:`110`, :pull:`117`). By `Julius Busecke <https://github.com/jbusecke>`_


Internal Changes
~~~~~~~~~~~~~~~~

- Refactored CI internals, added dependabot, and some updated failcases (:pull:`121`, :pull:`128`, :pull:`129`, :pull:`133`, :pull:`134`, :pull:`135`). By `Julius Busecke <https://github.com/jbusecke>`_

.. _whats-new.0.2.0:

v0.2.0 (2021/4/9)
-----------------

Breaking changes
~~~~~~~~~~~~~~~~
- Removed `replace_x_y_nominal_lat_lon` from `combined_preprocessing` due to ongoing performance issues with dask (:issue:`75`, :issue:`85`, :issue:`94`) (:pull:`104`). By `Julius Busecke <https://github.com/jbusecke>`_
- Further refactor of `replace_x_y_nominal_lat_lon`, which avoids missing values in the dimension coordinates (:issue:`66`) (:pull:`79`). By `Julius Busecke <https://github.com/jbusecke>`_

- Consistent treatment of cf-style bounds. The combination of `parse_lon_lat_bounds`,`maybe_convert_bounds_to_vertex`, `maybe_convert_vertex_to_bounds`, and `sort_vertex_order` applied on the dataset, assures that all datasets have both conventions available and the vertex order is the same. By `Julius Busecke <https://github.com/jbusecke>`_

- New implementation of `replace_x_y_nominal_lat_lon`, which avoids duplicate values in the derived dimensions (:issue:`34`) (:pull:`35`). By `Julius Busecke <https://github.com/jbusecke>`_

New Features
~~~~~~~~~~~~
- Create merged region masks with :py:func:`merged_mask` (:pull:`18`). By `Julius Busecke <https://github.com/jbusecke>`_


Bug fixes
~~~~~~~~~
- Updated cmip6 catalog location for the pangeo gc archive (:issue:`80`) (:pull:`81`). By `Julius Busecke <https://github.com/jbusecke>`_


Documentation
~~~~~~~~~~~~~
- Sphinx/RTD documentation, including contributor guide and new logo 🤗. (:issue:`27`) (:pull:`99`).

Internal Changes
~~~~~~~~~~~~~~~~
- Adds options to skip extensive cloud ci by using [skip-ci] in commit message. Adds the ability to cancel previous GHA jobs to prevent long wait times for rapid pushes. (:pull:`99`) By `Julius Busecke <https://github.com/jbusecke>`_.

-  Add `ni` and `nj` to the `rename_dict` dictionary in _preprocessing.py_ as dimensions to be corrected (:pull:`54`). By `Markus Ritschel <https://github.com/markusritschel>`_


.. _whats-new.0.1.2:

v0.1.2
------


New Features
~~~~~~~~~~~~
- Added more models, now supporting both ocean and atmospheric output for :py:func:`combined_preprocessing` (:pull:`14`). By `Julius Busecke <https://github.com/jbusecke>`_



.. _whats-new.0.1.0:

v0.1.0 (2/21/2020)
----------------------

Initial release.
