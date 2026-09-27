from src.extractors import CSVExtractor as CSVE, APIExtractor as APIE
from src.transform import Transformer as T
from src.loaders import CSVLoader as CSVL
from src.pipeline import Pipeline

def main():
    # try:

    ## ** CSV to CSV **
    # Pipeline(CSVE.CSVExtractor(), T.Transformer(), CSVL.CSVLoader(), 'usuarios_erros.csv', 'data').run()
    Pipeline(CSVE.CSVExtractor(), T.Transformer(), CSVL.CSVLoader(), 'usuarios_erros copy.csv', 'data').run()

    api = 'https://jsonplaceholder.typicode.com/users'

    # Pipeline(APIE.APIExtractor(), T.Transformer(), CSVL.CSVLoader(), api, 'data').run()

    # except Exception as e:
    #     print(f'ERROR: {e}')

if __name__ == '__main__':
    main()
