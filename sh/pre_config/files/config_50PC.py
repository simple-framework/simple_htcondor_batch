from models.config_file import ConfigFile
from helpers.generic_helpers import get_dns_info


class BatchConfig(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        execution_id = self.lightweight_component['execution_id']
        dns = get_dns_info(self.augmented_site_level_config, execution_id)
        allow_write = '.'.join((dns['container_ip'].split('.')[0:-2] + ['*']))
        self.advanced_category.add("Use ROLE: CentralManager\n")
        self.advanced_category.add_key_value("condor_host", dns['container_ip'])
        self.advanced_category.add_key_value("allow_write", allow_write)
