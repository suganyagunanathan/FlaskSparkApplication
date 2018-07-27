from flask import Flask, jsonify, request
import pyspark
import boto3
import datetime
import json
import sys

# Create a flask application
app = Flask(__name__)


@app.route('/copy_files', methods=["POST","GET"])
def hello_world():
    print("Hello World from Suganyaaaaaaaaaaa")
    try:
        input_data = json.loads(request.data)
        current_dt = datetime.datetime.now()

        source_bucket = input_data['source_bucket']
        destination_bucket = input_data['destination_bucket']
        source_key = input_data['source_key']
        destination_key = input_data['destination_key']

        print("source_bucket ::: " + source_bucket)
        print("destination_bucket ::: " + destination_bucket)
        print("source_key ::: " + source_key)
        print("destination_key ::: " + destination_key)

        print("Task1")
        spark = pyspark.sql.SparkSession.builder.getOrCreate()
        print("***Start creating data frame")
        data_frame = spark.createDataFrame(
            data=[[1, 'A', 'Suganya'], [2, 'B', 'Charvi'], [3, 'C', 'Tao'], [4, 'D', 'Jon']])
        print("DATA FRAME CREATED ::: ")
        print(data_frame)

        print("***Start writing data frame")
        temp_file = "testSchema" + str(current_dt.strftime("%Y_%m_%d_%H_%M_%S")) + ".csv"
        print(temp_file)
        data_frame.coalesce(1).write.csv(temp_file, header=True)

        print("Task2")
        print("***Start reading the file")
        s3 = boto3.resource('s3')
        print("***Start reading from S3")
        fileobj = s3.Object(source_bucket, source_key).get()['Body']
        print("SOURCE LOCATION FILE CONTENTS ::: ")
        print(fileobj.read())
        s3.Bucket(source_bucket).download_file(source_key, '/tmp/file1.csv')

        print("***Start writing tO S3")
        client = boto3.client('s3')
        s3.meta.client.upload_file('/tmp/file1.csv', destination_bucket, destination_key)

        fileobj = s3.Object(destination_bucket, destination_key).get()['Body']
        print("DESTINATION LOCATION FILE CONTENTS ::: ")
        print(fileobj.read())

        message = "File copied successfully"

    except Exception as ex:
        message = str(ex)

    result = {"message": message, "copied_time": str(current_dt.strftime("%Y-%m-%d %H:%M:%S"))}
    print("result ::: " + str(result))

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
