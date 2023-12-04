# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest_asyncio

import aiopki
from canonical import ResourceName


@pytest_asyncio.fixture(scope='module') # type: ignore
async def signing_key(key_uri: ResourceName | str) -> aiopki.types.ICryptoKey:
    return await aiopki.CryptoKeyType.parse(key_uri) # type: ignore