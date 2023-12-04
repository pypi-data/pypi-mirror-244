# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from aiopki.lib import JSONWebKey
from aiopki.types import IAlgorithm
from .algorithms import get as algorithm


class CryptoKeyVersion(pydantic.BaseModel):
    name: str
    alg: str
    enabled: bool
    thumbprint: str
    public: JSONWebKey | None = None

    def default_algorithm(self) -> IAlgorithm:
        return algorithm(self.alg)

    def process_signature(self, signature: bytes) -> bytes:
        if self.public is not None:
            signature = self.public.process_signature(signature)
        return signature
