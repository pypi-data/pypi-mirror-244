"""__init__.py
Provides version tools for create versioning for classes using inheritance. A VersionedClass is structured so any
subclasses can optionally define a version which can be used to compare other subclasses. This versioning framework
can also be used for objects of these classes, but it is primarily designed around versioning classes. Versioning is
useful for creating classes that interface with datastructures that change frequently and support for previous versions
are needed. For example, a file type may change how data is stored within it, but you might have files of the new and
previous version. In this case an appropriate class which addresses each version can be chosen based on the version of
the file which can be defined by the class' version.
"""
# Package Header #
from .header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from baseobjects.versioning import *
from .meta import *
from .versionregistry import VersionRegistry
from .versionedclass import VersionedClass
