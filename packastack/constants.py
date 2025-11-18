# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Constants and configuration values for packastack."""

import re

# URLs
TARBALLS_BASE_URL = "https://tarballs.opendev.org"
RELEASES_REPO_URL = "https://opendev.org/openstack/releases"
OPENDEV_BASE_URL = "https://opendev.org"
OPENSTACK_GIT_BASE_URL = f"{OPENDEV_BASE_URL}/openstack"
GITHUB_BASE_URL = "https://github.com"

# Launchpad
LAUNCHPAD_TEAM = "~ubuntu-openstack-dev"

# Directory names
PACKAGING_DIR = "packaging"
UPSTREAM_DIR = "upstream"
TARBALLS_DIR = "tarballs"
RELEASES_DIR = "releases"
LOGS_DIR = "logs"

# File paths (relative to releases repository)
SERIES_STATUS_PATH = "data/series_status.yaml"
SIGNING_KEY_INDEX_PATH = "doc/source/index.rst"
SIGNING_KEY_STATIC_DIR = "doc/source/static"

# Regex patterns
# Pattern to extract signing key ID from index.rst
# Matches lines like: "present...Cycle key...\n...key)`_" and extracts the key ID
SIGNING_KEY_PATTERN = re.compile(
    r"present.*Cycle key.*\n.*key\s*(?P<key>0x[0-9a-fA-F]+)`_", re.MULTILINE
)

# Pattern to match version tags
VERSION_TAG_PATTERN = re.compile(r"^(\d+\.)+\d+")
BETA_TAG_PATTERN = re.compile(r"^(\d+\.)+\d+\.0?b\d+$")
CANDIDATE_TAG_PATTERN = re.compile(r"^(\d+\.)+\d+\.0?rc\d+$")

# Branch names
PRISTINE_TAR_BRANCH = "pristine-tar"
UPSTREAM_BRANCH_PREFIX = "upstream"

# Git remote names
DEFAULT_REMOTE = "origin"

# Retry configuration
MAX_RETRY_ATTEMPTS = 3
RETRY_MIN_WAIT_SECONDS = 2
RETRY_MAX_WAIT_SECONDS = 10
RETRY_MULTIPLIER = 1

# Network timeouts (seconds)
CONNECT_TIMEOUT = 30
READ_TIMEOUT = 300

# Logging
ERROR_LOG_FILE = "import-errors.log"

