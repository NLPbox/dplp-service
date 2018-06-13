# dplp-service

[![Travis Build Status](https://travis-ci.org/NLPbox/dplp-service.svg?branch=master)](https://travis-ci.org/NLPbox/dplp-service)
[![Docker Build Status](https://img.shields.io/docker/build/nlpbox/dplp-service.svg)](https://hub.docker.com/r/nlpbox/dplp-service/)

This docker container allows you to build, install and run the
[DPLP RST discourse parser](https://github.com/jiyfeng/DPLP)
(Ji and Eisenstein 2014) as a REST API in a docker container.


## build

docker build -t dplp-service .

## run

docker run -p 8000:8000 -ti dplp-service


## Usage Examples

### CURL

```
$ cat test.txt 
Altough they didn't like him, they accepted the offer.

$ curl -X POST -F "input=@test.txt" http://localhost:8000/parse -F output_format=original
0       1       Altough Altough NNP     root    0       O        (ROOT (FRAG (NP (NP (NNP Altough))     1
0       2       they    they    PRP     nsubj   3       O        (SBAR (S (NP (PRP they))       2
0       3       didn't  didn't  VBP     acl:relcl       1       O        (VP (VBP didn't)       2
0       4       like    like    IN      case    5       O        (SBAR (S (PP (IN like) 2
0       5       him,    him,    NN      nmod    7       O        (NP (NN him,)))        2
0       6       they    they    PRP     nsubj   7       O        (NP (PRP they))        3
0       7       accepted        accept  VBD     ccomp   3       O        (VP (VBD accepted)     3
0       8       the     the     DT      det     9       O        (NP (DT the)   3
0       9       offer.  offer.  NN      dobj    7       O        (NN offer.)))))))))))  3

RELATIONS:

((1, 1), 'Satellite', 'attribution')
((2, 2), 'Nucleus', 'span')
((3, 3), 'Satellite', 'elaboration')
((2, 3), 'Nucleus', 'span')


$ curl -X POST -F "input=@test.txt" http://localhost:8000/parse -F output_format=rs3
<?xml version='1.0' encoding='UTF-8'?>
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
```

### Javascript

```
>>> var xhr = new XMLHttpRequest();

>>> xhr.open("POST", "http://localhost:8000/parse")

>>> var data = new FormData();
>>> data.append('input', 'Altough they didn\'t like him, they accepted the offer.');
>>> data.append('output_format', 'original');

>>> xhr.send(data);
>>> console.log(xhr.response);
0	1	Altough	Altough	NNP	root	0	O	 (ROOT (FRAG (NP (NP (NNP Altough))	1
0	2	they	they	PRP	nsubj	3	O	 (SBAR (S (NP (PRP they))	2
0	3	didn't	didn't	VBP	acl:relcl	1	O	 (VP (VBP didn't)	2
0	4	like	like	IN	case	5	O	 (SBAR (S (PP (IN like)	2
0	5	him,	him,	NN	nmod	7	O	 (NP (NN him,)))	2
0	6	they	they	PRP	nsubj	7	O	 (NP (PRP they))	3
0	7	accepted	accept	VBD	ccomp	3	O	 (VP (VBD accepted)	3
0	8	the	the	DT	det	9	O	 (NP (DT the)	3
0	9	offer.	offer.	NN	dobj	7	O	 (NN offer.)))))))))))	3

RELATIONS:

((1, 1), 'Satellite', 'attribution')
((2, 2), 'Nucleus', 'span')
((3, 3), 'Satellite', 'elaboration')
((2, 3), 'Nucleus', 'span')
```
