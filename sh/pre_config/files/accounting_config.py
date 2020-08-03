from models.config_file import ConfigFile
from helpers.generic_helpers import get_dns_info


class AccountingConfig(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()
        self.static_category.add("# Priority halflife is 24h")
        self.static_category.add_key_value("PRIORTIY_HALFLIFE", "86400")

        self.static_category.add("# Allow groups to use more than fs")
        self.static_category.add_key_value("GROUP_AUTOREGROUP", "True")
        self.static_category.add_key_value("GROUP_ACCEPT_SURPLUS", "True")

        self.static_category.add("# Calculate the surplus allocated to each group correctly")
        self.static_category.add_key_value("NEGOTIATOR_USE_WEIGHTED_DEMAND", "True")


    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        execution_id = self.lightweight_component['execution_id']

