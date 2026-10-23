from src.pipeline import Pipeline
from utils.logger import logger

def main():
    try:
        Pipeline('config/file.json')
    except Exception:
        logger.exception('ETL execution failed')

if __name__ == '__main__':
    main()
