# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        template_vars = ncs.template.Variables()

        if service.continent == 'North America':
            template_vars.add('PRIMARY_NTP_SERVER_IP', '1.1.1.1')
            template_vars.add('SECONDARY_NTP_SERVER_IP', '11.11.11.11')
        elif service.continent == 'South America':
            template_vars.add('PRIMARY_NTP_SERVER_IP', '2.2.2.2')
            template_vars.add('SECONDARY_NTP_SERVER_IP', '22.22.22.22')
        elif service.continent == 'Europe':
            template_vars.add('PRIMARY_NTP_SERVER_IP', '3.3.3.3')
            template_vars.add('SECONDARY_NTP_SERVER_IP', '33.33.33.33')
        elif service.continent == 'Asia':
            template_vars.add('PRIMARY_NTP_SERVER_IP', '4.4.4.4')
            template_vars.add('SECONDARY_NTP_SERVER_IP', '44.44.44.44')
        elif service.continent == 'Australia':
            template_vars.add('PRIMARY_NTP_SERVER_IP', '5.5.5.5')
            template_vars.add('SECONDARY_NTP_SERVER_IP', '55.55.55.55')
        # need default setting here

        template = ncs.template.Template(service)
        template.apply('ntp-config-tpl', template_vars)

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service postmod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('ntp-config-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
