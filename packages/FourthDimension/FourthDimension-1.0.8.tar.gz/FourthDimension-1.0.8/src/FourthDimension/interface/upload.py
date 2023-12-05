#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
import logging
import time

from FourthDimension.es.es_client import ElasticsearchClient
from FourthDimension.faiss_process.faiss_storage import embeddings_storage

es_client = ElasticsearchClient()


def upload_entrance(all_documents):
    """
    存储入口
    :param all_documents_list: 段落
    :return:
    """
    print('解析完成，文档上传中...')
    all_documents = es_upload(all_documents)
    if len(all_documents) > 200:
        print('您上传的文档内容较多，请耐心等待...')
    # insert_file_name = faiss_upload(all_documents)
    # print('已存储文档：{}'.format(insert_file_name))
    print('---------------------------------')


def es_upload(all_documents):
    """
    es上传
    :param all_documents: 段落
    :return:
    """
    all_documents = es_client.insert_data(all_documents)
    return all_documents


def faiss_upload(contexts):
    """
    es上传
    :param contexts: 段落
    :return:
    """
    insert_file_name = embeddings_storage(contexts)
    return insert_file_name


def upload_test(contexts_path):
    pass
