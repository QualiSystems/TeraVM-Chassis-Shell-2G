from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.devices.driver_helper import get_logger_with_thread_id
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from traffic.teravm.chassis.client import TeraVMClient
from traffic.teravm.chassis.configuration_attributes_structure import TrafficGeneratorChassisResource
from traffic.teravm.chassis.runners.autoload_runner import TeraVMAutoloadRunner


class TeraVMChassisDriver(ResourceDriverInterface):
    SHELL_NAME = "Traffic TeraVM 2G"

    def initialize(self, context):
        """

        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        pass

    def cleanup(self):
        pass

    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Autoload started')

        with ErrorHandlingContext(logger):
            resource_config = TrafficGeneratorChassisResource.from_context(context=context, shell_name=self.SHELL_NAME)

            tvm_client = TeraVMClient(address=resource_config.address, port=int(resource_config.port))

            autoload_runner = TeraVMAutoloadRunner(tvm_client=tvm_client,
                                                   resource_config=resource_config,
                                                   logger=logger)

            response = autoload_runner.discover()
            logger.info('Autoload completed')

            return response
