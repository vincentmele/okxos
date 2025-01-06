from okxos.client import OKXClient


class DeFiAPI:
    def __init__(self, client: OKXClient):
        self.client = client

    async def get_protocol_list(self, platform_id=None, platform_name=None):
        """
        查询协议列表

        官方文档: https://www.okx.com/zh-hans/web3/build/docs/waas/defi-api-reference-explore-protocol-list

        :param platform_id: 平台 ID，可选。
        :param platform_name: 平台官方名称，可选。
        :return: 协议信息的 JSON 数据。
        """
        endpoint = "/api/v5/defi/explore/protocol/list"
        params = {}
        if platform_id:
            params["platformId"] = platform_id
        if platform_name:
            params["platformName"] = platform_name

        return await self.client.request("GET", endpoint, params=params)


