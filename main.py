from my_etl_package.transform import transform_data
from my_etl_package.load import load_to_glue
from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glueContext = GlueContext(sc)

BUCKET_NAME = "my-etl-bucket"
DATABASE_NAME = "my_etl_db"
TABLE_NAME = "sample_table"
S3_OUTPUT_PATH = f"s3://{BUCKET_NAME}/output/"
METADATA_PATH = f"s3://{BUCKET_NAME}/my_etl_package/metadata.json"

def main():
    df_transformed = transform_data(BUCKET_NAME, METADATA_PATH, glueContext)
    load_to_glue(df_transformed, DATABASE_NAME, TABLE_NAME, S3_OUTPUT_PATH, glueContext)

if __name__ == "__main__":
    main()
