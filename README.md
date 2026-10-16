# ⚙️ ETL Framework

A configurable and extensible **ETL framework built with Python** to extract data from CSV files, JSON files, and APIs, transform records using JSON schemas, and load the results into CSV files or SQLite databases.

The project explores modular ETL architecture, object-oriented programming, reusable components, and schema-driven data transformation.

> 🚧 **Project status:** Under development. Features and configuration options may evolve.

## ✨ Features

- **Multiple data sources:** CSV, JSON, and HTTP APIs.
- **Multiple destinations:** CSV files and SQLite databases.
- **Configurable pipelines:** Choose the extractor, source, schema, loader, and destination in a JSON configuration file.
- **Schema-driven transformations:** Select source fields, convert data types, apply numeric limits, and configure supported cleaning operations.
- **Nested field extraction:** Read values from nested JSON objects using dot notation, such as `address.city`.
- **Data preservation:** Invalid conversions and missing fields are represented as `None` rather than causing the entire record to be discarded.
- **Optional deduplication:** Remove duplicate transformed records through pipeline configuration.
- **Validation:** Validate pipeline configuration and schema definitions before processing.
- **Logging:** Report pipeline progress and execution errors.
- **Automated tests:** Use `pytest` to test transformation behavior.

## 🧱 Architecture

The framework separates the ETL process into three stages:

```text
    Source
      │
      ▼
┌───────────┐
│  Extract  │  CSV / JSON / API
└─────┬─────┘
      ▼
┌───────────┐
│ Transform │  Schema-driven conversions and validation
└─────┬─────┘
      ▼
┌───────────┐
│   Load    │  CSV / SQLite
└─────┬─────┘
      ▼
 Destination
```

### Extract

Extractor implementations retrieve records from supported sources:

| Extractor | Description |
|---|---|
| `csv` | Reads records from a CSV file using its header row. |
| `json` | Reads data from a local JSON file. |
| `api` | Sends an HTTP GET request to a URL and parses the JSON response. |

The API extractor uses a request timeout and raises an error for unsuccessful HTTP responses.

### Transform

The `Transformer` uses a JSON schema to determine which fields to produce and how to process their values.

Supported schema options include:

| Option | Purpose |
|---|---|
| `type` | Target data type. |
| `source` | Source field name; supports nested paths such as `address.city`. |
| `min` | Minimum accepted value for numeric fields. |
| `max` | Maximum accepted value for numeric fields. |
| `clean` | Enables a configured cleaning transformation. |
| `transform` | Selects a supported cleaning operation when `clean` is `true`. |
| `contains` | Keeps a string value only when it contains the specified substring. |

Supported cleaning operations currently include `clean_name` and `clean_phone`.

Supported conversion types include `int`, `float`, `str`, `string`, `bool`, `boolean`, `list`, `dict`, and `tuple`.

If a field is missing or a conversion fails, the transformed field is set to `None`. Numeric values outside configured `min` or `max` limits are also set to `None`.

**Record preservation:** invalid field values do not, by themselves, cause a record to be discarded. However, duplicate records may be removed depending on the deduplication setting.

### Load

| Loader | Description |
|---|---|
| `csv` | Writes the transformed records to `data_transformed.csv` in the configured destination directory. |
| `sqlite` | Creates the configured table if it does not exist and inserts records into `data_transformed.db` in the destination directory. |

The SQLite loader derives column types from the schema. Python `None` values are stored as SQL `NULL`.

## 🗂️ Project Structure

```text
ETL-framework/
├── config/
│   ├── csv_to_csv.json
│   ├── sqlite.json
│   └── ...
├── data/
│   └── ...
├── schemas/
│   └── ...
├── src/
│   ├── config/
│   │   ├── config_validator.py
│   │   ├── load_json.py
│   │   └── schema_validator.py
│   ├── extractors/
│   ├── factories/
│   ├── loaders/
│   ├── transform/
│   └── pipeline.py
├── tests/
│   └── test_transformer.py
├── utils/
│   └── logger.py
├── main.py
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later.
- `pip`.

### 1. Clone the repository

```bash
git clone https://github.com/mxavier-dev/ETL-framework.git
cd ETL-framework
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🛠️ Configuration

