"""
Created on 6 May 2013

@author: mike
"""
from abc import abstractmethod, ABCMeta

from volatility.framework import validity
from volatility.framework.interfaces import context as context_module

#
#  Plugins
#   - Take in relevant number of TranslationLayers (of specified type)
#   - Outputs TreeGrid
#
#
#
#
#

class PluginInterface(validity.ValidityRoutines):
    """Class that defines the interface all Plugins must maintain"""
    __metaclass__ = ABCMeta

    def __init__(self, context):
        self.type_check(context, context_module.ContextInterface)
        self._context = context

    @property
    def context(self):
        return self._context

    @classmethod
    @abstractmethod
    def determine_inputs(cls):
        """Returns the accepted inputs

           This should be a dictionary of TranslationLayer names matched to TranslationLayer types
        """

    def verify_inputs(self):
        """Verifies the inputs based on the output of determine_inputs"""
        inputs = self.determine_inputs()
        for tl_name, tl_type in inputs.items():
            layer = self.context.memory.get(tl_name, None)
            if layer is not None:
                if not layer.can_handle(tl_type):
                    raise TypeError("Layer " + tl_name + " cannot handle type " + tl_type + )
            else:
                raise TypeError("Layer " + tl_name + " has not been populated.")

    @abstractmethod
    def establish_context(self):
        """Alters the context to ensure the plugin can run.

        This function constructs the necessary symbol spaces that the plugin will need.
        """

    @abstractmethod
    def plugin_options(self, config_group = None):
        """Modifies the passed in ConfigGroup object to contain the required options"""

    @abstractmethod
    def __call__(self, context):
        """Executes the functionality of the code

        @:param

        :return: a TreeGrid object that can then be passed to a Renderer.
        :rtype: TreeGrid
        """


# TODO: Needs to say what it can/can't handle (validate context)
# TODO: Needs to offer available options'
# TODO: Figure out how to handle global config options