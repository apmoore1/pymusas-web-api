from httpx import AsyncClient
import pytest

from pymusas_web_api.server import SpacyToken, SupportedLanguages, app


@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'


@pytest.mark.anyio
async def test_tag() -> None:
    params = {'lang': SupportedLanguages.french.value, 'text': 'bonjour ca va'}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/", params=params)
        assert response.status_code == 200
        json_response = response.json()
        assert 3 == len(json_response)
        # Test that each token in response can be converted into a SpacyToken
        [SpacyToken(**token) for token in json_response]

        # Test for incorrect parameters
        response = await ac.get("/")
        assert response.status_code == 422


@pytest.mark.anyio
async def test_supported_languages() -> None:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/supported-languages')
        assert response.status_code == 200
        json_response = response.json()
        supported_languages = [language.value for language in SupportedLanguages]
        assert len(supported_languages) == len(json_response)
        assert set(supported_languages) == set(json_response)