The pipeline is configured through JSON files. A pipeline configuration selects the extractor, source, schema, loader, and destination. The schema defines the output fields and their transformation rules.

### Example `config/pipeline.json`

This example reads a JSON file, transforms its records using `schemas/user.json`, and writes the output to a CSV file in the `data/` directory.

```json
{
  "extractor": "json",
  "source": "data/users.json",
  "schema": "user",
  "loader": "csv",
  "destination": "data/",
  "remove_duplicates": false
}
```

Configuration fields:

| Field | Description |
|---|---|
| `extractor` | Extractor identifier: `csv`, `json`, or `api`. |
| `source` | File path or API URL, depending on the extractor. |
| `schema` | Schema filename without the `.json` extension, stored in `schemas/`. |
| `loader` | Loader identifier: `csv` or `sqlite`. |
| `destination` | Destination directory. |
| `remove_duplicates` | Optional boolean. Set to `true` to remove duplicate transformed records or `false` to preserve them. |
| `table` | Required when `loader` is `sqlite`; specifies the destination table name. |

If `remove_duplicates` is omitted, the current implementation removes duplicate transformed records. Set it explicitly to `false` if duplicates must be preserved.

For SQLite, use a configuration such as:

```json
{
  "extractor": "csv",
  "source": "data/users.csv",
  "schema": "user",
  "loader": "sqlite",
  "destination": "data/",
  "table": "users",
  "remove_duplicates": false
}
```

This creates or uses `data/data_transformed.db` and inserts records into the `users` table.

### Example `schemas/user.json`

Suppose the input records contain `id`, `name`, `age`, and a nested `address.city` field.

```json
{
  "id": {
    "type": "int",
    "source": "id"
  },
  "name": {
    "type": "str",
    "source": "name",
    "clean": true,
    "transform": "clean_name"
  },
  "age": {
    "type": "int",
    "source": "age",
    "min": 0,
    "max": 120
  },
  "city": {
    "type": "str",
    "source": "address.city"
  }
}
```

In this schema:

- `id` is converted to an integer.
- `name` is processed by the `clean_name` transformation.
- `age` must be an integer between `0` and `120`; values outside that range become `None`.
- `city` is extracted from the nested `address.city` field.
- Missing fields and failed conversions become `None`.

The `source` option is optional when the input field has the same name as the output field.

> **Note:** The cleaning functions currently remove selected characters; they are simple cleaning examples, not comprehensive data-quality or phone-number validation rules.

## ▶️ Running the Pipeline

The current `main.py` runs `config/csv_to_csv.json`:

```bash
python main.py
```

To run a different configuration, change the configuration path passed to `Pipeline` in `main.py`. For example:

```python
Pipeline("config/sqlite.json").run()
```

Ensure that the referenced configuration file, schema, and source data exist before running the pipeline.

## 🧪 Running Tests

Run the automated test suite from the repository root:

```bash
pytest
```

The current tests cover data-type conversions, invalid values, schema-driven output structure, numeric limits, nested field extraction, data preservation, and duplicate removal.

## 🔭 Roadmap

Potential areas for further development:

- Expand unit and integration test coverage.
- Improve error handling and configuration diagnostics.
- Add more extractors and loaders.
- Improve logging and execution reporting.
- Expand data-cleaning and validation capabilities.
- Document additional end-to-end pipeline examples.
- 
## 📫 Contact

Developed by **Matheus de Freitas Xavier** • [Linkedin Profile](https://www.linkedin.com/in/matheus-xavier-a14b0732a)

## 📄 License

No license has been defined for this project yet.
