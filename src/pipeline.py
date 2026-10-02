from src.config.load_json import load_json
from src.factories.extractor_factory import create_extractor
from src.factories.loader_factory import create_loader
from src.transform.Transformer import Transformer

class Pipeline:
    def __init__(self, config):
        config = load_json(config)

        self.schema = load_json(f'schemas/{config["schema"]}.json')
        self.extractor = create_extractor(config['extractor'])
        self.source = config['source']
        self.loader = create_loader(config['loader'])
        self.destination = config['destination']
        self.transformer = Transformer()

    def run(self):
        data = self.extractor.extract(self.source)
        transformed = self.transformer.transform(data, self.schema)
        self.loader.load(transformed, self.destination, self.schema)
        
        print(f'Extract data: {len(data)}')
        print(f'Loaded data: {len(transformed)}')

