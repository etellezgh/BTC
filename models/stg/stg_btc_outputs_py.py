from snowflake.snowpark.functions import col, flatten, parse_json


def model(dbt, session):

    dbt.config(materialized="table")

    df = dbt.ref("stg_btc")

    df_with_json = df.with_column("OUTPUTS_JSON", parse_json(col("OUTPUTS")))

    df_exploded = df_with_json.join_table_function(flatten(col("OUTPUTS_JSON")))

    output_columns = [c for c in df.columns]

    df_final = df_exploded.select(
        *[col(c) for c in output_columns],
        col("VALUE")["address"].cast("string").alias("ADDRESS"),
        col("VALUE")["value"].cast("float").alias("VALUE")
    ).filter(col("ADDRESS").is_not_null())

    return df_final


