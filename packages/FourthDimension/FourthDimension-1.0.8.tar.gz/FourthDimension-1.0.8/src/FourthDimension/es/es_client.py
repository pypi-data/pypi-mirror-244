#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
import json
import os

from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm

from FourthDimension.config.config import config_setting
from FourthDimension.rerank.rerank import (
    question_analysis,
    getDetailResult
)

"""
文件说明：
"""
# Elasticsearch连接信息
host = config_setting['elasticsearch_setting']['host']
port = config_setting['elasticsearch_setting']['port']
username = config_setting['elasticsearch_setting']['username']
password = config_setting['elasticsearch_setting']['password']
index_name = config_setting['elasticsearch_setting']['index_name']
analyzer = config_setting['elasticsearch_setting']['analyzer']
top_k = config_setting['recall_config']['top_k']


class DocQAAnswerEntity:
    def init(self, content, question, fuzz_score, words_ratio, para_num, context_type, para_context, file_name):
        self.content = content
        self.question = question
        self.fuzz_score = fuzz_score
        self.words_ratio = words_ratio
        self.context_type = context_type
        self.para_num = para_num
        self.para_context = para_context
        self.file_name = file_name


class ElasticsearchClient:
    def __init__(self, host=host, port=port, username=username, password=password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = Elasticsearch(
            [self.host],
            http_auth=(self.username, self.password),
            port=self.port,
            use_ssl=False,
            verify_certs=False,
            timeout=30,
            max_retries=3,
            retry_on_timeout=True
        )

    def create_index(self):
        index_exists = self.client.indices.exists(index=index_name)
        if index_exists:
            # print(f"索引 '{index_name}' 已存在")
            pass
        else:
            # 创建索引
            settings = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "index.lifecycle.name": "default_index",
                    "index.lifecycle.rollover_alias": "index"
                },
                "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "text_id": {
                            "type": "keyword"
                        },
                        "file_name": {
                            "type": "keyword"
                        },
                        "type": {
                            "type": "keyword"
                        },
                        "text": {
                            "type": "text",
                            "analyzer": analyzer,
                            "search_analyzer": analyzer
                        },
                        "para_num": {
                            "type": "long"
                        },
                    }
                }
            }
            self.client.indices.create(index=index_name, ignore=400, body=settings)
            if self.client.indices.exists(index=index_name):
                print(f"索引 '{index_name}' 创建成功")
            else:
                print(f"索引 '{index_name}' 创建失败，请检查es设置")

    def insert_data(self, all_documents):
        """
        插入文档
        context_type：数据类型（chunk分块、para自然段）
        """
        self.create_index()
        file_names = self.search_filename()
        actions = []

        for d in tqdm(all_documents):
            metadata = d.metadata
            filename = metadata['source']
            para_num = metadata['para_num']
            context_type = metadata['type']
            if filename not in file_names:
                context = d.page_content
                action = {
                    '_index': index_name,
                    '_type': '_doc',
                    '_source': {
                        'text_id': '',
                        'file_name': filename,
                        'type': context_type,
                        'text': context,
                        'para_num': para_num
                    }
                }
                actions.append(action)

        if actions:
            helpers.bulk(self.client, actions)

        return all_documents

    def search_filename(self):
        # 构建查询语句
        query = {
            "size": 10000,  # 每次滚动获取的文档数
            "_source": ["file_name"],
            "query": {
                "match_all": {}
            }
        }

        # 执行查询
        result = self.client.search(index=index_name, body=query, scroll="1s")

        # 从查询结果中提取文件名
        file_names = []
        scroll_id = result["_scroll_id"]
        while True:
            hits = result["hits"]["hits"]
            for hit in hits:
                file_names.append(hit["_source"]["file_name"])

            # 检查是否还有更多结果
            if len(hits) < 10000:
                break

            # 滚动到下一批结果
            result = self.client.scroll(scroll_id=scroll_id, scroll="1s")
            scroll_id = result["_scroll_id"]

        # 去重文件名列表
        result = list(set(file_names))

        return result

    def clean_data(self):
        """
        清除数据
        """
        self.create_index()
        self.client.delete_by_query(index=index_name, body={"query": {"match_all": {}}})

    def es_search_para(self, para_num, file_name):
        try:
            # es查询
            search_results = []
            for num in para_num:
                sourceBuilder = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "term": {
                                        "file_name": file_name
                                    }
                                },
                                {
                                    "term": {
                                        "type": "para"
                                    }
                                },
                                {
                                    "term": {
                                        "para_num": num
                                    }
                                }
                            ]
                        }
                    },
                    "size": 1
                }
                response = self.client.search(index=index_name, body=sourceBuilder)
                hits = response["hits"]["hits"]
                context = hits[0]['_source']['text']
                search_results.append(context)
            return search_results
        except Exception as e:
            print(e)

    def es_search(self, question):
        self.create_index()
        question_anal = question_analysis(question)
        searchHits = []
        try:
            # es查询
            sourceBuilder = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "match": {
                                                "text": {
                                                    "query": question,
                                                    "boost": 1,
                                                    "analyzer": analyzer
                                                }
                                            }
                                        },
                                        {
                                            "match": {
                                                "text": {
                                                    "query": question_anal,
                                                    "boost": 3,
                                                    "analyzer": analyzer
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "term": {
                                    "type": "chunk"
                                }
                            }
                        ],
                        "filter": [
                            {
                                "term": {
                                    "type": "chunk"
                                }
                            }
                        ]
                    }
                },
                "size": top_k
            }
            response = self.client.search(index=index_name, body=sourceBuilder)
            hits = response["hits"]["hits"]
            searchHits = hits
        except Exception as e:
            print(e)

        esResponses = []

        # 获取es查询命中结果
        for hit in searchHits:
            esResponse = DocQAAnswerEntity()
            hitString = hit["_source"]
            content = hitString['text']
            para_num = hitString['para_num']
            context_type = hitString['type']
            file_name = hitString['file_name']
            esResponse.question = question
            esResponse.content = content
            esResponse.para_num = para_num
            esResponse.context_type = context_type
            esResponse.file_name = file_name
            esResponses.append(esResponse)
        sorted_es_response = getDetailResult(esResponses, question, question_anal)
        top_k_documents = []
        for i, d in enumerate(sorted_es_response):
            para_num = d.para_num
            file_name = d.file_name
            para_contexts = self.es_search_para(para_num, file_name)
            d.para_context = para_contexts
            top_k_documents.append(d)
        return top_k_documents
        # top_k_content = []
        # for i, d in enumerate(sorted_es_response):
        #     top_k_content.append(d.content)
        # return top_k_content
