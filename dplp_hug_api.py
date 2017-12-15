#!/usr/bin/env python3
import os
import sys

import hug
import sh

PARSER_PATH = '/opt/DPLP'
PARSER_EXECUTABLE = 'dplp.sh'
INPUT_FILEPATH = '/tmp/input.txt'
OUTPUT_FILEPATH = '/opt/DPLP/complete_output.txt'


@hug.post('/parse', output=hug.output_format.file)
def call_parser(body, output_format: hug.types.text):
    parser = sh.Command(os.path.join(PARSER_PATH, PARSER_EXECUTABLE))

#    import pdb; pdb.set_trace()

    if 'input' in body:
        input_file_content = body['input']
        with open(INPUT_FILEPATH, 'wb') as input_file:
            input_file.write(input_file_content)
        
        parser_stdout = parser(input_file.name, _cwd=PARSER_PATH)
        #parser_stdout = sh.bash("-x", os.path.join(PARSER_PATH, PARSER_EXECUTABLE), input_file.name, _cwd=PARSER_PATH) 
        return OUTPUT_FILEPATH
    
    else:
        return {'body': body}
