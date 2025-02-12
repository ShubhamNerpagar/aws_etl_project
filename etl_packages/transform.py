from pyspark.sql.functions import col, regexp_extract, when, lit
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from my_etl_package.extract import extract_from_s3

def transform_data(bucket_name, metadata_path, glueContext):
    """Transform data: Apply schema validation, regex rules, and partitioning."""
    
    spark = glueContext.spark_session
    metadata = load_metadata(metadata_path)["tables"]["sample_table"]

    all_data = extract_from_s3(bucket_name, metadata_path)

    schema = StructType([
        StructField(field, IntegerType() if dtype == "integer" else StringType(), True)
        for field, dtype in metadata["schema"].items()
    ])

    df = spark.createDataFrame(all_data, schema)

    for pattern, columns in metadata["ge_validations"]["expect_column_values_to_match_regex"].items():
        for column in columns:
            df = df.withColumn(
                column,
                when(regexp_extract(col(column), pattern, 0) != "", col(column)).otherwise(None)
            )

    # Add partition key (_export_date) dynamically
    df = df.withColumn("_export_date", lit("2024-02-12"))

    return df
