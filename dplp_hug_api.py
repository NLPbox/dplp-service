#!/usr/bin/env python3
import os
import sys

import hug
import sh

PARSER_PATH = '/opt/DPLP'
PARSER_EXECUTABLE = 'dplp.sh'
INPUT_FILEPATH = os.path.join(PARSER_PATH, 'input.txt')
OUTPUT_FILEPATH = os.path.join(PARSER_PATH, 'complete_output.txt')


@hug.post('/parse', output=hug.output_format.file)
def call_parser(body, output_format: hug.types.text):
    parser = sh.Command(os.path.join(PARSER_PATH, PARSER_EXECUTABLE))

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)
        
        parser_stdout = parser(input_file.name, _cwd=PARSER_PATH)
        return OUTPUT_FILEPATH
    
    else:
        return {'body': body}
