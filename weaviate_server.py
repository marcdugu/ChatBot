# weaviate_server.py
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout

# Connect to Weaviate running in Docker on localhost:8080
client = weaviate.connect_to_local(
    additional_config=AdditionalConfig(
        timeout=Timeout(init=60, query=60, insert=120)  # a bit generous for first calls
    )
)