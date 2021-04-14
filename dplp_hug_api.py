#!/usr/bin/env python3
import os
import sys
import traceback

import falcon
import hug
import sh

PARSER_PATH = '/opt/DPLP'
PARSER_EXECUTABLE = 'dplp.sh'
INPUT_FILEPATH = '/tmp/input.txt'

# files that DPLP will produce
OUTPUT_FILEPATH = '/opt/DPLP/complete_output.txt'
OUTPUT_PARSETREE_FILEPATH = '/tmp/input.txt.parsetree'
OUTPUT_MERGE_FILEPATH = '/tmp/input.txt.merge'


@hug.response_middleware()
def process_data(request, response, resource):
    """This is a middleware function that gets called for every request a hug API processes.
    It will allow Javascript clients on other hosts / ports to access the API (CORS request).
    """
    response.set_header('Access-Control-Allow-Origin', '*')


@hug.post('/parse', output=hug.output_format.file)
def call_parser(body):
    parser = sh.Command(os.path.join(PARSER_PATH, PARSER_EXECUTABLE))

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)
        
        try:
            parser_stdout = parser(input_file.name, _cwd=PARSER_PATH)
            return OUTPUT_FILEPATH
        except Exception:
            ex_str = traceback.format_exc()
            raise falcon.HTTPInternalServerError("Can't get result from CoreNLP", ex_str)

    else:
        return {'body': body}
