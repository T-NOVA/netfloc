from oslo_log import log as logging
from heat.engine import properties
from heat.engine import resource
from gettext import gettext as _
import requests
import json
import time
from time import sleep

LOG = logging.getLogger(__name__)

__author__ = 'traj'


class ChainCreate(resource.Resource):
    PROPERTIES = (
        SENDER_SFC_PORT,
        VNF_IN_PORT,
        VNF_OUT_PORT,
        RECEIVER_SFC_PORT,
        ODL_USERNAME,
        ODL_PASSWORD,
        NETFLOC_IP_PORT) = (
        'sender_sfc_port',
        'vnf_in_port',
        'vnf_out_port',
        'receiver_sfc_port',
        'odl_username',
        'odl_password',
        'netfloc_ip_port')

    properties_schema = {
        SENDER_SFC_PORT: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('SFC port of sender VM'),
            required=True
        ),
        VNF_IN_PORT: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('SFC ingress port of VNF'),
            required=True
        ),
        VNF_OUT_PORT: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('SFC egress port of VNF'),
            required=True
        ),
        RECEIVER_SFC_PORT: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('SFC port of receiver VM'),
            required=True
        ),
        ODL_USERNAME: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('User name to be configured for ODL Restconf access'),
            required=True
        ),
        ODL_PASSWORD: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('Password to be set for ODL Restconf access'),
            required=True
        ),
        NETFLOC_IP_PORT: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('IP and port of the Netfloc node'),
            required=True
        )
    }

    def handle_create(self):
        # Time until dependent resources are created.
        # Can vary for different environments (preliminary).
        time.sleep(15)
        sender_sfc_port = self.properties.get(self.SENDER_SFC_PORT)
        vnf_in_port = self.properties.get(self.VNF_IN_PORT)
        vnf_out_port = self.properties.get(self.VNF_OUT_PORT)
        receiver_sfc_port = self.properties.get(self.RECEIVER_SFC_PORT)
        odl_username = self.properties.get(self.ODL_USERNAME)
        odl_password = self.properties.get(self.ODL_PASSWORD)
        netfloc_ip_port = self.properties.get(self.NETFLOC_IP_PORT)

        ports = "%s,%s,%s,%s" % (sender_sfc_port, vnf_in_port, vnf_out_port, receiver_sfc_port)

        create_url = 'restconf/operations/netfloc:create-service-chain'

        url = "%s%s:%s@%s/%s" % ('http://', odl_username, odl_password, netfloc_ip_port, create_url)

        ports_dict = {"input": {"neutron-ports": str(ports)}}

        headers = {'Content-type': 'application/json'}

        LOG.debug('CHAIN_PORTS %s', ports_dict)

        try:

            req = requests.post(url, data=json.dumps(ports_dict), headers=headers)

            if req.json()['output']:
                chainID = req.json()['output']['service-chain-id']

                self.resource_id_set(chainID)

                LOG.debug('chainID %s', chainID)

                return chainID

        except Exception as ex:

            LOG.warn("Failed to fetch chain ID: %s", ex)


class ChainDelete(resource.Resource):
    PROPERTIES = (
        CHAIN_ID,
        ODL_USERNAME,
        ODL_PASSWORD,
        NETFLOC_URL) = (
        'chain_id',
        'odl_username',
        'odl_password',
        'netfloc_url')

    properties_schema = {
        CHAIN_ID: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('ID of the created chain'),
            required=True
        ),
        ODL_USERNAME: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('User name to be configured for ODL Restconf access'),
            required=True
        ),
        ODL_PASSWORD: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('Password to be set for ODL Restconf access'),
            required=True
        ),
        NETFLOC_IP_PORT: properties.Schema(
            data_type=properties.Schema.STRING,
            description=_('IP and port of the Netfloc node'),
            required=True
        )
    }

    def handle_create(self):
        chain_id = self.properties.get(self.CHAIN_ID)
        odl_username = self.properties.get(self.ODL_USERNAME)
        odl_password = self.properties.get(self.ODL_PASSWORD)
        netfloc_ip_port = self.properties.get(self.NETFLOC_IP_PORT)

        delete_url = 'restconf/operations/netfloc:delete-service-chain'

        url = "%s%s:%s@%s/%s" % ('http://', odl_username, odl_password, netfloc_ip_port, delete_url)

        headers = {'Content-type': 'application/json'}

        body = {"input": {"service-chain-id": str(chain_id)}}

        try:

            req = requests.post(url, data=json.dumps(body), headers=headers)

            if req.json()['output']:
                chainID = req.json()['output']['service-chain-id']

                return req.status_code

        except Exception as ex:

            LOG.warn("Failed to delete chain: %s", ex)


def resource_mapping():
    mappings = {}
    mappings['Netfloc::Chain::Create'] = ChainCreate
    mappings['Netfloc::Chain::Delete'] = ChainDelete
    return mappings