from src.extractors.CSVExtractor import CSVExtractor
from src.transform.Transformer import Transformer
from src.loaders.CSVLoader import CSVLoader
from src.pipeline import Pipeline

def main():
    # try:

    csv_path = 'usuarios_erros.csv'
    t_path = 'data'
    Pipeline(CSVExtractor(), Transformer(), CSVLoader(), csv_path, t_path).run()

    # except Exception as e:
    #     print(f'ERROR: {e}')

if __name__ == '__main__':
    main()
