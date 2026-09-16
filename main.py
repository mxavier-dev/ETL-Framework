from src.extractors.csv import CSVExtractor
from src.transform.base import Transformer
from src.loaders.csv import CSVLoader
from src.pipeline import Pipeline

def main():
    # try:

    csv_path = 'data/usuarios_erros.csv'
    t_path = 'data'
    Pipeline(CSVExtractor(), Transformer(), CSVLoader(), csv_path, t_path).run()

    # except Exception as e:
    #     print(f'ERROR: {e}')

if __name__ == '__main__':
    main()
