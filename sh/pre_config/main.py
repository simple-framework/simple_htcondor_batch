import argparse
import yaml
from files.config_50PC import BatchConfig
from files.timezone import TimeZone


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site_config', help="Compiled Site Level Configuration YAML file")
    parser.add_argument('--execution_id', help="ID of lightweight component")
    parser.add_argument('--output_dir', help="Output directory")
    args = parser.parse_args()
    return {
        'augmented_site_level_config_file': args.site_config,
        'execution_id': args.execution_id,
        'output_dir': args.output_dir
    }


if __name__ == "__main__":
    args = parse_args()
    execution_id = args['execution_id']
    augmented_site_level_config_file = args['augmented_site_level_config_file']
    output_dir = args['output_dir']

    augmented_site_level_config = yaml.safe_load(open(augmented_site_level_config_file, 'r'))

    config_50PC = BatchConfig("{output_dir}/50PC.conf".format(output_dir=output_dir), augmented_site_level_config, execution_id)
    config_50PC.generate_output_file()

    timezone = TimeZone("{output_dir}/timezone".format(output_dir=output_dir), augmented_site_level_config, execution_id)
    timezone.generate_output_file()
