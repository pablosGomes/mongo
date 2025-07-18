from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from datetime import datetime

class MongoAdvancedHandler:
    def __init__(self):
        self.client = MongoClient("mongodb://admin:password@localhost:27017/?authSource=admin")
        self.db = self.client["bancoAvancado"]
        self.collection = self.db["usuarios"]

    def inserir_usuario(self, nome: str, idade: int, interesses: list):
        usuario = {
            "nome": nome,
            "idade": idade,
            "interesses": interesses,
            "data_cadastro": datetime.utcnow()
        }
        self.collection.insert_one(usuario)
        return usuario

    def buscar_por_interesse(self, interesse: str):
        return list(self.collection.find({"interesses": interesse}))

    def buscar_ordenado_por_idade(self, limite: int = 5):
        return list(self.collection.find().sort("idade", ASCENDING).limit(limite))

    def atualizar_interesses(self, usuario_id: str, novos_interesses: list):
        resultado = self.collection.update_one(
            {"_id": ObjectId(usuario_id)},
            {"$set": {"interesses": novos_interesses}}
        )
        return resultado.modified_count

    def deletar_usuarios_menores_de_idade(self):
        resultado = self.collection.delete_many({"idade": {"$lt": 18}})
        return resultado.deleted_count

    def criar_indices(self):
        self.collection.create_index([("nome", ASCENDING)])
        self.collection.create_index([("idade", DESCENDING)])

if __name__ == "__main__":
    handler = MongoAdvancedHandler()
    handler.criar_indices()

    # Exemplos de inserção
    handler.inserir_usuario("Maria", 22, ["música", "livros"])
    handler.inserir_usuario("Carlos", 17, ["games", "filmes"])
    
    # Buscar
    print(handler.buscar_por_interesse("games"))
    print(handler.buscar_ordenado_por_idade())
    
    # Atualizar (substituir por um id válido real)
    # print(handler.atualizar_interesses("64cc1a5fc7c9a8a3b7d9f123", ["esportes", "viagem"]))

    # Deletar menores
    print(handler.deletar_usuarios_menores_de_idade())
