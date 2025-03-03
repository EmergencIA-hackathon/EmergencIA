import aiohttp
import asyncio

async def coordenadas_para_endereco(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&addressdetails=1"
    headers = {"User-Agent": "Mozilla/5.0"}  # Define um User-Agent para evitar bloqueios
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                dados = await response.json()
                if "address" in dados:
                    return dados["display_name"]  # Retorna o endereço completo
                else:
                    return "Endereço não encontrado."
            else:
                return f"Erro na requisição: {response.status}"
