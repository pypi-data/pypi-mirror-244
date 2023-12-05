Bundles
=======

There is a class for each bundle type:
:class:`~momotor.bundles.ConfigBundle`,
:class:`~momotor.bundles.ProductBundle`,
:class:`~momotor.bundles.RecipeBundle`,
:class:`~momotor.bundles.ResultsBundle`, and
:class:`~momotor.bundles.TestResultBundle`.

All classes implement the same basic functionality to implement reading and writing bundles,
plus functionality specific to the bundle type.

:class:`~momotor.bundles.Bundle`
--------------------------------

:class:`~momotor.bundles.Bundle` is the base class from which all other bundle types extend. It provides the shared
functionality for all bundle classes.

The constructor creates a new uninitialized bundle. The
:py:meth:`~momotor.bundles.Bundle.create` method can be used to initialize a newly created bundle, the class methods
:py:meth:`~momotor.bundles.Bundle.from_bytes_factory` and
:py:meth:`~momotor.bundles.Bundle.from_file_factory`
can be used to create an initialized instance of a bundle class from an existing bundle file,
either from memory or disk.

The methods :py:meth:`~momotor.bundles.Bundle.to_buffer`, :py:meth:`~momotor.bundles.Bundle.to_directory`, and
:py:meth:`~momotor.bundles.Bundle.to_file` can be used to export a bundle to various destinations. A bundle must be
fully initialized before it can be exported.

.. autoclass:: momotor.bundles.Bundle
   :members:
   :exclude-members: recreate
   :inherited-members:

:class:`~momotor.bundles.ConfigBundle`
--------------------------------------

A :class:`~momotor.bundles.ConfigBundle` contains all configuration needed by the recipe.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor.configComplexType`

It also implements all methods inherited from :class:`~momotor.bundles.Bundle`

.. autoclass:: momotor.bundles.ConfigBundle
   :members: create,
             id,
             options, get_options, get_option_value,
             files, copy_files_to

:class:`~momotor.bundles.ProductBundle`
---------------------------------------

A :class:`~momotor.bundles.ProductBundle` contains the product to be evaluated by the recipe.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor.productComplexType`

It also implements all methods inherited from :class:`~momotor.bundles.Bundle`

.. autoclass:: momotor.bundles.ProductBundle
   :members: create,
             id,
             options, get_options, get_option_value,
             files, copy_files_to,
             properties, get_properties, get_property_value

:class:`~momotor.bundles.RecipeBundle`
--------------------------------------

A :class:`~momotor.bundles.RecipeBundle` describes the process of processing a product into a result.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor.recipeComplexType`

It also implements all methods inherited from :class:`~momotor.bundles.Bundle`

.. autoclass:: momotor.bundles.RecipeBundle
   :members: create,
             id,
             steps,
             tests,
             options, get_options, get_option_value,
             files, copy_files_to

:class:`~momotor.bundles.ResultsBundle`
---------------------------------------

A :class:`~momotor.bundles.ResultsBundle` contains the results of the recipe applied to a product.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor.resultsComplexType`

It also implements all methods and properties inherited from :class:`~momotor.bundles.Bundle` and
:class:`~momotor.bundles.elements.results.Results`

.. autoclass:: momotor.bundles.ResultsBundle
   :members: create,
             id,
             results

.. autofunction:: momotor.bundles.results.create_error_result_bundle

:class:`~momotor.bundles.TestResultBundle`
------------------------------------------

A :class:`~momotor.bundles.TestResultBundle` contains the results of a recipe's self-test.
It provides a Python interface to read and create XML files of
:class:`~momotor.bundles.binding.momotor.testResultComplexType`

It also implements all methods inherited from :class:`~momotor.bundles.Bundle`

Self-testing is not yet implemented in Momotor.

.. autoclass:: momotor.bundles.TestResultBundle
   :members: create, results
