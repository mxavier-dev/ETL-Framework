from src.pipeline import Pipeline
from utils.logger import logger

def main():
    try:
        Pipeline('config/csv_to_csv.json').run()
        # Pipeline('config/sqlite.json').run()
        # Pipeline('config/pipeline.json').run()
        # Pipeline('config/json_to_some.json').run()
    except Exception:
        logger.exception('ETL execution failed')

if __name__ == '__main__':
    main()
