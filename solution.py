import os
import requests
import folium
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env
load_dotenv(".env", override=True)

# 1. Autenticação na API SPTrans (conforme o slide)
s = requests.Session()
token = os.getenv("SPTRANS_TOKEN")
login_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}"
res_login = s.post(login_url)
print("Autenticação:", res_login.json())

# 2. Busca pelas Paradas da Linha 2506 (conforme o slide)
res_paradas = s.get("http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha=2506")
paradas = res_paradas.json()

# 3. Busca pelas Posições dos Ônibus em Tempo Real (conforme o slide)
res_pos = s.get("http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha=2506")
posicoes = res_pos.json()

# 4. Criação do Mapa usando Folium (conforme o slide)
# Centraliza o mapa na primeira parada da lista
m = folium.Map(location=[paradas[3]["py"], paradas[3]["px"]], zoom_start=14)

# 5. Adiciona os pinos das Paradas de Ônibus (Cor: Azul - requisito da atividade)
for i in paradas:
    folium.Marker(
        location=[i["py"], i["px"]],
        popup=i["np"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 6. Adiciona os pinos dos Ônibus em Tempo Real (Cor: Vermelho - requisito da atividade)
veiculos = posicoes.get("vs", []) if isinstance(posicoes, dict) else []
for v in veiculos:
    folium.Marker(
        location=[v["py"], v["px"]],
        popup=f"Ônibus: {v.get('p')}",
        icon=folium.Icon(color="red", icon="bus", prefix="fa")
    ).add_to(m)

# 7. Salva o Mapa no repositório (requisito da atividade)
m.save("mapa_sptrans.html")
print("Mapa gerado com sucesso!")

