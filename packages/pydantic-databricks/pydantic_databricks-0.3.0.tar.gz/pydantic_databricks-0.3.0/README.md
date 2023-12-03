# Pydantic Databricks

## Overview

This library leverages Pydantic to simplify the generation of Databricks SQL queries for managing tables.
It provides a convenient way to define table schemas using Pydantic models and generates corresponding SQL statements.

## Installation

```bash
pip install pydantic-databricks
```

## Usage

### 1. Basic Example Table Creation

```python
from pydantic_databricks import DatabricksModel
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

class Schema(DatabricksModel):
    _table_name = "test"
    _schema_name = "test_schema"
    
    col1: str
    col2: int
    col3: float
    
spark.sql(Schema.create_table())
```
Generated SQL:
```sql
CREATE TABLE test_schema.test (col1 STRING NOT NULL, col2 BIGINT NOT NULL, col3 DOUBLE NOT NULL) USING DELTA; 
```

### 2. Setting Grants

```python
from pydantic_databricks import DatabricksModel, Grant, GrantAction
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

class Schema(DatabricksModel):
    _table_name = "test"
    _schema_name = "default"
    _grants = {Grant(action=GrantAction.MODIFY, principal="user1"),
               Grant(action=GrantAction.SELECT, principal="user2"), }

    col1: str

for grant in Schema.grant_statements():
    spark.sql(grant)
```
   
    

## Currently Supported Options

- `_catalog_name`: The catalog name for the table. Default is `None`. If `None` then a two part namespace is used.
- `_schema_name`: The schema name for the table (required).
- `_table_name`: The name of the table (required).
- `_grants`: A set of Grant objects. Default is `None`.
- `_location_prefix`: The location prefix for external tables. Default is `None`. If set, then the table is created as an external table. The prefix will be appended with the full table name.
- `_table_properties`: A dictionary of table properties.
- `_table_create_mode`: The mode for table creation. Default is `CreateMode.CREATE`.
- `_table_data_source`: The data source for the table. Default is `DataSource.DELTA`.
- `_partition_columns`: A list of partition columns for the table. Default is `None`.
- `_options`: A dictionary of additional options for table creation. Default is `None`.
- `_comment`: A comment for the table. Default is `None`.

## Coming soon 
- Support for table and column constraints

## Contributing

We welcome contributions to pydantic-databricks! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a branch for your feature or bug fix.
3. Make your changes.
4. Test your changes thoroughly.
5. Submit a pull request.


## License

* pydantic-databricks is licensed under the MIT License. See [LICENSE](LICENSE) for more information
