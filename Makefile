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
        create-network $(PACKAGE_STORE)/alu-sr-cli-3.4	 1

#all: netsim ncs
all: netsim ncs

netsim:
	ncs-netsim --dir netsim $(NETWORK)
#	cp initial_data/ios.xml netsim/ce/ce0/cdb

ncs:
	ncs-setup --netsim-dir netsim --dest .
#	cp initial_data/topology.xml ncs-cdb
	ncs-netsim ncs-xml-init > ncs-cdb/netsim_devices_init.xml
start:
	ncs-netsim start
	ncs

clean:
	rm -rf netsim running.DB logs state ncs-cdb *.trace
	rm -f packages/alu-sr-cli-3.4
	rm -f packages/cisco-ios-cli-3.8
	rm -f packages/cisco-iosxr-cli-3.5
	rm -f packages/juniper-junos-nc-3.0
	rm -rf bin
