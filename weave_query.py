import weaviate
import config
import pprint
import sys

from lib.database import weaviate_query
from lib.ai import ai

client = weaviate.Client(
    url=config.weaviate_url,
    additional_headers={
        "X-OpenAI-Api-Key": config.openai_token
    }
)
query = input("enter query: ")


near_text_filter = {
  "concepts": [query],
  "moveTo": {
    "concepts": [""],
    "force": 0.5
  }
}
additional_clause = {
  "featureProjection": [
    "vector"
  ]
}

additional_setting = {
  "dimensions": 3
}

query_result = (
  client.query
  .get("Document", ["fragment", "gpt_fragment"])
  .with_near_text(near_text_filter)
  .with_additional(
    (additional_clause, additional_setting)
  )
  .do()
)

datas = query_result.get('data').get('Get').get('Document')
content = ""
for i, data in enumerate(datas):
	content = content + " " + data.get('gpt_fragment')
	
	if i > 10:
		document = {"plain": query, "content": content}
		print(document)
		print(ai("prime_chat", document).get('answer', "None"))
		break

sys.exit()

xs = []
ys = []
texts = []

for data in datas:
	print(data.get('sentence')[:100], data.get("_additional").get('featureProjection').get('vector'))
	# xs.append(data.get("_additional").get('featureProjection').get('vector')[0])
	# ys.append(data.get("_additional").get('featureProjection').get('vector')[1])
	# texts.append(data.get('title')[:20])

sys.exit()

import plotly.express as px
fig = px.scatter(x=xs, y=ys, text=texts)

fig.show()

"""
all_objects = client.data_object.get(class_name="Support")
print(all_objects)

import sys
sys.exit()

schema = client.schema.get()
for classe in schema.get('classes'):
	print(classe.get('class'))
"""

document = {"plain": query}
collection = "Docs"
fields = ["url", "title", "sentence"]
records = weaviate_query([query], collection, fields)

for i, record in enumerate(records):
	if i > 10:
		break
	print(record)

"""
for doc in documents:
	nearText = {
	  "concepts": [doc.get('plain')],
	  "distance": 0.7,
	}
	print("=========================================")
	print("========", doc.get('plain'))
	result = (
	  client.query
	  .get("Slothbot", ["table","plain","sql"])
	  .with_additional(["certainty", "distance"])
	  .with_near_text(nearText)
	  .do()
	)

	for record in result.get('data').get('Get').get('Slothbot'):
		print(record.get('_additional').get('certainty'), "|", record.get('_additional').get('distance'), "|", record.get('table'), "|", record.get('sql'))

documents = [
	{"plain": "select from planets"}
]
for doc in documents:
	nearText = {
	  "concepts": [doc.get('plain')],
	  "distance": 0.2,
	}
	print("=========================================")
	print("========", doc.get('plain'))
	result = (
	  client.query
	  .get("Slothbot", ["plain"])
	  .with_additional(["certainty", "distance", "id"])
	  .with_near_text(nearText)
	  .do()
	)

	for record in result.get('data').get('Get').get('Slothbot'):
		print(record.get('_additional').get('certainty'), "|", record.get('_additional').get('distance'), "|", record.get('table'), "|", record.get('sql'))

"""
