import os
import hashlib
import threading
import time
from queue import Queue
from urllib.parse import unquote, urlparse
import copy

import requests

from mtmtool.log import stream_logger


QUENE_DEQUENE_DELAY = 0.1
TRUST_HOSTNAMES_IN_REDIRECTING = ["urs.earthdata.nasa.gov"]

logger = stream_logger("Down")
logger_io = stream_logger("IO")


def extract_filename_from_headers(headers):
    # 检查 Content-Disposition header 是否存在
    if 'Content-Disposition' in headers:
        # 从 Content-Disposition header 中提取文件名
        content_disposition = headers['Content-Disposition']
        _, params = content_disposition.split(';')
        filename_param = next((param.strip() for param in params.split(';') if param.strip().startswith('filename=')), None)

        if filename_param:
            _, filename = filename_param.split('=')
            filename = unquote(filename.strip('\"'))
            return filename
    else:
        return ""

class TrustHostnameSession(requests.Session):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.trust_hostnames = kwargs.get("trust_hostnames", TRUST_HOSTNAMES_IN_REDIRECTING)

    def should_strip_auth(self, old_url, new_url):
        raw_flag = super().should_strip_auth(old_url, new_url)
        if raw_flag and urlparse(new_url).hostname in self.trust_hostnames:
            return False
        return raw_flag
    

class FileIntegrity:
    @staticmethod
    def size(path):
        if not os.path.isfile(path):
            return -1
        return os.path.getsize(path)
    
    @staticmethod
    def md5(path):
        if not os.path.isfile(path):
            return ""
        with open(path, "rb") as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            return md5.hexdigest()

    @staticmethod
    def rm(path):
        if not os.path.exists(path):
            return
        try:
            os.remove(path)
            info_text = "File remove success!"
        except Exception:
            info_text = "File remove failed!"
        logger_io.info(f"{info_text} {path}")


class SingleConnectionDownloaderThread(threading.Thread):
    def __init__(self, queue:Queue, session=None, timeout=None, check_integrity=False, should_wait=False, only_file = True, **kwargs):
        super().__init__(daemon=kwargs.get("daemon", None)) # 线程守护

        # 设置请求会话
        self.session = session or TrustHostnameSession() # requests session
        if "cookies" in kwargs:
            self.session.cookies.update(kwargs["cookies"])
        if "headers" in kwargs:
            self.session.headers.update(kwargs["headers"])
        if "auth" in kwargs:
            self.session.auth = kwargs["auth"]
        if "proxies" in kwargs:
            self.session.proxies = kwargs["proxies"]
        if "trust_hostnames" in kwargs:
            self.session.trust_hostnames = kwargs["trust_hostnames"]

        # 设置下载任务队列
        self.quene = queue if queue else None # 下载任务队列
        self.should_wait = should_wait # 是否等待下载任务, 每次下载任务完成后, 等待wait_event被唤醒
        self.only_file = only_file

        assert isinstance(queue, Queue), "queue is not Queue class"

        # 下载任务默认参数
        self.default = {
            "method": "GET",
            "url": "https://",
            "filedir": "",
            "filename": "",
            "size": -1,
            "md5": "",
            "chunk_size": 1024 * 1024,
            "timeout": timeout,
            "check_integrity": check_integrity,
        }

        # 线程控制条件
        self.wait_event = threading.Event()
        self.running = False
        self.error = None
        self.exit = False

    def check_file_integrity(self, item, force=False):
        # 检查文件md5
        if md5:=FileIntegrity.md5(item.get("path", "")) if item.get("md5", "") else None:
            return md5 == (item.get("md5", "") )
        # 检查文件大小
        if size:=FileIntegrity.size(item.get("path", "")) if item.get("size", -1) > 0 else None:
            return size == (item.get("size", -1) )
        # 看看是否设置了不检查文件完整性, 如果设置中不检查文件完整性, 则默认为完整
        if not item.get("check_integrity", False) and not force: # force参数用于强制检查文件完整性
            return True
        return False

    def get_file_path(self, item, headers):
        # 获取文件路径
        web_file_name = extract_filename_from_headers(headers)
        url_file_name = os.path.basename(urlparse(item.get("url", "")).path)
        raw_file_name = os.path.basename(item.get("filename", "")) if item.get("filename", "") else ""
        if raw_file_name:
            file_name = raw_file_name
        elif web_file_name:
            file_name = web_file_name
        elif url_file_name:
            file_name = url_file_name
        file_dir = item.get("filedir", "")
        if file_dir:
            file_path = os.path.join(file_dir, file_name)
        else:
            file_path = file_name
        assert file_name, f"File name {file_name} is empty"
        return file_path, file_dir, file_name

    def print_success_info(self, item):
        filesize = FileIntegrity.size(item["path"])
        info_text = "File Downloaded ({:.4f}MB)!".format(filesize / 1024 / 1024)
        file_name = os.path.basename(item["path"])
        logger.info(f"{info_text} {file_name}")

    def run(self):
        while True:
            # 等待线程被唤醒
            self.wait_event.wait() if self.should_wait else None

            # 检查是否退出
            if self.exit:
                break

            # 获取下载任务
            item = self.default.copy()
            item.update(self.quene.get())
            self.running = True
            response = None

            try:
                # 发送请求
                response = self.session.request(
                    method="HEAD", 
                    url=item.get("url", "https://"), 
                    timeout=item.get("timeout", None),
                    stream=False,
                    allow_redirects=True
                )
                response.raise_for_status()
                response.close()
                headers = response.headers.copy()

                # 检查请求是否是文件下载请求
                if self.only_file and "Content-Length" not in headers and headers["Content-Type"].startswith("text"):
                    logger.error(f"{item.get('url', 'https://')} is not a file!")
                    continue

                # 获取文件路径
                file_path, file_dir, file_name = self.get_file_path(item, headers)
                item["path"] = file_path
                
                # 获取文件大小
                response_content_length = int(headers.get("Content-Length", -1))
                if item.get("size", -1) < 0 and response_content_length > 0:
                    item["size"] = response_content_length
                
                # 记录此次请求的信息
                with open(".downtmp", 'a') as fp:
                    text = item.get("url", "https://") + "," + file_name + "," + str(response_content_length) + "\n"
                    fp.write(text)
                
                # 下载前强制检查文件完整性, 如果文件不完整, 则删除文件重新下载, 如果文件完整, 则跳过下载
                is_integrity_predownload = self.check_file_integrity(item, force=True)
                if is_integrity_predownload:
                    self.print_success_info(item)
                    continue
                
                # 删除之前的文件
                FileIntegrity.rm(file_path)
                
                # 分块下载文件
                logger.info(f"Downloading File: {file_name}")
                response = self.session.request(
                    method=item.get("method", "GET"), 
                    url=item.get("url", "https://"), 
                    timeout=item.get("timeout", None),
                    stream=True,
                    allow_redirects=True
                )
                response.raise_for_status()
                with open(file_path, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=item.get("chunk_size", None)):
                        fd.write(chunk)

                # 检查文件完整性, 如果要求检查文件且文件不完整, 则删除文件
                is_integrity = self.check_file_integrity(item, force=False)
                if is_integrity:
                    self.print_success_info(item)
                else:
                    FileIntegrity.rm(file_path)

            except requests.exceptions.RequestException as e:
                logger.error(e)
            except Exception as e:
                self.error = e
            finally:
                # 单次任务完成
                response.close() if response else None
                self.running = False
                self.wait_event.clear() if self.should_wait else None


