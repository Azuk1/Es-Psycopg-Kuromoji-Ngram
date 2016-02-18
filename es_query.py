#!/usr/bin/env python
# coding: utf-8
# by default we connect to localhost:9200
from __future__ import unicode_literals
from future_builtins import *
from datetime import datetime
from elasticsearch import Elasticsearch
# from elasticsearch_dsl import analyzer, tokenizer

es = Elasticsearch()

es.indices.refresh(index="wantedly-demo")

# 質問読み込み
print "質問："
input_q = raw_input().decode("utf-8")
# input_q = "Java エンジニアウォンテッド！"

results = es.indices.analyze(text=input_q)

for result in results['tokens']:
    print result['token']

    res = es.search(index="wantedly-demo", doc_type="project", body={"query": {"simple_query_string": {"fields":["_all"],"query":"%s"%result["token"]}}})

    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(id)s: %(title)s" % hit["_source"])

#会社情報検索
# res = es.search(index="wantedly-demo", doc_type="company", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(id)s %(name)s: %(location)s" % hit["_source"])

