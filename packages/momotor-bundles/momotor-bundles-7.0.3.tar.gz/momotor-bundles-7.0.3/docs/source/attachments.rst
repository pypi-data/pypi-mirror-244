.. _attachments:

Attachments handling
====================

Bundles can have local attachments, files that are referenced from the XML. Bundles with attachments are stored as
zip files.

The ``<link>``, ``<repository>`` and ``<file>`` nodes of the bundle XML all have an optional `src` attribute that
can reference attachments. The path of `src` is relative to the location of the XML document of the bundle.
The `src` attribute can refer to a single file or a directory. When `src` references a directory, all files
in that directory and subdirectories thereof are part of the bundle.

The :py:class:`~momotor.bundles.elements.checklets.Link`, :py:class:`~momotor.bundles.elements.checklets.Repository` and
:py:class:`~momotor.bundles.elements.files.File` classes provide several methods to access the attachment, for example
:py:meth:`~momotor.bundles.mixins.attachments.AttachmentMixin.open` and
:py:meth:`~momotor.bundles.mixins.attachments.AttachmentMixin.copy_to`.
When working with an existing zip bundle, the files are accessed directly from the zip file.

When creating a bundle the `src` attribute of these elements should refer to the file or directory to attach.
These files or directories need to remain available on the filesystem until the bundle has been exported using the
:py:meth:`~momotor.bundles.Bundle.to_buffer`, :py:meth:`~momotor.bundles.Bundle.to_file` or
:py:meth:`~momotor.bundles.Bundle.to_directory` methods, and when using the latter export method,
the `src` paths may not overlap the path to export the bundle to.
