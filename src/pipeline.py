class Pipeline:
    def __init__(self, extractor, transformer, loader, source, destination):
        self.extract = extractor
        self.transform = transformer
        self.load = loader
        self.source = source
        self.destination = destination

    def run(self):
        data = self.extract.extractor(self.source)
        t = self.transform.transform(data)
        self.load.loader(t, self.destination)
        print(f'Extract data: {len(data)}')
        print(f'Loaded data: {len(t)}')

