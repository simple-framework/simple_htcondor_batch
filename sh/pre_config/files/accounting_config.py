from models.config_file import ConfigFile
from helpers.generic_helpers import *


class AccountingConfig(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_lightweight_component_queried_parameters(self):
        super().add_lightweight_component_queried_parameters()
        self.lightweight_component_queried_category.add_key_value_query("PRIORITY_HALFLIFE", "$.config.priority_halflife")
        self.lightweight_component_queried_category.add_key_value_query("GROUP_AUTOREGROUP", "$.config.group_autoregroup")

    def add_advanced_parameters(self):
        super().add_advanced_parameters()

        accept_surplus = self.lightweight_component['config']['group_accept_surplus']
        if accept_surplus:
            self.advanced_category.add_key_value("GROUP_ACCEPT_SURPLUS", "True")
            # Calculate the surplus allocated to each group correctly"
            self.advanced_category.add_key_value("NEGOTIATOR_USE_WEIGHTED_DEMAND", "True")
            self.advanced_category.add_key_value("NEGOTIATOR_ALLOW_QUOTA_OVERSUBSCRIPTION", "False")
        group_names_quotas = {}
        # VO Based Accounting, FQAN based sub accounting
        supported_vos = get_supported_vos_with_quotas(self.augmented_site_level_config)

        for vo in supported_vos:
            name = vo['name']
            quota = vo['quota']
            group_names_quotas[f"group_{name}"] = quota
            fqans = get_fqan_for_vo(name, self.augmented_site_level_config,self.lightweight_component)
            fqans = get_quotas_for_fqans(fqans)
            for fqan in fqans:
                acct_group = generate_acct_group_for_fqan(name, fqan["voms_fqan"])
                group_names_quotas[acct_group] = fqan["quota"]

        self.advanced_category.add_key_value("GROUP_NAMES", ", \\\n\t".join(group_names_quotas.keys()))
        for acct_group, quota in group_names_quotas.items():
            self.advanced_category.add_key_value(f"GROUP_QUOTA_DYNAMIC_{acct_group}", quota)

