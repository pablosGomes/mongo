from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Dict, List

# Configuração de conexão
MONGO_URI = "mongodb://admin:password@localhost:27017/?authSource=admin"
DB_NAME = "meuBanco"
COLLECTION_NAME = "minhaCollection"

class MongoDBHandler:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def insert_document(self, document: Dict) -> Dict:
        self.collection.insert_one(document)
        return document

    def insert_many_documents(self, documents: List[Dict]) -> List[Dict]:
        self.collection.insert_many(documents)
        return documents

    def find_documents(self, filter_query: Dict = {}) -> List[Dict]:
        return list(self.collection.find(filter_query, {"_id": 0}))

    def find_one_document(self, filter_query: Dict) -> Dict:
        return self.collection.find_one(filter_query, {"_id": 0})

    def update_document(self, object_id: str, update_fields: Dict) -> int:
        result = self.collection.update_one(
            {"_id": ObjectId(object_id)},
            {"$set": update_fields}
        )
        return result.modified_count

    def update_many_documents(self, filter_query: Dict, update_fields: Dict) -> int:
        result = self.collection.update_many(filter_query, {"$set": update_fields})
        return result.modified_count

    def delete_document(self, object_id: str) -> int:
        result = self.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count

    def delete_many_documents(self, filter_query: Dict) -> int:
        result = self.collection.delete_many(filter_query)
        return result.deleted_count

    def create_ttl_index(self, field_name: str, expire_seconds: int):
        self.collection.create_index(field_name, expireAfterSeconds=expire_seconds)

# Exemplo de uso
if __name__ == "__main__":
    mongo_handler = MongoDBHandler()
    
    # Inserir documento
    doc = {"nome": "João", "idade": 25, "data_de_criacao": datetime.utcnow()}
    mongo_handler.insert_document(doc)
    
    # Buscar todos
    print(mongo_handler.find_documents())
    
    # Criar índice TTL
    mongo_handler.create_ttl_index("data_de_criacao", 3600)
