from models.config_file import ConfigFile


class BatchConfig(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)


    def add_static_parameters(self):
        super().add_static_parameters()
        self.static_category.add_key_value("Use Role", "CentralManager")


    def add_lightweight_component_queried_parameters(self):
        super().add_lightweight_component_queried_parameters()
        self.lightweight_component_queried_category.add_key_value_query("CONDOR_HOST", "$.deploy.node")
        self.lightweight_component_queried_category.add_key_value_query("ALLOW_WRITE", "$.config.allow_write")

    def add_advanced_parameters(self):
        pass