# Upstream Git Repositories
UPSTREAM_GIT_REPOS = {
    "alembic":                          f"{GITHUB_BASE_URL}/sqlalchemy/alembic",
    "aodh":                             f"{OPENSTACK_GIT_BASE_URL}/aodh.git",
    "barbican":                         f"{OPENSTACK_GIT_BASE_URL}/barbican.git",
    "ceilometer":                       f"{OPENSTACK_GIT_BASE_URL}/ceilometer.git",
    "cinder":                           f"{OPENSTACK_GIT_BASE_URL}/cinder.git",
    "cloudkitty":                       f"{OPENSTACK_GIT_BASE_URL}/cloudkitty.git",
    "designate":                        f"{OPENSTACK_GIT_BASE_URL}/designate.git",
    "designate-dashboard":              f"{OPENSTACK_GIT_BASE_URL}/designate-dashboard.git",
    "git-review":                       f"{OPENSTACK_GIT_BASE_URL}/git-review.git",
    "glance":                           f"{OPENSTACK_GIT_BASE_URL}/glance.git",
    "gnocchi":                          f"{GITHUB_BASE_URL}/gnocchixyz/gnocchi.git",
    "heat":                             f"{OPENSTACK_GIT_BASE_URL}/heat.git",
    "heat-dashboard":                   f"{OPENSTACK_GIT_BASE_URL}/heat-dashboard.git",
    "horizon":                          f"{OPENSTACK_GIT_BASE_URL}/horizon.git",
    "ironic":                           f"{OPENSTACK_GIT_BASE_URL}/ironic.git",
    "ironic-inspector":                 f"{OPENSTACK_GIT_BASE_URL}/ironic-inspector.git",
    "ironic-ui":                        f"{OPENSTACK_GIT_BASE_URL}/ironic-ui.git",
    "keystone":                         f"{OPENSTACK_GIT_BASE_URL}/keystone.git",
    "magnum":                           f"{OPENSTACK_GIT_BASE_URL}/magnum.git",
    "magnum-ui":                        f"{OPENSTACK_GIT_BASE_URL}/magnum-ui.git",
    "manila":                           f"{OPENSTACK_GIT_BASE_URL}/manila.git",
    "manila-ui":                        f"{OPENSTACK_GIT_BASE_URL}/manila-ui.git",
    "masakari":                         f"{OPENSTACK_GIT_BASE_URL}/masakari.git",
    "masakari-dashboard":               f"{OPENSTACK_GIT_BASE_URL}/masakari-dashboard.git",
    "masakari-monitors":                f"{OPENSTACK_GIT_BASE_URL}/masakari-monitors.git",
    "mistral":                          f"{OPENSTACK_GIT_BASE_URL}/mistral.git",
    "mistral-dashboard":                f"{OPENSTACK_GIT_BASE_URL}/mistral-dashboard.git",
    "murano":                           f"{OPENSTACK_GIT_BASE_URL}/murano.git",
    "murano-agent":                     f"{OPENSTACK_GIT_BASE_URL}/murano-agent.git",
    "murano-dashboard":                 f"{OPENSTACK_GIT_BASE_URL}/murano-dashboard.git",
    "networking-arista":                f"{OPENDEV_BASE_URL}/x/networking-arista",
    "networking-bagpipe":               f"{OPENSTACK_GIT_BASE_URL}/networking-bagpipe.git",
    "networking-baremetal":             f"{OPENSTACK_GIT_BASE_URL}/networking-baremetal.git",
    "networking-bgpvpn":                f"{OPENSTACK_GIT_BASE_URL}/networking-bgpvpn.git",
    "networking-hyperv":                f"{OPENSTACK_GIT_BASE_URL}/networking-hyperv.git",
    "networking-l2gw":                  f"{OPENDEV_BASE_URL}/x/networking-l2gw.git",
    "networking-mlnx":                  f"{OPENDEV_BASE_URL}/x/networking-mlnx.git",
    "networking-odl":                   f"{OPENSTACK_GIT_BASE_URL}/networking-odl.git",
    "networking-ovn":                   f"{OPENSTACK_GIT_BASE_URL}/networking-ovn.git",
    "networking-sfc":                   f"{OPENSTACK_GIT_BASE_URL}/networking-sfc.git",
    "neutron":                          f"{OPENSTACK_GIT_BASE_URL}/neutron.git",
    "neutron-dynamic-routing":          f"{OPENSTACK_GIT_BASE_URL}/neutron-dynamic-routing.git",
    "neutron-fwaas":                    f"{OPENSTACK_GIT_BASE_URL}/neutron-fwaas.git",
    "neutron-fwaas-dashboard":          f"{OPENSTACK_GIT_BASE_URL}/neutron-fwaas-dashboard.git",
    "neutron-lbaas":                    f"{OPENSTACK_GIT_BASE_URL}/neutron-lbaas.git",
    "neutron-lbaas-dashboard":          f"{OPENSTACK_GIT_BASE_URL}/neutron-lbaas-dashboard.git",
    "neutron-taas":                     f"{OPENSTACK_GIT_BASE_URL}/neutron-taas.git",
    "neutron-vpnaas":                   f"{OPENSTACK_GIT_BASE_URL}/neutron-vpnaas.git",
    "neutron-vpnaas-dashboard":         f"{OPENSTACK_GIT_BASE_URL}/neutron-vpnaas-dashboard.git",
    "nova":                             f"{OPENSTACK_GIT_BASE_URL}/nova.git",
    "octavia":                          f"{OPENSTACK_GIT_BASE_URL}/octavia.git",
    "octavia-dashboard":                f"{OPENSTACK_GIT_BASE_URL}/octavia-dashboard.git",
    "openstack-pkg-tools":              f"{OPENSTACK_GIT_BASE_URL}/openstack-pkg-tools.git",
    "openstack-release":                f"{OPENSTACK_GIT_BASE_URL}/openstack-release.git",
    "openstack-trove":                  f"{OPENSTACK_GIT_BASE_URL}/openstack-trove.git",
    "ovn-bgp-agent":                    f"{OPENSTACK_GIT_BASE_URL}/ovn-bgp-agent.git",
    "ovn-octavia-provider":             f"{OPENSTACK_GIT_BASE_URL}/ovn-octavia-provider.git",
    "panko":                            f"{OPENSTACK_GIT_BASE_URL}/panko.git",
    "pg8000":                           f"{GITHUB_BASE_URL}/mfenniak/pg8000.git",
    "placement":                        f"{OPENSTACK_GIT_BASE_URL}/placement.git",
    "pydeb-cookiecutter":               f"{OPENSTACK_GIT_BASE_URL}/pydeb-cookiecutter.git",
    "python-aodhclient":                f"{OPENSTACK_GIT_BASE_URL}/python-aodhclient.git",
    "python-automaton":                 f"{OPENSTACK_GIT_BASE_URL}/automaton.git",
    "python-barbicanclient":            f"{OPENSTACK_GIT_BASE_URL}/python-barbicanclient.git",
    "python-binary-memcached":          f"{GITHUB_BASE_URL}/jaysonsantos/python-binary-memcached.git",
    "python-blazarclient":              f"{OPENSTACK_GIT_BASE_URL}/python-blazarclient.git",
    "python-castellan":                 f"{OPENSTACK_GIT_BASE_URL}/castellan.git",
    "python-ceilometerclient":          f"{OPENSTACK_GIT_BASE_URL}/python-ceilometerclient.git",
    "python-ceilometermiddleware":      f"{OPENSTACK_GIT_BASE_URL}/ceilometermiddleware.git",
    "python-cinderclient":              f"{OPENSTACK_GIT_BASE_URL}/python-cinderclient.git",
    "python-cliff":                     f"{OPENSTACK_GIT_BASE_URL}/cliff.git",
    "python-designateclient":           f"{OPENSTACK_GIT_BASE_URL}/python-designateclient.git",
    "python-diskimage-builder":         f"{OPENSTACK_GIT_BASE_URL}/diskimage-builder.git",
    "python-dracclient":                f"{OPENSTACK_GIT_BASE_URL}/dracclient.git",
    "python-glanceclient":              f"{OPENSTACK_GIT_BASE_URL}/python-glanceclient.git",
    "python-glance-store":              f"{OPENSTACK_GIT_BASE_URL}/glance-store.git",
    "python-gnocchiclient":             f"{OPENSTACK_GIT_BASE_URL}/python-gnocchiclient.git",
    "python-heatclient":                f"{OPENSTACK_GIT_BASE_URL}/python-heatclient.git",
    "python-ibmcclient":                f"{GITHUB_BASE_URL}/IamFive/python-ibmcclient.git",
    "python-ironicclient":              f"{OPENSTACK_GIT_BASE_URL}/python-ironicclient.git",
    "python-ironic-inspector-client":   f"{OPENSTACK_GIT_BASE_URL}/ironic-inspector-client.git",
    "python-ironic-lib":                f"{OPENSTACK_GIT_BASE_URL}/ironic-lib.git",
    "python-keystoneauth1":             f"{OPENSTACK_GIT_BASE_URL}/keystoneauth1.git",
    "python-keystoneclient":            f"{OPENSTACK_GIT_BASE_URL}/python-keystoneclient.git",
    "python-keystonemiddleware":        f"{OPENSTACK_GIT_BASE_URL}/keystonemiddleware.git",
    "python-libjuju":                   f"{GITHUB_BASE_URL}/juju/python-libjuju.git",
    "python-magnumclient":              f"{OPENSTACK_GIT_BASE_URL}/python-magnumclient.git",
    "python-manilaclient":              f"{OPENSTACK_GIT_BASE_URL}/python-manilaclient.git",
    "python-masakariclient":            f"{OPENSTACK_GIT_BASE_URL}/python-masakariclient.git",
    "python-mistralclient":             f"{OPENSTACK_GIT_BASE_URL}/python-mistralclient.git",
    "python-mistral-lib":               f"{OPENSTACK_GIT_BASE_URL}/mistral-lib.git",
    "python-monascaclient":             f"{OPENSTACK_GIT_BASE_URL}/python-monascaclient.git",
    "python-monasca-statsd":            f"{OPENSTACK_GIT_BASE_URL}/monasca-statsd.git",
    "python-muranoclient":              f"{OPENSTACK_GIT_BASE_URL}/python-muranoclient.git",
    "python-neutronclient":             f"{OPENSTACK_GIT_BASE_URL}/python-neutronclient.git",
    "python-neutron-lib":               f"{OPENSTACK_GIT_BASE_URL}/neutron-lib.git",
    "python-novaclient":                f"{OPENSTACK_GIT_BASE_URL}/python-novaclient.git",
    "python-observabilityclient":       f"{OPENSTACK_GIT_BASE_URL}/python-observabilityclient.git",
    "python-octaviaclient":             f"{OPENSTACK_GIT_BASE_URL}/python-octaviaclient.git",
    "python-octavia-lib":               f"{OPENSTACK_GIT_BASE_URL}/octavia-lib.git",
    "python-openstackclient":           f"{OPENSTACK_GIT_BASE_URL}/python-openstackclient.git",
    "python-openstackdocstheme":        f"{OPENSTACK_GIT_BASE_URL}/openstackdocstheme.git",
    "python-openstacksdk":              f"{OPENSTACK_GIT_BASE_URL}/openstacksdk.git",
    "python-os-api-ref":                f"{OPENSTACK_GIT_BASE_URL}/os-api-ref.git",
    "python-os-brick":                  f"{OPENSTACK_GIT_BASE_URL}/os-brick.git",
    "python-osc-lib":                   f"{OPENSTACK_GIT_BASE_URL}/osc-lib.git",
    "python-os-client-config":          f"{OPENSTACK_GIT_BASE_URL}/os-client-config.git",
    "python-osc-placement":             f"{OPENSTACK_GIT_BASE_URL}/osc-placement.git",
    "python-os-ken":                    f"{OPENSTACK_GIT_BASE_URL}/os-ken.git",
    "python-oslo.cache":                f"{OPENSTACK_GIT_BASE_URL}/oslo.cache.git",
    "python-oslo.concurrency":          f"{OPENSTACK_GIT_BASE_URL}/oslo.concurrency.git",
    "python-oslo.config":               f"{OPENSTACK_GIT_BASE_URL}/oslo.config.git",
    "python-oslo.context":              f"{OPENSTACK_GIT_BASE_URL}/oslo.context.git",
    "python-oslo.db":                   f"{OPENSTACK_GIT_BASE_URL}/oslo.db.git",
    "python-oslo.i18n":                 f"{OPENSTACK_GIT_BASE_URL}/oslo.i18n.git",
    "python-oslo.limit":                f"{OPENSTACK_GIT_BASE_URL}/oslo.limit.git",
    "python-oslo.log":                  f"{OPENSTACK_GIT_BASE_URL}/oslo.log.git",
    "python-oslo.messaging":            f"{OPENSTACK_GIT_BASE_URL}/oslo.messaging.git",
    "python-oslo.metrics":              f"{OPENSTACK_GIT_BASE_URL}/oslo.metrics.git",
    "python-oslo.middleware":           f"{OPENSTACK_GIT_BASE_URL}/oslo.middleware.git",
    "python-oslo.policy":               f"{OPENSTACK_GIT_BASE_URL}/oslo.policy.git",
    "python-oslo.privsep":              f"{OPENSTACK_GIT_BASE_URL}/oslo.privsep.git",
    "python-oslo.reports":              f"{OPENSTACK_GIT_BASE_URL}/oslo.reports.git",
    "python-oslo.rootwrap":             f"{OPENSTACK_GIT_BASE_URL}/oslo.rootwrap.git",
    "python-oslo.serialization":        f"{OPENSTACK_GIT_BASE_URL}/oslo.serialization.git",
    "python-oslo.service":              f"{OPENSTACK_GIT_BASE_URL}/oslo.service.git",
    "python-oslotest":                  f"{OPENSTACK_GIT_BASE_URL}/oslotest.git",
    "python-oslo.upgradecheck":         f"{OPENSTACK_GIT_BASE_URL}/oslo.upgradecheck.git",
    "python-oslo.utils":                f"{OPENSTACK_GIT_BASE_URL}/oslo.utils.git",
    "python-oslo.versionedobjects":     f"{OPENSTACK_GIT_BASE_URL}/oslo.versionedobjects.git",
    "python-oslo.vmware":               f"{OPENSTACK_GIT_BASE_URL}/oslo.vmware.git",
    "python-osprofiler":                f"{OPENSTACK_GIT_BASE_URL}/osprofiler.git",
    "python-os-resource-classes":       f"{OPENSTACK_GIT_BASE_URL}/os-resource-classes.git",
    "python-os-service-types":          f"{OPENSTACK_GIT_BASE_URL}/os-service-types.git",
    "python-os-testr":                  f"{OPENSTACK_GIT_BASE_URL}/os-testr.git",
    "python-os-traits":                 f"{OPENSTACK_GIT_BASE_URL}/os-traits.git",
    "python-os-vif":                    f"{OPENSTACK_GIT_BASE_URL}/os-vif.git",
    "python-os-win":                    f"{OPENSTACK_GIT_BASE_URL}/os-win.git",
    "python-os-xenapi":                 f"{OPENSTACK_GIT_BASE_URL}/os-xenapi.git",
    "python-ovsdbapp":                  f"{OPENSTACK_GIT_BASE_URL}/ovsdbapp.git",
    "python-pankoclient":               f"{OPENSTACK_GIT_BASE_URL}/python-pankoclient.git",
    "python-pbr":                       f"{OPENSTACK_GIT_BASE_URL}/pbr.git",
    "python-proliantutils":             f"{OPENDEV_BASE_URL}/x/proliantutils",
    # TODO(wolsen) Need to check on this one
    "python-purestorage":               f"{GITHUB_BASE_URL}/PureStorage-OpenConnect/rest-client.git",
    "python-pyasyncore":                f"{GITHUB_BASE_URL}/simonrob/pyasyncore.git",
    "python-pycdlib":                   f"{GITHUB_BASE_URL}/clalancette/pycdlib.git",
    "python-qinlingclient":             f"{OPENSTACK_GIT_BASE_URL}/python-qinlingclient.git",
    "python-saharaclient":              f"{OPENSTACK_GIT_BASE_URL}/saharaclient.git",
    "python-scciclient":                f"{OPENDEV_BASE_URL}/x/python-scciclient.git",
    "python-searchlightclient":         f"{OPENSTACK_GIT_BASE_URL}/searchlightclient.git",
    "python-senlinclient":              f"{OPENSTACK_GIT_BASE_URL}/senlinclient.git",
    "python-sushy":                     f"{OPENSTACK_GIT_BASE_URL}/sushy.git",
    "python-sushy-oem-idrac":           f"{OPENDEV_BASE_URL}/x/sushy-oem-idrac.git",
    "python-swiftclient":               f"{OPENSTACK_GIT_BASE_URL}/swiftclient.git",
    "python-tackerclient":              f"{OPENSTACK_GIT_BASE_URL}/tackerclient.git",
    "python-taskflow":                  f"{OPENSTACK_GIT_BASE_URL}/taskflow.git",
    "python-tooz":                      f"{OPENSTACK_GIT_BASE_URL}/tooz.git",
    "python-troveclient":               f"{OPENSTACK_GIT_BASE_URL}/troveclient.git",
    "python-vitrageclient":             f"{OPENSTACK_GIT_BASE_URL}/vitrageclient.git",
    "python-vmware-nsxlib":             f"{OPENDEV_BASE_URL}/x/vmware-nsxlib.git",
    "python-watcherclient":             f"{OPENSTACK_GIT_BASE_URL}/watcherclient.git",
    # TODO(wolsen) Where does this one come from?
    # "python-xclarityclient":            f"{OPENSTACK_GIT_BASE_URL}/xclarityclient.git",
    "python-zaqarclient":               f"{OPENSTACK_GIT_BASE_URL}/python-zaqarclient.git",
    "python-zunclient":                 f"{OPENSTACK_GIT_BASE_URL}/python-zunclient.git",
    # TODO(wolsen) Need to update the homepage in debian/control
    "rally":                            f"{OPENSTACK_GIT_BASE_URL}/rally.git",
    "sahara":                           f"{OPENSTACK_GIT_BASE_URL}/sahara.git",
    "sahara-dashboard":                 f"{OPENSTACK_GIT_BASE_URL}/sahara-dashboard.git",
    "sahara-plugin-spark":              f"{OPENSTACK_GIT_BASE_URL}/sahara-plugin-spark.git",
    "sahara-plugin-vanilla":            f"{OPENSTACK_GIT_BASE_URL}/sahara-plugin-vanilla.git",
    "senlin":                           f"{OPENSTACK_GIT_BASE_URL}/senlin.git",
    "sqlalchemy":                       f"{OPENSTACK_GIT_BASE_URL}/sqlalchemy.git",
    "stevedore":                        f"{OPENSTACK_GIT_BASE_URL}/stevedore.git",
    "swift":                            f"{OPENSTACK_GIT_BASE_URL}/swift.git",
    "trove-dashboard":                  f"{OPENSTACK_GIT_BASE_URL}/trove-dashboard.git",
    "ubuntu-openstack-metadata":        f"{OPENSTACK_GIT_BASE_URL}/ubuntu-openstack-metadata.git",
    "virtualbmc":                       f"{OPENSTACK_GIT_BASE_URL}/virtualbmc.git",
    "vitrage":                          f"{OPENSTACK_GIT_BASE_URL}/vitrage.git",
    "vmware-nsx":                       f"{OPENDEV_BASE_URL}/x/vmware-nsx.git",
    "watcher":                          f"{OPENSTACK_GIT_BASE_URL}/watcher.git",
    "watcher-dashboard":                f"{OPENSTACK_GIT_BASE_URL}/watcher-dashboard.git",
    "zaqar":                            f"{OPENSTACK_GIT_BASE_URL}/zaqar.git",
    "zaqar-ui":                         f"{OPENSTACK_GIT_BASE_URL}/zaqar-ui.git",
    # Note(wolsen): This really should be point to https://github.com/openmainframeproject/feilong
    "zvmcloudconnector":                f"{OPENSTACK_GIT_BASE_URL}/zvmcloudconnector.git",
}

DEPRECATED_PACKAGES = {
    "pg8000",
    "python-pyasyncore",
    "python-qinlingclient",
    "python-pankoclient",
    "sahara",
    "saharah-dashboard",
    "sahara-plugin-spark",
    "sahara-plugin-vanilla",
    "senlin",
}
