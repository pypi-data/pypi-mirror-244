import json
import os
import tempfile
from typing import Any, Optional
from uuid import UUID

from fastapi import UploadFile

from FourthDimension.doc.document import Document
from FourthDimension.doc.spliter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from FourthDimension.utils.file import compute_sha1_from_file
from FourthDimension.config.config import config_setting, encoding

chunk_size = config_setting['para_config']['chunk_size']
# chunk_overlap = config_setting['para_config']['overlap']
chunk_overlap = 20
min_single_para_len = 80
max_para_len = 1000
max_chunk_len = 500


def get_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return num_tokens


class File(BaseModel):
    id: Optional[UUID] = None
    file: Optional[UploadFile]
    file_name: Optional[str] = ""
    file_size: Optional[int] = None
    file_sha1: Optional[str] = ""
    vectors_ids: Optional[list] = []
    file_extension: Optional[str] = ""
    content: Optional[Any] = None
    chunk_size: int = chunk_size
    chunk_overlap: int = chunk_overlap
    origin_documents: Optional[Any] = None
    para_documents: Optional[Any] = None
    chunk_documents: Optional[Any] = None
    chunk_text_splitter: Optional[Any] = None
    para_text_splitter: Optional[Any] = None
    min_single_para_len: int = min_single_para_len
    max_para_len: int = max_para_len

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.file:
            self.para_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=max_para_len, chunk_overlap=chunk_overlap)
            self.chunk_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=max_chunk_len, chunk_overlap=chunk_overlap)
            self.file_name = self.file.filename
            self.file_size = self.file.size  # pyright: ignore reportPrivateUsage=none
            self.file_extension = os.path.splitext(
                self.file.filename  # pyright: ignore reportPrivateUsage=none
            )[-1].lower()

    async def compute_file_sha1(self):
        """
        Compute the sha1 of the file using a temporary file
        """
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            await self.file.seek(0)  # pyright: ignore reportPrivateUsage=none
            self.content = (
                await self.file.read()  # pyright: ignore reportPrivateUsage=none
            )
            tmp_file.write(self.content)
            tmp_file.flush()
            self.file_sha1 = compute_sha1_from_file(tmp_file.name)

        os.remove(tmp_file.name)

    def compute_para(self, documents):
        content = documents[0].page_content
        file_name = documents[0].metadata['source']
        all_para = []
        split_content = content.split('\n')
        current_para = split_content[0]
        for i in range(1, len(split_content)):
            line = split_content[i]
            current_para_len = get_tokens_from_string(current_para)
            line_len = get_tokens_from_string(line)
            # 若单段长度小于总段限长
            if line_len < max_para_len:
                # 若本段加上下一段的长度小于总段限长，则两段拼接
                if current_para_len + line_len < max_para_len:
                    if current_para != "":
                        current_para += '\n' + line
                    else:
                        current_para += line
                    if line_len >= min_single_para_len:
                        all_para.append(current_para)
                        current_para = ""
                else:
                    # 若本段加上下一段的长度大于总段限长，则归类为一个自然段
                    all_para.append(current_para)
                    current_para = line
            else:
                # 切分过长段落
                # if current_para != "" and current_para not in all_para:
                if current_para != "":
                    all_para.append(current_para)
                line_para_documents = [Document(page_content=line, metadata={'source': file_name})]
                line_para_documents = self.para_text_splitter.split_documents(line_para_documents)
                current_para = line_para_documents[0].page_content
                for j in range(1, len(line_para_documents)):
                    # 切分后的段落
                    current_para_len = get_tokens_from_string(current_para)
                    current_line = line_para_documents[j].page_content
                    current_line_len = get_tokens_from_string(current_line)

                    if current_para_len + current_line_len < max_para_len:
                        if current_para != "":
                            # current_para += current_line
                            current_para += '\n' + current_line
                        else:
                            current_para += current_line
                        if current_line_len >= min_single_para_len:
                            all_para.append(current_para)
                            current_para = ""
                    else:
                        # 若本段加上下一段的长度大于总段限长，则归类为一个自然段
                        all_para.append(current_para)
                        current_para = current_line
        # 处理最后一个自然段
        if current_para != "":
            all_para.append(current_para)
        # with open('德国喜宝HIPP纯天然有机婴儿奶粉_para.json', 'w', encoding='utf-8') as fr:
        #     json.dump(all_para, fr, indent=4, ensure_ascii=False)
        # 封装document
        all_para_document = []
        for i, para in enumerate(all_para):
            all_para_document.append(Document(page_content=para, metadata={'source': file_name, 'para_num': i,
                                                                           'type': 'para'}))
        return all_para_document

    def compute_documents(self, loader_class):
        """
        Compute the documents from the file

        Args:
            loader_class (class): The class of the loader to use to load the file
        """

        documents = []
        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            tmp_file.write(self.content)  # pyright: ignore reportPrivateUsage=none
            tmp_file.flush()
            loader = loader_class(tmp_file.name)
            documents = loader.load()

        os.remove(tmp_file.name)
        self.origin_documents = documents
        self.para_documents = self.compute_para(documents)
        self.chunk_documents = self.chunk_text_splitter.split_documents(documents)

        self.mapping_chunk2para()

    def mapping_chunk2para(self):
        origin_docx_text = self.origin_documents[0].page_content
        para_index_in_chunk = []
        chunk_index_in_origin_docx = []
        para_index_in_origin_docx = []
        for i, chunk_doc in enumerate(self.chunk_documents):
            chunk_context = chunk_doc.page_content
            origin_start = origin_docx_text.find(chunk_context)
            # if origin_start == -1:
            #     split_chunk_context = chunk_context[:20]
            #     split_start = origin_docx_text.find(split_chunk_context)
            #     if split_start != -1:
            #         origin_start = split_start
            #     else:
            #         split_chunk_context = chunk_context[:10]
            #         split_start = origin_docx_text.find(split_chunk_context)
            #         if split_start != -1:
            #             origin_start = split_start
            end = origin_start + len(chunk_context) - 1

            chunk_index_in_origin_docx.append(
                (chunk_context, origin_start, end)
            )

        for i, para_doc in enumerate(self.para_documents):
            para_context = para_doc.page_content
            origin_start = origin_docx_text.find(para_context)
            if origin_start == -1:
                split_para_context = para_context[:20]
                if '\n' in split_para_context:
                    split_para_context = split_para_context.replace('\n', ' ')
                split_start = origin_docx_text.find(split_para_context)
                if split_start != -1:
                    origin_start = split_start
            #     else:
            #         split_para_context = para_context[:10]
            #         split_start = origin_docx_text.find(split_para_context)
            #         if split_start != -1:
            #             origin_start = split_start
            end = origin_start + len(para_context) - 1

            para_index_in_origin_docx.append(
                (para_context, origin_start, end)
            )

        for i, chunk_index in enumerate(chunk_index_in_origin_docx):
            chunk_st = chunk_index[1]
            chunk_end = chunk_index[2]
            contain_st_idx = -1
            contain_end_idx = -1
            for j, para_index in enumerate(para_index_in_origin_docx):
                para_st = para_index[1]
                para_end = para_index[2]
                if para_st <= chunk_st <= para_end and contain_st_idx == -1:
                    contain_st_idx = j
                if para_st <= chunk_end <= para_end and contain_end_idx == -1:
                    contain_end_idx = j
            if contain_st_idx != -1:
                if contain_end_idx != -1:
                    para_index_in_chunk.append(
                        [num for num in range(contain_st_idx, contain_end_idx + 1)]
                    )
                else:
                    contain_end_idx = contain_st_idx
                    para_index_in_chunk.append(
                        [num for num in range(contain_st_idx, contain_end_idx + 1)]
                    )
            else:
                if contain_end_idx != -1:
                    contain_st_idx = contain_end_idx
                    para_index_in_chunk.append(
                        [num for num in range(contain_st_idx - 1, contain_end_idx)]
                    )
                else:
                    print(chunk_index)
        for i in range(len(self.chunk_documents)):
            self.chunk_documents[i].metadata['para_num'] = list(para_index_in_chunk[i])
        print('')

        # chunk_range = []
        # para_range = []
        # contain_range = []
        # start = 0
        # end = 0
        # for i, chunk_doc in enumerate(self.chunk_documents):
        #     chunk_context = chunk_doc.page_content
        #     end += len(chunk_context)
        #     chunk_range.append(
        #         (start, end)
        #     )
        #     start += len(chunk_context)
        #
        # start = 0
        # end = 0
        # for i, para_doc in enumerate(self.para_documents):
        #     para_context = para_doc.page_content
        #     end += len(para_context)
        #     para_range.append(
        #         (start, end)
        #     )
        #     start += len(para_context)
        #
        # for i, chunk_index in enumerate(chunk_range):
        #     chunk_st = chunk_index[0]
        #     chunk_end = chunk_index[1]
        #     contain_st_idx = -1
        #     contain_end_idx = -1
        #     for j, para_index in enumerate(para_range):
        #         para_st = para_index[0]
        #         para_end = para_index[1]
        #         if para_st <= chunk_st <= para_end and contain_st_idx == -1:
        #             contain_st_idx = j
        #         if para_st <= chunk_end <= para_end and contain_end_idx == -1:
        #             contain_end_idx = j
        #     if contain_st_idx != -1 and contain_end_idx != -1:
        #         contain_range.append(
        #             [num for num in range(contain_st_idx, contain_end_idx + 1)]
        #         )
        # return chunk_range
