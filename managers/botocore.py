"""
    This adds support for Amazon S3.

    User group -
        A group where we can add multiple users, with same permission properties.

        services -> security & identity -> IAM
        user group -> create group with (AWS S3 full access)
        user -> create and download assess keys

    Local setup -

"""
import os

import time
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from flask import jsonify
from constants import Constants


def get_credentials():
    try:
        # Create a session and retrieve credentials
        session = boto3.Session(region_name=Constants.region, profile_name='default')
        credentials = session.get_credentials()

        # Extract and return credentials information
        response = {
            "AccessKeyId": credentials.access_key,
            "SecretAccessKey": credentials.secret_key
        }

        return jsonify(response), 200
    except Exception as e:
        error_response = {"error": str(e)}
        return jsonify(error_response), 500


# printing all buckets
def get_bucket_list(console_print: bool):
    # console_print is an argument to print the buckets
    # in standard console.

    try:
        client = boto3.client('s3')
        buckets_list = client.list_buckets()['Buckets']

        # print buckets in console.
        if console_print:
            for bucket in buckets_list:
                print(bucket)

        return buckets_list, None

    except BotoCoreError as e:
        return None, str(e)


def upload_to_buckets():

    # instance of client
    client = boto3.client('s3')

    # set variables
    bucket = Constants.bucket_name
    file = Constants.file

    curr_path = os.getcwd()
    file_path = os.path.join(curr_path, 'uploads', file)

    # Measure the start time
    start_time = time.time()

    # upload to s3
    client.upload_file(file_path, bucket, file) # file -> name of doc after upload

    # Calculate the time taken
    end_time = time.time()
    time_taken = end_time - start_time
    average_speed = os.path.getsize(file_path)/time_taken

    return {
        "path": file_path,
        "status": "success",
        "time_taken": time_taken,
        "average_speed": average_speed
    }


def create_bucket(new_bucket_name: str):
    try:
        client = boto3.client('s3')
        client.create_bucket(
            Bucket=new_bucket_name,
            CreateBucketConfiguration={'LocationConstraint': Constants.region}
        )
        return True, None
    except ClientError as e:
        error_message = str(e)
        if 'BucketAlreadyOwnedByYou' in error_message:
            return False, "Bucket with the same name already exists and is owned by you."
        else:
            return False, "An error occurred while creating the bucket." + str(e)


# creating an object (simply folder) in S3
def create_folders(target_bucket: str, folder_structure):
    try:
        # this function should be able to make multiple objects (folder).
        client = boto3.client('s3')

        # core logic
        for folder in folder_structure:
            client.put_object(Bucket=target_bucket, Key=folder)
        return {
            "status": 200,
            "created_folders": folder_structure
        }
    except ClientError as e:
        error_message = str(e)
        return False, error_message


def download_file():
    # instance of client
    client = boto3.client('s3')

    # set variables
    bucket = Constants.bucket_name
    file = Constants.file

    curr_path = os.getcwd()
    file_path = os.path.join(curr_path, 'downloads', file)

    # Measure the start time
    start_time = time.time()

    # object method to download file
    client.download_file(
        Bucket=bucket,
        Key=file,
        Filename=file_path
    )
    # Calculate the time taken
    end_time = time.time()
    time_taken = end_time - start_time
    average_speed = os.path.getsize(file_path)/time_taken

    # list the content of Downloaded dir
    downloads_dir = os.path.join(curr_path, 'downloads')
    downloads_files = []
    for root, dirs, files in os.walk(downloads_dir):
        for filename in files:
            print(filename)
            downloads_files.append(filename)
    return {
        "filename": downloads_files,
        "status": "success",
        "time_taken": time_taken,
        "average_speed": average_speed
    }


def delete_file():
    # instance of client
    client = boto3.client('s3')

    # set variables
    bucket = Constants.bucket_name
    file = Constants.file

    curr_path = os.getcwd()
    file_path = os.path.join(curr_path, 'downloads', file)

    client.delete_object(
        Bucket=bucket,
        Key=file_path
    )


def delete_bucket():
    # instance of client
    client = boto3.client('s3')

    # set variables
    bucket = Constants.bucket_name
    file = Constants.file

    curr_path = os.getcwd()
    file_path = os.path.join(curr_path, 'downloads', file)

    client.delete_object(
        Bucket=bucket
    )
    return {
        "status": "success"
    }
