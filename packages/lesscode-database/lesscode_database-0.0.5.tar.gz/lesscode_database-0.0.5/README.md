# lesscode_database

数据库连接工具包

示例代码

```python
import asyncio

from sqlalchemy import select, Column, VARCHAR, INTEGER, Table, MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker

from lesscode_database.connection_info import ConnectionInfo
from lesscode_database.db_options import db_options

db_options.conn_list = [
    ConnectionInfo(dialect="mysql", name="mysql", host="127.0.0.1", port=3306, user="root",
                   password="root", db_name="test", enable=False, params={"pool_recycle": 3600},
                   async_enable=True),
    ConnectionInfo(dialect="doris", name="doris", host="127.0.0.1", port=9030, user="root",
                   password="root", db_name="test", enable=False, params={"pool_recycle": 3600},
                   async_enable=True),
    ConnectionInfo(dialect="ocean_base", name="ocean_base", host="127.0.0.1", port=2883, user="root",
                   password="root", db_name="test", enable=False, params={"pool_recycle": 3600},
                   async_enable=True),
    ConnectionInfo(dialect="tidb", name="tidb", host="127.0.0.1", port=4000, user="root",
                   password="root", db_name="test", enable=False, params={"pool_recycle": 3600},
                   async_enable=True),
    ConnectionInfo(dialect="mssql", name="mssql", host="127.0.0.1", port=1433, user="root",
                   password="root", db_name="test", enable=False, async_enable=False),
    ConnectionInfo(dialect="oracle", name="oracle", host="127.0.0.1", port=1521, user="root",
                   password="root", db_name="test", enable=False, async_enable=False),
    ConnectionInfo(dialect="sqlite3", name="sqlite3", dsn="/test/test.db", async_enable=False),
    ConnectionInfo(dialect="elasticsearch", name="es", host="127.0.0.1", port=9210, user="root",
                   password="root", enable=False, async_enable=True),
    ConnectionInfo(dialect="mongo", name="mongo", host="127.0.0.1", port=27027, user="root",
                   password="root", enable=False, async_enable=True),
    ConnectionInfo(dialect="nebula", name="nebula", host="127.0.0.1", port=9669, user="root",
                   password="nebula", db_name="nebula", enable=False),
    ConnectionInfo(dialect="postgresql", host="127.0.0.1", port=5454, user="root", password="root",
                   db_name="root", enable=False, async_enable=True),
    ConnectionInfo(dialect="redis", name="redis", host="127.0.0.1", port=6379, user=None,
                   password=None, db_name=1, enable=False, async_enable=True),
    # sqlalchemy 异步支持mysql，postgresql，tidb，ocean_base，doris;
    # 同步支持mysql，postgresql，tidb，ocean_base，doris，sqlite3，mssql，oracle
    ConnectionInfo(dialect="sqlalchemy", name="sqlalchemy", host="127.0.0.1", port=3306, user="root",
                   password="root", db_name="test", enable=False, async_enable=False, params={"db_type": "mysql"}),
    ConnectionInfo(dialect="neo4j", name="neo4j", host="127.0.0.1", port=7687, user="neo4j",
                   password="neo4j", db_name=None, enable=False, async_enable=True),
    ConnectionInfo(dialect="clickhouse", name="clickhouse", dsn="clickhouse://localhost", host="127.0.0.1", port=9000,
                   user="default", password="", db_name='', enable=True, async_enable=False),

]

# mysql 同步测试，async_enable=False
with db_options.mysql.dedicated_connection() as conn:
    conn.ping(reconnect=True)
    with conn.cursor() as cursor:
        cursor.execute("select 1")
        description = cursor.description
        rs = cursor.fetchone()
        print(rs)


# mysql 异步测试，async_enable=True
async def async_mysql_test():
    async with db_options.mysql.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("select 1")
            rs = await cursor.fetchone()
            print(rs)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_mysql_test())

# doris 同步测试，async_enable=False
with db_options.doris.dedicated_connection() as conn:
    conn.ping(reconnect=True)
    with conn.cursor() as cursor:
        cursor.execute("select 1")
        description = cursor.description
        rs = cursor.fetchone()
        print(rs)


# doris 异步测试，async_enable=True
async def async_doris_test():
    async with db_options.doris.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("select 1")
            rs = await cursor.fetchone()
            print(rs)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_doris_test())

# ocean_base 同步测试，async_enable=False
with db_options.ocean_base.dedicated_connection() as conn:
    conn.ping(reconnect=True)
    with conn.cursor() as cursor:
        cursor.execute("select 1")
        description = cursor.description
        rs = cursor.fetchone()
        print(rs)


# ocean_base 异步测试，async_enable=True
async def async_ocean_base_test():
    async with db_options.ocean_base.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("select 1")
            rs = await cursor.fetchone()
            print(rs)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_ocean_base_test())

# tidb 同步测试，async_enable=False
with db_options.tidb.dedicated_connection() as conn:
    conn.ping(reconnect=True)
    with conn.cursor() as cursor:
        cursor.execute("select 1")
        description = cursor.description
        rs = cursor.fetchone()
        print(rs)


# tidb 异步测试，async_enable=True
async def async_tidb_test():
    async with db_options.tidb.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("select 1")
            rs = await cursor.fetchone()
            print(rs)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_tidb_test())


# sqlite3 异步测试
async def async_sqlite3_test():
    cur = await db_options.sqlite3.cursor()
    await cur.execute("SELECT 1")
    row = await cur.fetchone()
    print(row)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_sqlite3_test())

# sqlite3 同步测试
cursor = db_options.sqlite3.cursor()
cursor.execute('select 1')
row = cursor.fetchone()
print(row)

# es同步测试，async_enable=False
body = {
    "query": {
        "bool": {
            "must": []
        }
    },
    "size": 1
}
resp = db_options.es.search(
    index="test",
    body=body
)
print(resp)


# es异步测试，async_enable=True
async def async_es_test():
    resp = await db_options.es.search(
        index="test",
        body={"query": {"match_all": {}}},
        size=1,
    )
    print(resp)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_es_test())

# sql server同步测试
cursor = db_options.mssql.cursor()
cursor.execute('SELECT 1')
row = cursor.fetchone()
print(row)

# sql server暂不支持异步测试

# oracle 同步测试
cursor = db_options.oracle.cursor()
cursor.execute('select 1')
row = cursor.fetchone()
print(row)

# oracle暂不支持异步测试


# mongo同步测试，async_enable=False
print(db_options.mongo.test.test.find_one())


# mongo异步测试，async_enable=True
async def async_mongo_test():
    resp = await db_options.mongo.test.test.find_one()
    print(resp)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_mongo_test())

# nebula同步测试，async_enable=False
with db_options.nebula.session_context("root", "nebula") as session:
    session.execute(f'USE test')
    result = session.execute("match (t:Test) return t limit 1")
    print(result)

# nebula暂不支持异步

# postgresql同步测试，async_enable=False
with db_options.postgresql.connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("select 1")
        rs = cursor.fetchone()
        print(rs)


# postgresql异步测试，async_enable=True
async def async_pg_test():
    async with db_options.postgresql.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select 1")
            rs = await cur.fetchone()
            print(rs)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_pg_test())

# redis 同步测试，async_enable=False
print(db_options.redis.exists("test"))


# redis 异步测试，async_enable=True
async def async_redis_test():
    rs = await db_options.redis.exists("test")
    print(rs)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_redis_test())

# sqlalchemy table
meta = MetaData()
t1 = Table("test_user", meta, Column("name", VARCHAR(collation='utf8mb3_bin', length=255)),
           Column(name='id', comment=None, nullable=False, autoincrement=False, primary_key=True, type_=INTEGER(),
                  server_default=None))

# sqlalchemy同步测试，async_enable=False
with sessionmaker(bind=db_options.sqlalchemy)() as session:
    cur = session.execute(select(t1))
    print(cur.fetchall())


# sqlalchemy异步测试，async_enable=True
async def async_sqlalchemy_test():
    async with async_sessionmaker(db_options.sqlalchemy)() as session:
        cur = await session.execute(select(t1))

        print(cur.fetchall())


loop = asyncio.get_event_loop()
loop.run_until_complete(async_sqlalchemy_test())


# neo4j同步测试
def query(tx):
    nql = "MATCH (c:Company) return c limit 1"
    for record in tx.run(nql):
        print(record)


with db_options.neo4j.session(database="invest") as session:
    session.execute_read(query)


# neo4j异步测试
async def query(tx):
    nql = "MATCH (c:Company) return c limit 1"
    res = await tx.run(nql)
    async for record in res:
        print(record)


async def async_neo4j_test():
    async with db_options.neo4j.session(database="invest") as session:
        await session.execute_read(query)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_neo4j_test())

# clickhouse 同步测试
with db_options.clickhouse as conn:
    with conn.cursor() as cursor:
        cursor.execute('SELECT 1')
        print(cursor.fetchall())


# clickhouse 异步测试测试
async def async_clickhouse_test():
    async with db_options.clickhouse.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1")
            ret = await cursor.fetchone()
            print(ret)


loop = asyncio.get_event_loop()
loop.run_until_complete(async_clickhouse_test())


```
