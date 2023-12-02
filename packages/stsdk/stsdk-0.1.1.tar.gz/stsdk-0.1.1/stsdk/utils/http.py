import httpx

timeout = 1


class Request:
    def get(self, url, headers=None, params=None):
        resp = httpx.get(url, headers=headers, params=params, timeout=timeout)
        return resp.json()

    def post(self, url, data, headers=None):
        resp = httpx.post(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def patch(self, url, data, headers=None):
        resp = httpx.patch(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def delete(self, url, data, headers=None):
        resp = httpx.delete(url, headers=headers, data=data, timeout=timeout)
        return resp.json()

    def close(self):
        self.session.close()


request = Request()
