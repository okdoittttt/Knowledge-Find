import psycopg2

from db_config import POSTGRES_DB

class DBManager:
    '''
    데이터베이스를 관리하기 위한 클래스
    '''
    def __init__(self):
        pass

    
    def create_table(self):
        '''
        테이블이 없으면 생성
        '''
        try:
            with psycopg2.connect(**POSTGRES_DB) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS public.uploaded_files (
                            id SERIAL PRIMARY KEY,
                            filename VARCHAR(255) NOT NULL,
                            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    conn.commit()
                    print("테이블이 성공적으로 생성되었거나 이미 존재합니다.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"PostgreSQL 테이블 생성 오류: {error}")

