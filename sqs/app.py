def main():

    import boto3
    import kfp
    import os
    import time

    sqs           = boto3.client('sqs')
    sqs_queue_url = os.getenv('sqs_queue_url')

    kubeflow_host = os.getenv('kubeflow_host')

    pipeline_package_path = 'app.yaml'
    pipeline_arguments    = {
        's3_service_name'      : 's3',
        's3_endpoint_url'      : os.getenv('s3_endpoint_url'),
        's3_access_key_id'     : os.getenv('s3_access_key_id'),
        's3_secret_access_key' : os.getenv('s3_secret_access_key'),
        's3_region'            : os.getenv('s3_region'),
        's3_bucket'            : os.getenv('s3_bucket'),
        'milvus_uri'           : os.getenv('milvus_uri'),
        'milvus_username'      : os.getenv('milvus_username'),
        'milvus_password'      : os.getenv('milvus_password'),
        'milvus_collection'    : os.getenv('milvus_collection'),
        'inference_server'     : os.getenv('inference_server'),
        'model_name'           : os.getenv('model_name'),
        'remove_watermark'     : os.getenv('remove_watermark') == 'True',
        'storage_class_name'   : os.getenv('storage_class_name'),
    }

    while True:

        messages = sqs.receive_message(
            QueueUrl              = sqs_queue_url,
            MessageAttrubuteNames = ['All'],
            MaxNumberOfMessages   = 5,
            WaitTimeSeconds       = 0
        )

        for message in messages:

            pipeline_arguments['s3_filename'] = 'pdf/test.pdf'

            kfp.client.Client(host = kubeflow_host).create_run_from_pipeline_package(
                pipeline_file = pipeline_package_path,
                arguments     = pipeline_arguments
            )

        time.sleep(120)


if __name__ == '__main__':

    main()
