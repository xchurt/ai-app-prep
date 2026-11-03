import asyncio
import time
import httpx
async def fetch_delay(client:httpx.AsyncClient,seconds:int):
    resp=await client.get(f"https://httpbin.org/delay/{seconds}")
    return {"delay":seconds,"status":resp.status_code}
async def main():
    start=time.time()
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(fetch_delay(client,1),fetch_delay(client,1),fetch_delay(client,1),fetch_delay(client,1))
        elapsed=time.time()-start
        print(f"总耗时:{elapsed:.2f}秒")
        print(f"结果:{results}")
if __name__=="__main__":
    asyncio.run(main())