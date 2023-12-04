# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .types import IAlgorithm
from .resource import Resource
from .versionedcryptokey import VersionedCryptoKey


__all__: list[str] = [
    'CryptoKeyType'
]


class CryptoKeyType(Resource[VersionedCryptoKey]):
    __module__: str = 'aiopki'
    model = VersionedCryptoKey

    @property
    def crv(self) -> str | None:
        return None

    @property
    def thumbprint(self) -> str:
        return self.impl.thumbprint

    def can_use(self, algorithm: IAlgorithm) -> bool:
        return self.impl.can_use(algorithm)

    async def discover(self):
        if not self.ready:
            await self.impl
        return self

    async def sign(
        self,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bytes:
        await self.impl
        version = self.impl.get(using)
        return await self.impl.sign(version, message, algorithm or version.default_algorithm())

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        algorithm: IAlgorithm | None = None,
        using: str | None = None
    ) -> bool:
        await self.impl
        if using and not self.impl.has(using):
            return False
        version = self.impl.get(using)
        return await self.impl.verify(
            version=version,
            signature=signature,
            message=message,
            algorithm=algorithm or version.default_algorithm(),
        )

    def __await__(self):
        return self.discover().__await__()