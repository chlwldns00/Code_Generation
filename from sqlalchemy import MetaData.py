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
import openai
from IPython.display import display, HTML

rows = [
    # iPhone13 Reviews
    {"category": "Phone", "product_name": "Iphone13", "review": "The iPhone13 is a stellar leap forward. From its sleek design to the crystal-clear display, it screams luxury and functionality. Coupled with the enhanced battery life and an A15 chip, it's clear Apple has once again raised the bar in the smartphone industry."},
    {"category": "Phone", "product_name": "Iphone13", "review": "This model brings the brilliance of the ProMotion display, changing the dynamics of screen interaction. The rich colors, smooth transitions, and lag-free experience make daily tasks and gaming absolutely delightful."},
    {"category": "Phone", "product_name": "Iphone13", "review": "The 5G capabilities are the true game-changer. Streaming, downloading, or even regular browsing feels like a breeze. It's remarkable how seamless the integration feels, and it's obvious that Apple has invested a lot in refining the experience."},

    # SamsungTV Reviews
    {"category": "TV", "product_name": "SamsungTV", "review": "Samsung's display technology has always been at the forefront, but with this TV, they've outdone themselves. Every visual is crisp, the colors are vibrant, and the depth of the blacks is simply mesmerizing. The smart features only add to the luxurious viewing experience."},
    {"category": "TV", "product_name": "SamsungTV", "review": "This isn't just a TV; it's a centerpiece for the living room. The ultra-slim bezels and the sleek design make it a visual treat even when it's turned off. And when it's on, the 4K resolution delivers a cinematic experience right at home."},
    {"category": "TV", "product_name": "SamsungTV", "review": "The sound quality, often an oversight in many TVs, matches the visual prowess. It creates an enveloping atmosphere that's hard to get without an external sound system. Combined with its user-friendly interface, it's the TV I've always dreamt of."},

    # Ergonomic Chair Reviews
    {"category": "Furniture", "product_name": "Ergonomic Chair", "review": "Shifting to this ergonomic chair was a decision I wish I'd made earlier. Not only does it look sophisticated in its design, but the level of comfort is unparalleled. Long hours at the desk now feel less daunting, and my back is definitely grateful."},
    {"category": "Furniture", "product_name": "Ergonomic Chair", "review": "The meticulous craftsmanship of this chair is evident. Every component, from the armrests to the wheels, feels premium. The adjustability features mean I can tailor it to my needs, ensuring optimal posture and comfort throughout the day."},
    {"category": "Furniture", "product_name": "Ergonomic Chair", "review": "I was initially drawn to its aesthetic appeal, but the functional benefits have been profound. The breathable material ensures no discomfort even after prolonged use, and the robust build gives me confidence that it's a chair built to last."},
]

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