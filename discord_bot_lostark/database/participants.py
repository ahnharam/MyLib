import pymysql
from config import DB_CONFIG

# 이미 참가했는지 확인 (중복 방지용)
def is_already_joined(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM RaidParticipants WHERE RaidId=%s AND UserId=%s"
            cursor.execute(sql, (raid_id, user_id))
            return cursor.fetchone()[0] > 0
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
