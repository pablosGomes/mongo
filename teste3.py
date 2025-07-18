from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

class ProdutosHandler:
    def __init__(self):
        self.client = MongoClient("mongodb://admin:password@localhost:27017/?authSource=admin")
        self.db = self.client["loja_virtual"]
        self.collection = self.db["produtos"]

    def adicionar_produto(self, nome: str, preco: float, categorias: list, estoque: int):
        produto = {
            "nome": nome,
            "preco": preco,
            "categorias": categorias,
            "estoque": estoque,
            "data_cadastro": datetime.utcnow()
        }
        self.collection.insert_one(produto)
        return produto

    def buscar_produtos_disponiveis(self):
        return list(self.collection.find({"estoque": {"$gt": 0}}))

    def buscar_por_categoria_e_preco(self, categoria: str, preco_max: float):
        return list(self.collection.find({
            "categorias": categoria,
            "preco": {"$lte": preco_max}
        }).sort("preco", 1))

    def atualizar_preco_em_lote(self, percentual: float):
        fator = 1 + percentual / 100
        resultado = self.collection.update_many(
            {},
            {"$mul": {"preco": fator}}
        )
        return resultado.modified_count

    def remover_produto(self, produto_id: str):
        resultado = self.collection.delete_one({"_id": ObjectId(produto_id)})
        return resultado.deleted_count

    def criar_indice_composto(self):
        self.collection.create_index([("categorias", 1), ("preco", 1)])

if __name__ == "__main__":
    handler = ProdutosHandler()
    handler.criar_indice_composto()

    handler.adicionar_produto("Mouse Gamer", 150.0, ["tecnologia", "perifericos"], 20)
    handler.adicionar_produto("Teclado Mecânico", 400.0, ["tecnologia", "perifericos"], 15)

    print(handler.buscar_produtos_disponiveis())
    print(handler.buscar_por_categoria_e_preco("tecnologia", 300))
    print(handler.atualizar_preco_em_lote(5))
