# check_pinecone_env.py
import pinecone

pinecone.init(api_key="pcsk_4eHQrh_7TYoyMWmcUUaE4ndViBKPgPwuXns7Yw8SDrR19pu3nvjB9oLQXhGdeivq4UsSEG", environment="us-west4-gcp")  # Replace with your environment

print("✅ Pinecone initialized successfully.")
print("Indexes:", pinecone.list_indexes())
