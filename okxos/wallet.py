from okxos.client import OKXClient


class WalletAPI:
    def __init__(self, client: OKXClient):
        self.client = client

    # 查询支持的区块链 api/v5/wallet/chain/supported-chains
    async def get_supported_chains(self):
        """
        查询支持的区块链

        官方文档: https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-get-supported-blockchain
        """
        endpoint = "/api/v5/wallet/chain/supported-chains"
        return await self.client.request("GET", endpoint)

    async def get_current_prices(self, token_data_list):
        """
        获取指定代币的当前价格

        官方文档: https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-get-current-pricelist

        :param token_data_list: 包含代币信息的列表，每个元素为字典，格式如下：
            [
                {"chainIndex": "1", "tokenAddress": "0xc18360217d8f7ab5e7c516566761ea12ce7f9d72"},
                {"chainIndex": "0", "tokenAddress": "btc-brc20-ordi"}
            ]
        :return: 实时价格信息的 JSON 数据
        """
        endpoint = "/api/v5/wallet/token/current-price"
        return await self.client.request("POST", endpoint, body=token_data_list)

    async def get_historical_prices(
            self,
            chain_index,
            token_address=None,
            limit=50,
            cursor=None,
            begin=None,
            end=None,
            period="1d",
    ):
        """
        查询某个币种的历史价格

        官方文档: https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-get-historical-pricelist

        :param chain_index: 链唯一标识。
        :param token_address: 代币地址或标识符，可选。
        :param limit: 每次查询返回的条数，默认 50，最大 200。
        :param cursor: 游标位置，默认为第一个。
        :param begin: 查询晚于该时间的历史币价，单位毫秒时间戳。
        :param end: 查询早于该时间的历史币价，单位毫秒时间戳。
        :param period: 时间间隔单位，支持 1m, 5m, 30m, 1h, 1d，默认值为 1d。
        :return: 历史币价的 JSON 数据。
        """
        endpoint = "/api/v5/wallet/token/historical-price"
        params = {
            "chainIndex": chain_index,
            "limit": str(limit),
            "period": period,
        }
        if token_address is not None:
            params["tokenAddress"] = token_address
        if cursor is not None:
            params["cursor"] = cursor
        if begin is not None:
            params["begin"] = str(begin)
        if end is not None:
            params["end"] = str(end)

        return await self.client.request("GET", endpoint, params=params)