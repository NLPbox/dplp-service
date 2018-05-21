#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

import pexpect
import pytest
import requests
import sh

INPUT_TEXT = "Although they didn't like it, they accepted the offer."
EXPECTED_OUTPUT = """0	1	Although	although	IN	mark	3	O	 (ROOT (SBAR (IN Although)	1
0	2	they	they	PRP	nsubj	3	O	 (S (NP (PRP they))	1
0	3	didn't	didn't	VBP	root	0	O	 (VP (VBP didn't)	1
0	4	like	like	IN	case	5	O	 (SBAR (S (PP (IN like)	1
0	5	it,	it,	NN	nmod	7	O	 (NP (NN it,)))	1
0	6	they	they	PRP	nsubj	7	O	 (NP (PRP they))	2
0	7	accepted	accept	VBD	ccomp	3	O	 (VP (VBD accepted)	2
0	8	the	the	DT	det	9	O	 (NP (DT the)	2
0	9	offer.	offer.	NN	dobj	7	O	 (NN offer.)))))))))	2

RELATIONS:

((1, 1), 'Nucleus', 'span')
((2, 2), 'Satellite', 'elaboration')
"""

EXPECTED_RS3 = """<?xml version='1.0' encoding='UTF-8'?>
<rst>
  <header>
    <relations>
      <rel name="elaboration" type="rst"/>
    </relations>
  </header>
  <body>
    <segment id="3" parent="1" relname="span">Although they didn't like it,</segment>
    <segment id="5" parent="3" relname="elaboration">they accepted the offer.</segment>
    <group id="1" type="span"/>
  </body>
</rst>
"""

@pytest.fixture(scope="session", autouse=True)
def start_api():
    print("starting API...")
    child = pexpect.spawn('hug -f dplp_hug_api.py')
    # provide the fixture value (we don't need it, but it marks the
    # point when the 'setup' part of this fixture ends).
    yield child.expect('(?i)Serving on :8000')
    print("stopping API...")
    child.close()


def test_api_plaintext():
    """The dplp-service API produces the expected plaintext parse output."""
    res = requests.post(
        'http://localhost:8000/parse',
        files={'input': INPUT_TEXT},
        data={'output_format': 'original'})
    assert res.content.decode('utf-8') == EXPECTED_OUTPUT


def test_api_rs3():
    """The dplp-service API produces the expected RS3 parse output."""
    res = requests.post(
        'http://localhost:8000/parse',
        files={'input': INPUT_TEXT},
        data={'output_format': 'rs3'})
    assert res.content.decode('utf-8') == EXPECTED_RS3
