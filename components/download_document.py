def download_document(
    s3_service_name      : str,
    s3_endpoint_url      : str,
    s3_access_key_id     : str,
    s3_secret_access_key : str,
    s3_region            : str,
    s3_bucket            : str,
    s3_filename          : str,
    pvc_directory        : str
):
    """
    Downloads the document from the s3 bucket.

    Parameters:
        - s3_service_name      (str) : The name of the s3 service. It should be 's3'.
        - s3_endpoint_url      (str) : The url of the s3 endpoint.
        - s3_access_key_id     (str) : The access key id for authentication.
        - s3_secret_access_key (str) : The secret access key for authentication.
        - s3_region            (str) : The region where the s3 bucket is located.
        - s3_bucket            (str) : The s3 bucket where the document will be downloaded.
        - s3_filename          (str) : The s3 pdf filename that will be downloaded.
        - pvc_directory        (str) : The PVC directory where the file will be saved.
    """

    import boto3
    import os

    pvc_directory = os.path.join(pvc_directory, os.path.dirname(s3_filename))
    pvc_filename  = os.path.join(pvc_directory, os.path.basename(s3_filename))

    os.makedirs(pvc_directory, exist_ok = True)

    s3_client = boto3.client(
        service_name          = s3_service_name,
        endpoint_url          = s3_endpoint_url,
        aws_access_key_id     = s3_access_key_id,
        aws_secret_access_key = s3_secret_access_key,
        region_name           = s3_region
    )

    s3_client.download_file(s3_bucket, s3_filename, pvc_filename)


if __name__ == '__main__':
    """
    Elyra Pipelines
    """

    import os

    download_document(
        s3_service_name      = os.getenv('s3_service_name'),
        s3_endpoint_url      = os.getenv('s3_endpoint_url'),
        s3_access_key_id     = os.getenv('s3_access_key_id'),
        s3_secret_access_key = os.getenv('s3_secret_access_key'),
        s3_region            = os.getenv('s3_region'),
        s3_bucket            = os.getenv('s3_bucket'),
        s3_filename          = os.getenv('s3_filename'),
        pvc_directory        = os.getenv('pvc_directory')
    )
