from src.config.load_json import load_json
from src.config.config_validator import validate_config
from src.config.schema_validator import validate_schema
from src.factories.extractor_factory import create_extractor
from src.factories.loader_factory import create_loader
from src.transform.Transformer import Transformer
from utils.logger import logger

class Pipeline:
    def __init__(self, config: str):

            config = load_json(config)
            validate_config(config)

            self.schema = load_json(f'schemas/{config["schema"]}.json')
            validate_schema(self.schema)

            self.extractor = create_extractor(config['extractor'])
            self.source = config['source']
            self.loader = create_loader(config['loader'])
            self.destination = (config['destination']
                                if not config.get('table')
                                else (config['destination'], config['table']))
            self.transformer = Transformer()
            self.remove_duplicates = config.get('remove_duplicates')


    def run(self):

            logger.info('Pipeline started')
            logger.info(f'Extracting data from "{self.source}"')

            data = self.extractor.extract(self.source)
            logger.info(f'Extracted {len(data)} records')

            logger.info('Transforming data')
            transformed = self.transformer.transform(data, self.schema, self.remove_duplicates)

            logger.info(f'Loading data into "{self.destination}"')
            self.loader.load(transformed, self.destination, self.schema)

            logger.info(f'Loaded {len(transformed)} records')
            logger.info('Pipeline finished')
