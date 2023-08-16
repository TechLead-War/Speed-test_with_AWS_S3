"""
    This is a speed test app, where you can test
    internet speed.

    Technical:
        The program uploads a file to AWS S3,
        amd then download file from S3, then
        calculates the time required for
        upload / download. Then file in S3
        is deleted.

    Size of download/upload:
        5MB each.

"""

import os
from flask import Flask, jsonify, request
import boto3
import time

from constants import HTML, Constants
from managers.botocore import get_credentials, upload_to_buckets, create_bucket, get_bucket_list, create_folders

app = Flask(__name__)
app.debug = True


def calculate_speed(file_size, elapsed_time):
    speed_mbps = (file_size / 1024 / 1024) / elapsed_time
    return speed_mbps


@app.route('/')
def index():
    return HTML.render_template


@app.route('/check_credentials')
def check_credentials():
    return get_credentials()


@app.route('/get_buckets', methods=['GET'])
def get_buckets():
    buckets_list, error_message = get_bucket_list(console_print=True)

    if error_message:
        return jsonify({"error": error_message}), 500
    else:
        return jsonify({"buckets": buckets_list}), 200


@app.route('/upload_file', methods=["POST"])
def upload_to_bucket():
    return upload_to_buckets()


@app.route('/create_bucket', methods=['POST'])
def create_bucket_route():
    try:
        request_data = request.json
        new_bucket_name = request_data.get('bucket_name')

        if not new_bucket_name:
            return jsonify({"error": "Bucket name is missing from the request body"}), 400

        success, message = create_bucket(new_bucket_name)

        if success:
            return jsonify({"message": "Bucket created successfully"}), 201
        else:
            return jsonify({"error": message}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/create_folder", methods=["POST"])
def create_folder():
    request_data = request.json
    folders = request_data.get('folder_structure')
    return create_folders(Constants.bucket_name, folders)


if __name__ == '__main__':
    app.run(debug=True)
# document this code very well for future use
# pre-assigned url as well
