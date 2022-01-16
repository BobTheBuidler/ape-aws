import boto3
from typing import Optional, Dict


class AwsNode:
    '''
    Creates AWS node on a specified blockchain network
    Will run as is, no parameters necessary
    :param
        'ClientRequestToken': str
        'NetworkId': str
            Available networks:
                -'n-ethereum-rinkeby' (Default)
                -'n-ethereum-mainnet'
                -'n-ethereum-ropsten'
        'MemberId': str
        'InstanceType': str
            Available Instances:
                -'bc.t3.large' (default)
                -TODO
        'AvailabilityZone': str
            Available Zones:
                -'us-east-1a' (default)
                -TODO
        'chain_code_logs': bool (default False)
        'peer_logs': bool (default False)
        'StateDB': str
        'Tags': dict
    '''

    def __init__(
            self,
            chain_code_logs: bool = False,
            peer_logs: bool = False,
            *args,
            **kwargs,
    ):
        self.args = args
        self.client = boto3.client('managedblockchain')
        self.network_id = 'n-ethereum-rinkeby'
        self.instance_type = 'bc.t3.large'
        self.availability_zone = 'us-east-1a'
        self.chain_code_logs = chain_code_logs
        self.peer_logs = peer_logs
        self.kwarg_config = {}
        if 'ClientRequestToken' in kwargs:
            self.kwarg_config['ClientRequestToken'] = kwargs['ClientRequestToken']
        self.kwarg_config['NetworkId'] = self.network_id
        if 'NetworkId' in kwargs:
            self.kwarg_config['NetworkId'] = kwargs['NetworkId']
        elif 'MemberId' in kwargs:
            self.kwarg_config['MemberId'] = kwargs['MemberId']
        elif 'InstanceType' in kwargs:
            self.instance_type = kwargs['InstanceType']
        elif 'AvailabilityZone' in kwargs:
            self.availability_zone = kwargs['AvailabilityZone']
        self.node_dict = self.create_node_config_kwargs()
        if self.chain_code_logs is True or self.peer_logs is True:
            self.node_dict["LogPublishingConfiguration"] = self.create_logs_kwargs()
        if 'StateDB' in kwargs:
            self.node_dict["StateDB"] = kwargs['StateDB']
        self.kwarg_config['NodeConfiguration'] = self.node_dict
        if 'Tags' in kwargs:
            self.kwarg_config['Tags'] = kwargs['Tags']

    def create_node_config_kwargs(self) -> Dict:
        return {
            "InstanceType": self.instance_type,
            "AvailabilityZone": self.availability_zone
        }

    def create_logs_kwargs(self) -> Dict:
        return {
            'Fabric': {
                'ChaincodeLogs': {
                    'Cloudwatch': {
                        'Enabled': self.chain_code_logs
                    }
                },
                'Peerlogs': {
                    'Cloudwatch': {
                        'Enabled': self.peer_logs
                    }
                }
            }
        }

    def create_node(self):
        return self.client.create_node(**self.kwarg_config)
