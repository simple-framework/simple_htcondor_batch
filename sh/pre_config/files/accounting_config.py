from models.config_file import ConfigFile
from helpers.generic_helpers import *


class AccountingConfig(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()
        # Priority halflife is 24h
        self.static_category.add_key_value("PRIORTIY_HALFLIFE", "86400")

        # Allow groups to use more than fs
        self.static_category.add_key_value("GROUP_AUTOREGROUP", "True")

        self.static_category.add_key_value("GROUP_ACCEPT_SURPLUS", "True")
        # Calculate the surplus allocated to each group correctly"
        self.static_category.add_key_value("NEGOTIATOR_USE_WEIGHTED_DEMAND", "True")
        self.static_category.add_key_value("NEGOTIATOR_ALLOW_QUOTA_OVERSUBSCRIPTION", "False")

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        group_names_quotas = {}
        voms_config = get_voms_config(self.augmented_site_level_config, self.lightweight_component)

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

