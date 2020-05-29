import sqlite3

#conn = sqlite3.connect(":memory:")
conn = sqlite3.connect('db_file.db')
cursor = conn.cursor()

def drop_table():
	cursor.execute("drop table Hypotheekrentetarieven")
	conn.commit()

def create_table():
	cursor.execute(r"""CREATE TABLE IF NOT EXISTS Hypotheekrentetarieven(
	   ID INTEGER PRIMARY KEY,
	   Hypotheekverstrekker TEXT NOT NULL,
	   Looptijd INT NOT NULL,
	   NHG FLOAT,
	   LTV60 FLOAT,
	   LTV80 FLOAT,
	   LTV90 FLOAT,
	   LTV100 FLOAT,
	   Pijlmaand DATE,
	   Modified_Timestamp DATETIME)""")
	conn.commit()

def insert_values(Hypotheekverstrekker, looptijd, nhg, ltv60, ltv80, ltv90, ltv100):
	cursor.execute(f"""
	INSERT INTO Hypotheekrentetarieven
	(Hypotheekverstrekker
	, Looptijd
	, NHG
	, LTV60
	, LTV80
	, LTV90
	, LTV100
	, Pijlmaand
	, Modified_Timestamp) 
	VALUES(
	 '{Hypotheekverstrekker}'
	, '{looptijd}'
	, '{nhg}'
	, '{ltv60}'
	, '{ltv80}'
	, '{ltv90}'
	, '{ltv100}'
	, date('now', 'start of month', 'localtime')
	, datetime('now', 'localtime'))
	""")
	conn.commit()

def delete_duplicate_records():
	cursor.execute("""DELETE FROM Hypotheekrentetarieven
		WHERE ID IN (
	SELECT ID FROM 
		(
		SELECT 
			ID 
			, ROW_NUMBER() OVER(
				PARTITION BY 
				Hypotheekverstrekker 
				, looptijd
				, NHG
				, LTV60
				, LTV80
				, LTV90
				, LTV100
				, Pijlmaand
				ORDER BY 
				Hypotheekverstrekker 
				, looptijd
				, NHG
				, LTV60
				, LTV80
				, LTV90
				, LTV100
				, Pijlmaand
				, Modified_Timestamp desc) as row_num
		FROM 
			Hypotheekrentetarieven
		)
		where row_num > 1)""")
	conn.commit()

delete_duplicate_records()
