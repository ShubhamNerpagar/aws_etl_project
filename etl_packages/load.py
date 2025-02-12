from awsglue.dynamicframe import DynamicFrame

def load_to_glue(df, database_name, table_name, s3_output_path, glueContext):
    """Load transformed data into AWS Glue Table with partitioning."""
    
    dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

    glueContext.write_dynamic_frame.from_options(
        frame=dynamic_frame,
        connection_type="s3",
        connection_options={"path": s3_output_path, "partitionKeys": ["_export_date"]},
        format="parquet"
    )
