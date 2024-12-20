from supabase import create_client, Client
import random


url = "https://your-project-url.supabase.co"
key = "your-public-anon-key"


supabase: Client = create_client(url, key)


def criar_tabela():
    schema = """
    CREATE TABLE IF NOT EXISTS produtos (
        id SERIAL PRIMARY KEY,
        descricao TEXT,
        preco DECIMAL,
        quantidade INT
    );
    """
    supabase.rpc('execute_sql', {'query': schema}).execute()


def inserir_produtos():
    for i in range(30):
        descricao = f"Produto {i+1}"
        preco = round(random.uniform(5, 100), 2)  
        quantidade = random.randint(1, 200)  
        produto = {
            "descricao": descricao,
            "preco": preco,
            "quantidade": quantidade
        }
        supabase.table("produtos").insert(produto).execute()


def deletar_produtos_baratos():
    supabase.table("produtos").delete().eq("preco", 10).lt("preco", 10).execute()


def selecionar_produtos_estoque():
    response = supabase.table("produtos").select("*").gt("quantidade", 100).execute()
    return response.data


def aumentar_quantidade_produtos_baratos():
    supabase.table("produtos").update({"quantidade": supabase.rpc("quantidade + 10")}).lt("preco", 50).execute()


criar_tabela()         
inserir_produtos()     
deletar_produtos_baratos()  
produtos_com_estoque_maior_100 = selecionar_produtos_estoque()  
aumentar_quantidade_produtos_baratos()  


print("Produtos com quantidade maior que 100 no estoque:")
for produto in produtos_com_estoque_maior_100:
    print(produto)
