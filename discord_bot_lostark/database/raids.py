import pymysql
from config import DB_CONFIG

# 레이드 등록 (중복 검사 + 메시지 ID 저장)
def insert_raid(server_id, title, creator_id, scheduled_time, message_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            check_sql = """
                SELECT COUNT(*) FROM raids
                WHERE ServerId = %s AND Title = %s AND ScheduledTime = %s AND DeletedAt IS NULL
            """
            cursor.execute(check_sql, (server_id, title, scheduled_time))
            if cursor.fetchone()[0] > 0:
                raise ValueError("이미 동일한 시간에 같은 보스가 등록되어 있습니다.")
            insert_sql = """
                INSERT INTO raids (ServerId, Title, ScheduledTime, CreatorId, MessageId)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (server_id, title, scheduled_time, creator_id, message_id))
        conn.commit()
    finally:
        conn.close()

# 최신 레이드 ID 조회
def get_latest_raid(server_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT Id FROM raids
                WHERE ServerId = %s AND DeletedAt IS NULL
                ORDER BY CreatedAt DESC LIMIT 1
            """
            cursor.execute(sql, (server_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        conn.close()

# 메시지 ID로 레이드 ID 조회
def get_raid_id_by_message_id(message_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT Id FROM raids WHERE MessageId = %s AND DeletedAt IS NULL"
            cursor.execute(sql, (message_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        conn.close()

# 오늘의 레이드 목록 조회
def get_raid_list(server_id, start, end):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT Id, Title, ScheduledTime FROM raids
                WHERE ServerId = %s AND DeletedAt IS NULL AND ScheduledTime BETWEEN %s AND %s
                ORDER BY ScheduledTime ASC
            """
            cursor.execute(sql, (server_id, start, end))
            return cursor.fetchall()
    finally:
        conn.close()

# 참가자 등록
def add_participant(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            check_sql = "SELECT Id FROM raidparticipants WHERE RaidId = %s AND UserId = %s"
            cursor.execute(check_sql, (raid_id, user_id))
            result = cursor.fetchone()
            if result:
                undelete_sql = "UPDATE raidparticipants SET DeletedAt = NULL WHERE Id = %s"
                cursor.execute(undelete_sql, (result[0],))
            else:
                insert_sql = "INSERT INTO raidparticipants (RaidId, UserId) VALUES (%s, %s)"
                cursor.execute(insert_sql, (raid_id, user_id))
        conn.commit()
    finally:
        conn.close()

# 참가자 취소
def remove_participant(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            delete_sql = """
                UPDATE raidparticipants
                SET DeletedAt = NOW()
                WHERE RaidId = %s AND UserId = %s AND DeletedAt IS NULL
            """
            cursor.execute(delete_sql, (raid_id, user_id))
        conn.commit()
    finally:
        conn.close()

# 레이드 삭제
def delete_raid(raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE raids SET DeletedAt = NOW() WHERE Id = %s AND DeletedAt IS NULL"
            cursor.execute(sql, (raid_id,))
        conn.commit()
    finally:
        conn.close()

# 레이드 시간 수정
def update_raid_time(raid_id, new_time):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE raids SET ScheduledTime = %s WHERE Id = %s AND DeletedAt IS NULL"
            cursor.execute(sql, (new_time, raid_id))
        conn.commit()
    finally:
        conn.close()

# 상세 조회
def get_raid_info_with_participants(raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql_raid = "SELECT Title, ScheduledTime FROM raids WHERE Id = %s AND DeletedAt IS NULL"
            cursor.execute(sql_raid, (raid_id,))
            raid = cursor.fetchone()
            if not raid:
                raise ValueError("해당 레이드를 찾을 수 없습니다.")
            sql_participants = "SELECT UserId FROM raidparticipants WHERE RaidId = %s AND DeletedAt IS NULL"
            cursor.execute(sql_participants, (raid_id,))
            participants = [row[0] for row in cursor.fetchall()]
            return raid[0], raid[1], participants
    finally:
        conn.close()
