# The order of packages is significant as there are dependencies between
# the packages. Typically generated namespaces are used by other packages.
#PACKAGES = l3vpn l3vpnui

# Directory of example packages
PACKAGE_STORE=$(NCS_DIR)/packages/neds

# The create-network argument to ncs-netsim
NETWORK = \
        create-network $(PACKAGE_STORE)/cisco-ios-cli-3.8	 2 ios \
        create-network $(PACKAGE_STORE)/cisco-iosxr-cli-3.5	 2 xr \
        create-network $(PACKAGE_STORE)/juniper-junos-nc-3.0	 2 j \
        create-network $(PACKAGE_STORE)/alu-sr-cli-3.4	 2 a

#all: netsim ncs
all: netsim ncs

netsim:
	ncs-netsim --dir netsim $(NETWORK)
	cp initial_data/ios0-ip-access-lists.xml netsim/ios/ios0/cdb
	cp initial_data/xr0-ipv4-access-list.xml netsim/xr/xr0/cdb

ncs:
	ncs-setup --netsim-dir netsim --dest .
	cp initial_data/baseline-tpl.xml ncs-cdb
	cp initial_data/security-policy-tpl.xml ncs-cdb
	ncs-netsim ncs-xml-init > ncs-cdb/netsim_devices_init.xml

start:	all
	ncs-netsim start
	ncs

stop:
	-ncs-netsim stop
	-ncs --stop

clean:
	rm -rf netsim running.DB logs state ncs-cdb *.trace
	rm -f packages/alu-sr-cli-3.4
	rm -f packages/cisco-ios-cli-3.8
	rm -f packages/cisco-iosxr-cli-3.5
	rm -f packages/juniper-junos-nc-3.0
	rm -rf bin
