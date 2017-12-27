from cloudshell.devices.autoload.autoload_builder import AutoloadDetailsBuilder

from traffic.teravm.chassis.autoload import models


class TeraVMAutoloadFlow(object):
    def __init__(self, tvm_client, resource_config, logger):
        """

        :param traffic.teravm.chassis.client.TeraVMClient tvm_client:
        :param traffic.teravm.chassis.configuration_attributes_structure.TrafficGeneratorChassisResource resource_config:
        :param logging.Logger logger:
        """
        self._tvm_client = tvm_client
        self._logger = logger
        self._resource_config = resource_config

    def autoload_details(self):
        """

        :return:
        """
        modules = self._tvm_client.get_modules_info()
        resource = models.Chassis(shell_name=self._resource_config.shell_name,
                                  name=self._resource_config.name,
                                  unique_id=self._resource_config.fullname)

        for module in modules:
            mod_res = models.Module(shell_name=self._resource_config.shell_name,
                                    name=module["name"].replace("/", "-"),
                                    unique_id=module["resourceId"])

            resource.add_sub_resource(module["number"], mod_res)

            for test_agent in module["testAgents"]:
                for test_if in test_agent["testInterfaces"]:

                    port_res = models.Port(shell_name=self._resource_config.shell_name,
                                           name=test_if["name"].replace("/", "-"),
                                           unique_id=test_if["resourceId"])

                    mod_res.add_sub_resource(test_if["number"], port_res)

        return AutoloadDetailsBuilder(resource).autoload_details()
