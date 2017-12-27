from traffic.teravm.chassis.flows.autoload_flow import TeraVMAutoloadFlow


class TeraVMAutoloadRunner(object):
    def __init__(self, tvm_client, logger, resource_config):
        """

        :param tmv_chassis.client.TeraVMClient tvm_client:
        :param logging.Logger logger:
        :param tvm_chassis.configuration_attributes_structure.TrafficGeneratorChassisResource resource_config:
        """
        self._tvm_client = tvm_client
        self._logger = logger
        self._resource_config = resource_config

    @property
    def _autoload_flow(self):
        return TeraVMAutoloadFlow(logger=self._logger,
                                  tvm_client=self._tvm_client,
                                  resource_config=self._resource_config)

    def discover(self):
        return self._autoload_flow.autoload_details()
