/*
  MIT No Attribution
  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
import json
import sys
import boto3
import base64
import os
import io
import contextlib
import logging
from io import StringIO
import sys


def lambda_handler(event, context):

    #command to execute with ParallelCluster
    command = event["queryStringParameters"]["command"]
    os.environ['HOME'] = '/tmp'
    module = "awsbatch." + command
    __import__(module)
    cli = sys.modules[module]
    sys.argv = [command]
    try:
      cluster = event["queryStringParameters"]["cluster"]
      sys.argv.append('--cluster')
      sys.argv.append(cluster)
    except:
      return {
               'statusCode': 200,
               'body': 'Please specify the cluster\n'
            }
    try:
      additional_parameters = event["headers"]["additional_parameters"]
      add_params = additional_parameters.split()
      sys.argv = sys.argv + add_params
    except:
      print("no_param")
    if command in ['awsbsub']:      
        #Retrieve submission script
        try:
            file_content = base64.b64decode(event['body'])
            path_config = '/tmp/script'
            config_file = open(path_config,'w')
            config_file.write(file_content.decode('utf-8'))
            config_file.close()
            sys.argv.append('-cf')
            sys.argv.append('/tmp/script')
        except:
            return {
               'statusCode': 200,
               'body': 'Please specify the submission script\n'
            }
    elif command in ['awsbstat', 'awsbout']:
      try:
        jobid = event["queryStringParameters"]["jobid"]
        try:
          compute_node = event["queryStringParameters"]["compute_node"]
          jobid = jobid + '#' + compute_node
        except:
          print("no compute_node")
        sys.argv.append(jobid)
      except:
        print("no jobid")
    elif command in ['awsbout', 'awsbkill']:
      try:
        jobid = event["queryStringParameters"]["jobid"]
        sys.argv.append(jobid)
      except:
        return {
               'statusCode': 200,
               'body': 'Please specify the jobid\n'
            }
    #execute the pcluster command
    output = ''
    try:
      pcluster_logger = logging.getLogger("pcluster")
      pcluster_logger.propagate = False
      stdout = io.StringIO()
      stderr = io.StringIO()
      with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        cli.main()
      print("stdout:\n{}".format(stdout.getvalue()))
      print("stderr:\n{}".format(stderr.getvalue()))
      output = stdout.getvalue() + '\n' + stderr.getvalue() + '\n'
    except SystemExit:
      print("stdout:\n{}".format(stdout.getvalue()))
      print("stderr:\n{}".format(stderr.getvalue()))
      print("exception: {}".format(e))
      output = stdout.getvalue() + '\n' + stderr.getvalue() + '\n' + str(e) + '\n'
      
    return {
        'statusCode': 200,
        'body': output
    }
