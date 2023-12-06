import requests
import json
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.base_function import BaseFunction


class UrlFunction(BaseFunction):
    def __init__(self):
        pass

    def get_name(self):
        return "url"

    def process(self, params, table_writer, context):
        endpoint = params[0]

        try:
            response = requests.get(endpoint)
            status_code = response.status_code
            logger.debug(
                "processing url function",
                endpoint=endpoint,
                status_code=status_code,
                encoding=response.encoding,
                content_type=response.headers["content-type"],
            )
            if status_code != 200:
                logger.error("status code is not 200")
                return
            if response.encoding != "utf-8":
                logger.error("encoding is not utf-8")
                return
            if "application/json" not in response.headers["content-type"]:
                logger.error("content is not json")
                return
            # json_data = json.loads(response.text)
            json_data = response.json()
            if isinstance(json_data, list):
                # json array
                for obj in json_data:
                    # item in array is dict
                    if isinstance(obj, dict):
                        kv_pair = {}
                        for k, v in obj.items():
                            if isinstance(v, dict):
                                kv_pair[k] = json.dumps(v)
                            else:
                                kv_pair[k] = v
                        table_writer.write_row(kv_pair)
                    else:
                        kv_pair = {}
                        # FIX ME: for temp use a default key name, since it's not a dict, should use a better name
                        if isinstance(obj, dict):
                            kv_pair["default_key"] = json.dumps(v)
                        else:
                            kv_pair["default_key"] = obj
                        table_writer.write_row(kv_pair)
            elif isinstance(json_data, dict):
                # json obejct
                kv_pair = {}
                for k, v in json_data.items():
                    if isinstance(v, dict):
                        kv_pair[k] = json.dumps(v)
                    else:
                        kv_pair[k] = v
                table_writer.write_row(kv_pair)

        except Exception as ex:
            logger.error(
                f"failed to get json response from http server: {endpoint}",
                error=str(ex),
            )