class SingleConnectionDownloaderThreadPool:
    quene_default = Queue()
    def __init__(self, max_threads = 1, **kwargs) -> None:
        super().__init__()
        self.max_threads = max_threads
        self.quene = Queue()
        kwargs.update({
            "queue": self.quene,
            "daemon": True,
            "should_wait": True,
        })
        self.kwargs = kwargs
        pass

    def put(self, **kwargs):
        self.quene.put(kwargs)

    def start(self):
        self.downloader_pools = [SingleConnectionDownloaderThread(**self.kwargs) for _ in range(self.max_threads)]
        for thread in self.downloader_pools:
            thread.wait_event.clear()
            thread.start()
        while True:
            for thread in self.downloader_pools:
                if thread.error:
                    raise thread.error
            if self.quene.empty():
                if not any([thread.running for thread in self.downloader_pools]):
                    for thread in self.downloader_pools:
                        thread.exit = True
                        thread.wait_event.set()
                    break
                time.sleep(0.1)
            else:
                for thread in self.downloader_pools:
                    if not thread.wait_event.is_set():
                        thread.wait_event.set()
                        break
                time.sleep(QUENE_DEQUENE_DELAY)
    


def download_from_dataframe(pool:SingleConnectionDownloaderThreadPool, df, obj_dir:str=".", tmp_csv:str="tempfileinfos.csv", loop_times=10):
    import pandas as pd
    flag_all_complete = False
    for _ in range(loop_times):
        # 如果所有文件都下载完成, 则跳过
        if flag_all_complete:
            continue

        # 检查是否有URL字段需要下载
        assert "url" in df.columns, "url column is not in the dataframe!"

        # 检查是否有文件名称字段, 如果没有, 则设置为空
        if "filename" not in df.columns:
            df["filename"] = ""
        
        # 将未完成下载的文件加入下载队列
        for _, row in df.iterrows():
            _dict = {"filedir": obj_dir}
            filepath = os.path.join(obj_dir, row.get("filename", ""))
            if "filedir" in row and row["filedir"]:
                _dict["filedir"] = row["filedir"]
            if "filename" in row and row["filename"] and os.path.isfile(filepath):
                flag_file_size = "size" in row and row["size"] > 0 and FileIntegrity.size(filepath) == row["size"]
                flag_file_md5 = "md5" in row and row["md5"] and FileIntegrity.md5(filepath) == row["md5"]
                if flag_file_size or flag_file_md5:
                    continue
            _dict.update(row.to_dict())
            pool.put(**_dict)

        # 开始下载
        pool.start()

        # 后处理
        if os.path.exists(".downtmp"):
            df_temp = pd.read_csv(".downtmp", header=None, names=["url", "filename", "size"])
            df_temp.drop(index=df_temp[df_temp["size"] < 0].index, inplace=True)
            df_temp.drop_duplicates(subset=["url"], keep="last", inplace=True)
            df_merge = df.merge(df_temp, on="url", how="left", suffixes=("", "_y"))
            # 当出现重复字段时, 使用新字段的值替换原始字段的值
            if "filename_y" in df_merge.columns:
                df["filename"] = df_merge["filename_y"].fillna(df_merge["filename"])
            if "size_y" in df_merge.columns:
                df["size"] = df_merge["size_y"].fillna(df_merge["size"])
            # 删除全为nan值的列
            df.dropna(axis=1, how="all", inplace=True)
            df.to_csv(tmp_csv, index=False)
            FileIntegrity.rm(".downtmp") if os.path.exists(".downtmp") else None
        else:
            flag_all_complete = True
    else:
        logger.info("下载完成") if flag_all_complete else logger.info("下载未完成")
        logger.info(f"本次下载的文件完整信息请查看: {tmp_csv}")