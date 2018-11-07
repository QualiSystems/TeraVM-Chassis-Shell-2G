from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.devices.driver_helper import get_api
from cloudshell.devices.driver_helper import get_logger_with_thread_id
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.traffic.teravm.api.client import TeraVMClient

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
            cs_api = get_api(context)
            password = cs_api.DecryptPassword(resource_config.password).Value

            tvm_client = TeraVMClient(address=resource_config.address,
                                      user=resource_config.user,
                                      password=password,
                                      port=int(resource_config.port))

            autoload_runner = TeraVMAutoloadRunner(tvm_client=tvm_client,
                                                   resource_config=resource_config,
                                                   logger=logger)

            response = autoload_runner.discover()
            logger.info('Autoload completed')

            return response

if __name__ == "__main__":
    import mock
    from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

    address = '192.168.42.192'

    user = 'admin'
    password = 'admin'
    port = 443
    auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
    api_port = 8029

    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'dsada'
    context.resource.fullname = 'TestAireOS'
    context.reservation = ReservationContextDetails()
    context.reservation.reservation_id = '559a65ef-962d-4495-a575-f6b0eb95f7af'
    context.resource.attributes = {}
    context.resource.attributes['{}.User'.format(TeraVMChassisDriver.SHELL_NAME)] = user
    context.resource.attributes['{}.Password'.format(TeraVMChassisDriver.SHELL_NAME)] = password
    context.resource.attributes["{}.Controller TCP Port".format(TeraVMChassisDriver.SHELL_NAME)] = port
    context.resource.address = address

    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = "192.168.85.10"

    dr = TeraVMChassisDriver()
    dr.initialize(context)

    out = dr.get_inventory(context)
    for resource in out.resources:
        print resource.__dict__
