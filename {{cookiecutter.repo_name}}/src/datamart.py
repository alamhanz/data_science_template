from google.cloud import bigquery
from google.cloud import storage
import pandas as pd
from tensorflow.python.lib.io import file_io


def gcs2local(path_origin, path_dest):
    model_w_load = file_io.FileIO(path_origin, mode="rb")
    temp_model_file = open(path_dest, "wb")
    temp_model_file.write(model_w_load.read())
    temp_model_file.close()
    model_w_load.close()


def set_query_from_file(file_path):
    sql_template_file = open(file_path, "r")
    sql_template = sql_template_file.read()
    sql_template_file.close()
    return sql_template


# def gcs_read_csv(path, prefix_file,bucket_name, usedcols=None,verbose=False):
def gcs_read_csv(config, usedcols=None, verbose=False):
    billing_project = config.get("billing_project", "gods-dev")
    df_raw0 = pd.DataFrame()
    client = storage.Client(project=billing_project)
    bucket_cli = client.get_bucket(config["bucket"])
    for c in bucket_cli.list_blobs(prefix=config["prefix"]):
        if config["table_name"] in c.name:
            file_n = "gs://" + config["bucket"] + "/" + c.name
            if verbose:
                print(file_n)

            if usedcols == None:
                df_temp = pd.read_csv(file_n)
            else:
                df_temp = pd.read_csv(file_n, usecols=usedcols)
            df_raw0 = df_raw0.append(df_temp)
    return df_raw0


def query_to_bq(query_text, config):
    # Construct a BigQuery client object.

    billing_project = config.get("billing_project", "gods-dev")
    project_id = config["project_name"]
    dataset_id = config["dataset_name"]

    client = bigquery.Client(project=billing_project)
    job_config = bigquery.QueryJobConfig(
        dry_run=False,
        use_query_cache=False
        # ,default_dataset ="{}.{}".format(project_id,dataset_id)
    )

    # Start the query, passing in the extra configuration.
    query_job = client.query(
        (query_text),
        job_config=job_config,
    )  # Make an API request.

    # A dry run query completes immediately.
    # print("This query will process {} bytes.".format(query_job.total_bytes_processed))

    query_job.result()  # Waits for the job to complete.
    # destination_table = client.get_table(bq_table_id)  # Make an API request.
    return query_job


def gcs2bq(config, disposition="WRITE_TRUNCATE", file_format=bigquery.SourceFormat.CSV):
    # WRITE_APPEND
    uri = config["uri"]
    project_id = config["project_name"]
    dataset_id = config["dataset_name"]
    table_name = config["table_name"]
    bq_client = config["client"]
    print(uri)

    bq_table_id = "{}.{}.{}".format(project_id, dataset_id, table_name)
    print(bq_table_id)
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        # skip_leading_rows=1,
        source_format=file_format,
        write_disposition=disposition,
        allow_quoted_newlines=True,
    )

    load_job = bq_client.load_table_from_uri(
        uri, bq_table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.
    destination_table = bq_client.get_table(bq_table_id)  # Make an API request.
    print("Table {} uploaded.".format(bq_table_id))


def table2bq(
    df, config, disposition="WRITE_TRUNCATE", file_format=bigquery.SourceFormat.CSV
):
    # WRITE_APPEND
    project_id = config["project_name"]
    dataset_id = config["dataset_name"]
    table_name = config["table_name"]
    bq_client = config["client"]

    bq_table_id = "{}.{}.{}".format(project_id, dataset_id, table_name)
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        # skip_leading_rows=1,
        source_format=file_format,
        write_disposition=disposition,
        allow_quoted_newlines=True,
    )

    load_job = bq_client.load_table_from_dataframe(
        df, bq_table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.
    destination_table = bq_client.get_table(bq_table_id)  # Make an API request.
    print("Table {} uploaded.".format(bq_table_id))


def bq2gcs(config):
    # bucket_name = config['bucket_name']
    # destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv")
    billing_project = config.get("billing_project", "gods-dev")

    destination_uri = config["destination_uri"]
    project = config["project_name"]
    dataset_id = config["dataset_name"]
    table_id = config["table_name"]

    client = bigquery.Client(project=billing_project)

    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_ref = dataset_ref.table(table_id)

    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        #       # Location must match that of the source table.
        #       location="US",
    )  # API request
    extract_job.result()  # Waits for job to complete.

    print(
        "Exported {}:{}.{} to {}".format(project, dataset_id, table_id, destination_uri)
    )
