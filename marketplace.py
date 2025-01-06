from okxos.client import OKXClient


class MarketplaceAPI:
    def __init__(self, client: OKXClient):
        self.client = client

    # 获取合集信息 GET https://www.okx.com/api/v5/mktplace/nft/runes/detail
    async def get_collection_info(self, runes_id: str):
        """
        获取合集信息
        官方文档:https://www.okx.com/zh-hans/web3/build/docs/waas/marketplace-get-runes-collection

        :param runes_id: 合集ID

        """
        endpoint = "/api/v5/mktplace/nft/runes/detail"
        params = {
            "runesId": runes_id
        }
        return await self.client.request("GET", endpoint, params)

