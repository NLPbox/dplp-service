#!/usr/bin/env python3
import os
import sys

import hug
import sh

PARSER_PATH = '/opt/DPLP'
PARSER_EXECUTABLE = 'dplp.sh'
INPUT_FILEPATH = '/tmp/input.txt'

# files that DPLP will produce
OUTPUT_FILEPATH = '/opt/DPLP/complete_output.txt'
OUTPUT_PARSETREE_FILEPATH = '/tmp/input.txt.parsetree'
OUTPUT_MERGE_FILEPATH = '/tmp/input.txt.merge'

# the converter will use DPLP's output to produce this .rs3 file
CONVERTER_PATH = '/opt/DPLP'
CONVERTER_EXECUTABLE = 'dplp2rs3.sh'
OUTPUT_RS3_FILEPATH = '/tmp/input.txt.rs3'


@hug.response_middleware()
def process_data(request, response, resource):
    """This is a middleware function that gets called for every request a hug API processes.
    It will allow Javascript clients on other hosts / ports to access the API (CORS request).
    """
    response.set_header('Access-Control-Allow-Origin', '*')


@hug.post('/parse', output=hug.output_format.file)
def call_parser(body, output_format: hug.types.text):
    parser = sh.Command(os.path.join(PARSER_PATH, PARSER_EXECUTABLE))

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)
        
        parser_stdout = parser(input_file.name, _cwd=PARSER_PATH)

        if body['output_format'] == b'rs3':
            # ~ import pudb; pudb.set_trace()
            dplp2rs3 = sh.Command(os.path.join(CONVERTER_PATH, CONVERTER_EXECUTABLE))
            dplp2rs3(OUTPUT_PARSETREE_FILEPATH, OUTPUT_MERGE_FILEPATH, _cwd=PARSER_PATH)
            return OUTPUT_RS3_FILEPATH
    
        else: # always fall back to the 'original' output format of the parser
            return OUTPUT_FILEPATH

    else:
        return {'body': body}
