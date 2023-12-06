import json

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tmt.v20180321 import models, tmt_client

from . import Translate


class TencentTranslate(Translate):
    def __init__(self, **kwargs) -> None:
        if not {"secret_key", "secret_id"}.issubset(kwargs):
            raise ValueError("secret_key,secret_id must be provided")
        self.secret_key = kwargs["secret_key"]
        self.secret_id = kwargs["secret_id"]

    def translate(
        self, word: str, source_language_code: str, target_language_code: str
    ) -> str:
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            # 实例化要请求产品的client对象,clientProfile是可选的
            client = tmt_client.TmtClient(cred, "ap-shanghai", clientProfile)

            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.TextTranslateRequest()
            params = {
                # "SourceText": "It was a bright cold day in April, and the clocks were striking thirteen.",
                "SourceText": "apple",
                "Source": "en",
                "Target": "zh",
                "ProjectId": 0,
            }
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个TextTranslateResponse的实例，与请求对象对应
            resp = client.TextTranslate(req)
            # 输出json格式的字符串回包
            res: dict = json.loads(resp.to_json_string())
            res_demo = {
                "TargetText": "这是四月一个晴朗寒冷的日子，时钟敲了十三下。",
                "Source": "en",
                "Target": "zh",
                "RequestId": "eb433f3e-d71b-41ef-84e3-62520a87da8c",
            }
            res2_demo = {
                "TargetText": "苹果",
                "Source": "en",
                "Target": "zh",
                "RequestId": "4dd3fc9c-fd76-47d1-a80d-b1762a8f7462",
            }
            return res

        except TencentCloudSDKException as err:
            print(err)

    def translate_word(self, word: str) -> str:
        ...

    def format_sentence_response(self, response: dict) -> dict:
        ...

    def format_word_response(self, response: dict) -> dict:
        ...

    def download_audio_file(self, url: str) -> bytes:
        ...
