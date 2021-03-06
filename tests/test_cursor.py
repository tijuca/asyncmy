import pytest

from asyncmy.cursors import DictCursor


@pytest.mark.asyncio
async def test_fetchone(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT 1")
        ret = cursor.fetchone()
        assert ret == (1,)


@pytest.mark.asyncio
async def test_fetchall(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT 1")
        ret = cursor.fetchall()
        assert ret == ((1,),)


@pytest.mark.asyncio
async def test_dict_cursor(connection):
    async with connection.cursor(cursor=DictCursor) as cursor:
        await cursor.execute("SELECT 1")
        ret = cursor.fetchall()
        assert ret == [{"1": 1}]


@pytest.mark.asyncio
async def test_insert(connection):
    async with connection.cursor(cursor=DictCursor) as cursor:
        rows = await cursor.execute(
            """INSERT INTO test.asyncmy(`decimal`, date, datetime, `float`, string, `tinyint`) VALUES (%s,%s,%s,%s,%s,%s)""",
            (
                1,
                "2020-08-08",
                "2020-08-08 00:00:00",
                1,
                "1",
                1,
            ),
        )
        assert rows == 1


@pytest.mark.asyncio
async def test_executemany(connection):
    async with connection.cursor(cursor=DictCursor) as cursor:
        rows = await cursor.executemany(
            """INSERT INTO test.asyncmy(`decimal`, date, datetime, `float`, string, `tinyint`) VALUES (%s,%s,%s,%s,%s,%s)""",
            [
                (
                    1,
                    "2020-08-08",
                    "2020-08-08 00:00:00",
                    1,
                    "1",
                    1,
                ),
                (
                    1,
                    "2020-08-08",
                    "2020-08-08 00:00:00",
                    1,
                    "1",
                    1,
                ),
            ],
        )
        assert rows == 2


@pytest.mark.asyncio
async def test_table_ddl(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("drop table if exists test.alter_table")
        create_table_sql = """
            CREATE TABLE test.alter_table
(
    `id` int primary key auto_increment
)
            """
        await cursor.execute(create_table_sql)
        add_column_sql = "alter table test.alter_table add column c varchar(20)"
        await cursor.execute(add_column_sql)
        show_table_sql = "show create table test.alter_table"
        await cursor.execute(show_table_sql)
        assert cursor.fetchone() == (
            "alter_table",
            "CREATE TABLE `alter_table` (\n  `id` int NOT NULL AUTO_INCREMENT,\n  `c` varchar(20) DEFAULT NULL,\n  PRIMARY KEY (`id`)\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci",
        )
        await cursor.execute("drop table test.alter_table")
