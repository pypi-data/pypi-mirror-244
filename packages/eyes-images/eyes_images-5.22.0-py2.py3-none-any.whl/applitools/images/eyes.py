from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING, ByteString, Union

from applitools.common import Region
from applitools.common.eyes import EyesBase
from applitools.common.optional_deps import Image
from applitools.common.selenium import Configuration

from .fluent import Target
from .runner import ClassicRunner

if TYPE_CHECKING:
    from typing import Optional, Text

    from applitools.common.utils.custom_types import ViewPort


class Eyes(EyesBase):
    _Configuration = Configuration
    _DefaultRunner = ClassicRunner

    def __init__(self):
        super(Eyes, self).__init__(None)

    def open(self, app_name=None, test_name=None, dimension=None):
        # type: (Text, Text, Optional[ViewPort]) -> None
        if not self.configure.is_disabled:
            self._prepare_open(app_name, test_name, dimension)
            self._eyes_ref = self._commands.manager_open_eyes(
                self._object_registry,
                self._runner._ref,  # noqa
                config=self.configure,
            )

    def check_region(self, image, region, tag=None):
        # type: (Union[ByteString, Text, Image], Region, Optional[Text]) -> bool
        return self.check(tag, Target.region(image, region))
