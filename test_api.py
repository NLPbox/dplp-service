#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <nlpbox.programming@arne.cl>

import pexpect
import pytest
import requests
import sh

INPUT_TEXT = "Although they didn't like it, they accepted the offer."
EXPECTED_OUTPUT = """0\t1\tAlthough\talthough\tIN\tmark\t3\tO\t (ROOT (SBAR (IN Although)\t1\n0\t2\tthey\tthey\tPRP\tnsubj\t3\tO\t (S (NP (PRP they))\t1\n0\t3\tdidn't\tdidn't\tVBP\troot\t0\tO\t (VP (VBP didn't)\t1\n0\t4\tlike\tlike\tIN\tcase\t5\tO\t (PP (IN like)\t1\n0\t5\tit,\tit,\tNN\tnmod\t3\tO\t (NP (NP (NN it,))\t1\n0\t6\tthey\tthey\tPRP\tnsubj\t7\tO\t (SBAR (S (NP (PRP they))\t2\n0\t7\taccepted\taccept\tVBD\tacl:relcl\t5\tO\t (VP (VBD accepted)\t2\n0\t8\tthe\tthe\tDT\tdet\t9\tO\t (NP (DT the)\t2\n0\t9\toffer.\toffer.\tNN\tdobj\t7\tO\t (NN offer.)))))))))))\t2\n\nParentedTree('NS-elaboration', [ParentedTree('EDU', ['1']), ParentedTree('EDU', ['2'])])"""


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
        files={'input': INPUT_TEXT})
    assert res.content.decode('utf-8') == EXPECTED_OUTPUT

