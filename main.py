from src.pipeline import Pipeline

def main():

    # Pipeline('config/csv_to_csv.json').run()
    # Pipeline('config/sqlite.json').run()
    Pipeline('config/pipeline.json').run()
    # Pipeline('config/json_to_some.json').run()

if __name__ == '__main__':
    main()
