import mock
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

from driver import TeraVMChassisDriver

address = '192.168.42.209'

user = 'admin'
password = 'admin'
port = 443
scheme = "https"
auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
api_port = 8029

context = ResourceCommandContext()
context.resource = ResourceContextDetails()
context.resource.name = 'TVM Chassis'
context.resource.fullname = 'TeraVM Chassis'
context.reservation = ReservationContextDetails()
context.reservation.reservation_id = 'b18fb3d1-5f08-4002-9cf2-c519ac3edfa6'
context.resource.attributes = {}
# context.resource.attributes['User'] = user
# context.resource.attributes['Password'] = password
context.resource.attributes["Traffic TeraVM 2G.Controller TCP Port"] = "443"
context.resource.address = address

context.connectivity = mock.MagicMock()
context.connectivity.server_address = "192.168.85.32"

dr = TeraVMChassisDriver()


# with mock.patch('driver.get_api') as get_api:
#     get_api.return_value = type('api', (object,), {
#         'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

out = dr.get_inventory(context)

for xx in out.resources:
    print xx.__dict__

print(out)
