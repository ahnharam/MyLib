import pymysql
from config import DB_CONFIG

# 이미 참가했는지 확인 (중복 방지용)
def is_already_joined(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT COUNT(*) FROM RaidParticipants
                WHERE RaidId = %s AND UserId = %s AND DeletedAt IS NULL
            """
            cursor.execute(sql, (raid_id, user_id))
            return cursor.fetchone()[0] > 0
    finally:
        conn.close()

# 참가 등록
def add_participant(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # 이전에 삭제된 참가자면 복구 처리
            restore_sql = """
                UPDATE RaidParticipants
                SET DeletedAt = NULL
                WHERE RaidId = %s AND UserId = %s AND DeletedAt IS NOT NULL
            """
            cursor.execute(restore_sql, (raid_id, user_id))
            if cursor.rowcount == 0:
                insert_sql = "INSERT INTO RaidParticipants (RaidId, UserId) VALUES (%s, %s)"
                cursor.execute(insert_sql, (raid_id, user_id))
        conn.commit()
    finally:
        conn.close()

# 레이드에 참가 등록
def join_raid(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO RaidParticipants (RaidId, UserId) VALUES (%s, %s)"
            cursor.execute(sql, (raid_id, user_id))
        conn.commit()
    finally:
        conn.close()

# 참가 취소 (레이드 ID, 유저 ID 기반 삭제)
def cancel_participation(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM RaidParticipants WHERE RaidId=%s AND UserId=%s"
            cursor.execute(sql, (raid_id, user_id))
        conn.commit()
    finally:
        conn.close()

# 참가 취소 (Soft Delete)
def remove_participant(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE RaidParticipants
                SET DeletedAt = NOW()
                WHERE RaidId = %s AND UserId = %s AND DeletedAt IS NULL
            """
            cursor.execute(sql, (raid_id, user_id))
        conn.commit()
    finally:
        conn.close()

def copy_participants(from_raid_id, to_raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO RaidParticipants (RaidId, UserId)
                SELECT %s, UserId
                FROM RaidParticipants
                WHERE RaidId = %s AND DeletedAt IS NULL
            """
            cursor.execute(sql, (to_raid_id, from_raid_id))
        conn.commit()
    finally:
        conn.close()
