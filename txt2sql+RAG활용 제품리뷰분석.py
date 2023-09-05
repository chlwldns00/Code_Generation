from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
    column,
)

from sqlalchemy import insert
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index import Document, ListIndex
from llama_index import SQLDatabase, ServiceContext
from llama_index.llms import ChatMessage, OpenAI
from typing import List
import ast
from IPython.display import display, HTML
#from llama_index.llms import llm
import os
import openai
import nltk


#예제 데이터
rows = [
    # iPhone13 Reviews
    {"id": 1, "category": "Phone", "product_name": "Iphone13", "review": "Amazing battery life and camera quality. Best iPhone yet."},
    {"id": 2, "category": "Phone", "product_name": "Iphone13", "review": "Stunning design and performance. Apple has done it again."},
    {"id": 3, "category": "Phone", "product_name": "Iphone13", "review": "The display is just incredible. Love the A15 chip's speed."},
    {"id": 4, "category": "Phone", "product_name": "Iphone13", "review": "Superb user experience with the new iOS. Seamless and smooth."},
    {"id": 5, "category": "Phone", "product_name": "Iphone13", "review": "5G capabilities are outstanding. Internet browsing is lightning fast."},
    {"id": 6, "category": "Phone", "product_name": "Iphone13", "review": "The build quality is top-notch. Feels premium in hand."},
    {"id": 7, "category": "Phone", "product_name": "Iphone13", "review": "Love the enhanced camera system. Pictures are more vivid."},
    {"id": 8, "category": "Phone", "product_name": "Iphone13", "review": "Face ID is faster and more responsive."},
    {"id": 9, "category": "Phone", "product_name": "Iphone13", "review": "Storage options are great. Worth the investment."},
    {"id": 10, "category": "Phone", "product_name": "Iphone13", "review": "Night mode photos are simply outstanding."},
    {"id": 11, "category": "Phone", "product_name": "Iphone13", "review": "The ceramic shield front cover is a nice touch."},
    {"id": 12, "category": "Phone", "product_name": "Iphone13", "review": "Battery life lasts all day even with heavy use."},
    {"id": 13, "category": "Phone", "product_name": "Iphone13", "review": "Video recording quality is cinema-grade."},
    {"id": 14, "category": "Phone", "product_name": "Iphone13", "review": "Gaming experience is smooth with no lags."},
    {"id": 15, "category": "Phone", "product_name": "Iphone13", "review": "Dual eSIM support is a game changer for travelers."},
    {"id": 16, "category": "Phone", "product_name": "Iphone13", "review": "Stereo speakers produce clear and loud audio."},
    {"id": 17, "category": "Phone", "product_name": "Iphone13", "review": "MagSafe accessories add to its versatility."},
    {"id": 18, "category": "Phone", "product_name": "Iphone13", "review": "Water and dust resistance is reliable."},
    {"id": 19, "category": "Phone", "product_name": "Iphone13", "review": "Graphics and performance are top-tier."},
    {"id": 20, "category": "Phone", "product_name": "Iphone13", "review": "All-around, the best smartphone on the market."},

    # SamsungTV Reviews
    {"id": 21, "category": "TV", "product_name": "SamsungTV", "review": "Impressive picture clarity and vibrant colors. A top-notch TV."},
    {"id": 22, "category": "TV", "product_name": "SamsungTV", "review": "Love the smart features and the remote. Simplifies everything."},
    {"id": 23, "category": "TV", "product_name": "SamsungTV", "review": "Sound quality could be better. Picture is stunning though."},
    {"id": 24, "category": "TV", "product_name": "SamsungTV", "review": "Connectivity options are plenty and easy to set up."},
    {"id": 25, "category": "TV", "product_name": "SamsungTV", "review": "Sleek design that complements the living room decor."},
    {"id": 26, "category": "TV", "product_name": "SamsungTV", "review": "The built-in apps and interface are user-friendly."},
    {"id": 27, "category": "TV", "product_name": "SamsungTV", "review": "Ambient mode is a nice touch for when not watching."},
    {"id": 28, "category": "TV", "product_name": "SamsungTV", "review": "Gaming mode offers a fantastic experience with low latency."},
    {"id": 29, "category": "TV", "product_name": "SamsungTV", "review": "HDR content looks spectacular."},
    {"id": 30, "category": "TV", "product_name": "SamsungTV", "review": "Remote control with voice command is super convenient."},
    {"id": 31, "category": "TV", "product_name": "SamsungTV", "review": "Crisp and clear audio, though an external system enhances it."},
    {"id": 32, "category": "TV", "product_name": "SamsungTV", "review": "Wall mounting was straightforward and secure."},
    {"id": 33, "category": "TV", "product_name": "SamsungTV", "review": "Streaming apps load quickly and play smoothly."},
    {"id": 34, "category": "TV", "product_name": "SamsungTV", "review": "Regular software updates keep the TV fresh."},
    {"id": 35, "category": "TV", "product_name": "SamsungTV", "review": "Multiple HDMI ports allow for various device connections."},
    {"id": 36, "category": "TV", "product_name": "SamsungTV", "review": "Power consumption is efficient."},
    {"id": 37, "category": "TV", "product_name": "SamsungTV", "review": "Tizen OS is intuitive and bug-free."},
    {"id": 38, "category": "TV", "product_name": "SamsungTV", "review": "The contrast ratio and deep blacks are impressive."},
    {"id": 39, "category": "TV", "product_name": "SamsungTV", "review": "No motion blur during fast-paced scenes."},
    {"id": 40, "category": "TV", "product_name": "SamsungTV", "review": "Overall, a solid investment for quality viewing."},

    # Ergonomic Chair Reviews
    {"id": 41, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Feels really comfortable even after long hours."},
    {"id": 42, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Assembly was a bit tough, but the comfort is unmatched."},
    {"id": 43, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Good support for back but wish it had more adjustability."},
    {"id": 44, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "The material breathes well. No more sweaty backs."},
    {"id": 45, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Sturdy build and doesn't wobble."},
    {"id": 46, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "The adjustable armrests are a godsend."},
    {"id": 47, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Feels like a high-end chair but without the hefty price tag."},
    {"id": 48, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Rollers are smooth and don't scratch the floor."},
    {"id": 49, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "The reclining feature is smooth and holds well."},
    {"id": 50, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Perfect for both office and gaming needs."},
    {"id": 51, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Height adjustment is fluid and stays in place."},
    {"id": 52, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "The cushioning is just right - not too soft or too firm."},
    {"id": 53, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Customer service was helpful with inquiries."},
    {"id": 54, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Fits well in both professional and casual room settings."},
    {"id": 55, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "The headrest provides adequate neck support."},
    {"id": 56, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Maintains good posture even after extended use."},
    {"id": 57, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "The lumbar support is adjustable and supportive."},
    {"id": 58, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Easy to clean and maintain."},
    {"id": 59, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "Quality far surpasses the price."},
    {"id": 60, "category": "Furniture", "product_name": "Ergonomic Chair", "review": "A great investment for anyone spending hours seated."},
]


#메모리에만 저장되는 DB생성
engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

# create product reviews SQL table
table_name = "product_reviews"
city_stats_table = Table(
    table_name,
    metadata_obj,
    Column("id", Integer(), primary_key=True),
    Column("category", String(16), primary_key=True),
    Column("product_name", Integer),
    Column("review", String(16), nullable=False)
)
metadata_obj.create_all(engine)

sql_database = SQLDatabase(engine, include_tables=["product_reviews"])

for row in rows:
    stmt = insert(city_stats_table).values(**row)
    with engine.connect() as connection:
        cursor = connection.execute(stmt)
        connection.commit()


#llm모델 select
openai.api_key = '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'

llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
#쿼리변환 모델에 들어갈 디폴트 값
service_context = ServiceContext.from_defaults(llm=llm)



#RAG이용 질문분해
def generate_questions(user_query: str) -> List[str]:
  system_message = '''
  You are given with Postgres table with the following columns.

  city_name, population, country, reviews.

  Your task is to decompose the given question into the following two questions.

  1. Question in natural language that needs to be asked to retrieve results from the table.
  2. Question that needs to be asked on the top of the result from the first question to provide the final answer.

  Example:

  Input:
  How is the culture of countries whose population is more than 5000000

  Output:
  1. Get the reviews of countries whose population is more than 5000000
  2. Provide the culture of countries
  '''

  messages = [
      ChatMessage(role="system", content=system_message),
      ChatMessage(role="user", content=user_query),
  ]
  generated_questions = llm.chat(messages).message.content.split('\n')

  return generated_questions

#유저 쿼리 예시
user_query = "Get the summary of reviews of Iphone13"

#질문나누기(기본쿼리용,심화질문용)
text_to_sql_query, rag_query = generate_questions(user_query)

#보여주기
display(HTML(f'<p style="font-size:20px">{text_to_sql_query, rag_query}</p>'))



#txt2sql 하기위한 환경설정
sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["product_reviews"],
    synthesize_response=False,
    service_context=service_context
)

#자연어 쿼리변환
sql_response = sql_query_engine.query(text_to_sql_query) #
sql_response_list = ast.literal_eval(sql_response.response)
text = [' '.join(t) for t in sql_response_list]
text = ' '.join(text)
display(HTML(f'<p style="font-size:20px">{sql_response.metadata["sql_query"]}</p>'))

#2차 질문을 위한 ListIndex설정(rag_query)
listindex = ListIndex([Document(text=text)]) #
list_query_engine = listindex.as_query_engine()

summary = list_query_engine.query(rag_query)

display(HTML(f'<p style="font-size:20px">{summary.response}</p>'))

"""Function to perform SQL+RAG"""

def sql_rag(user_query: str) -> str:
  text_to_sql_query, rag_query = generate_questions(user_query)

  sql_response = sql_query_engine.query(text_to_sql_query)

  sql_response_list = ast.literal_eval(sql_response.response)

  text = [' '.join(t) for t in sql_response_list]
  text = ' '.join(text)

  listindex = ListIndex([Document(text=text)])
  list_query_engine = listindex.as_query_engine()

  summary = list_query_engine.query(rag_query)

  return summary.response



#main
sql_rag("How is the sentiment of SamsungTV product?")