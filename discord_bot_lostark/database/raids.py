import pymysql
from config import DB_CONFIG
from database.participants import copy_participants

# ✅ 레이드 등록 함수 (중복 방지 + message_id 저장)
def insert_raid(server_id, title, creator_id, raid_time, message_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            check_sql = """
                SELECT COUNT(*) FROM raids
                WHERE ServerId = %s AND Title = %s AND ScheduledTime = %s AND DeletedAt IS NULL
            """
            cursor.execute(check_sql, (server_id, title, raid_time))
            if cursor.fetchone()[0] > 0:
                raise ValueError("이미 동일한 시간에 같은 보스가 등록되어 있습니다.")

            insert_sql = """
                INSERT INTO raids (ServerId, Title, ScheduledTime, CreatorId, MessageId)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (server_id, title, raid_time, creator_id, message_id))
        conn.commit()
    finally:
        conn.close()

# ✅ 가장 최신 레이드 ID 조회
def get_latest_raid(server_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT Id FROM raids
                WHERE ServerId = %s AND DeletedAt IS NULL
                ORDER BY CreatedAt DESC
                LIMIT 1
            """
            cursor.execute(sql, (server_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        conn.close()

# ✅ 미래 레이드 목록 조회 (알림 재등록용)
def get_future_raids(now):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT Id, ServerId, Title, ScheduledTime
                FROM raids
                WHERE ScheduledTime > %s AND DeletedAt IS NULL
                ORDER BY ScheduledTime ASC
            """
            cursor.execute(sql, (now,))
            return cursor.fetchall()
    finally:
        conn.close()

# ✅ 레이드 알림 메시지 ID 등록/업데이트
def update_message_id(raid_id, message_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE raids SET MessageId = %s WHERE Id = %s"
            cursor.execute(sql, (message_id, raid_id))
        conn.commit()
    finally:
        conn.close()

# ✅ 레이드 ID로 서버 ID, 제목, 시작 시간 조회 (알림용)
def get_raid_info_by_id(raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT ServerId, Title, ScheduledTime
                FROM raids
                WHERE Id = %s AND DeletedAt IS NULL
            """
            cursor.execute(sql, (raid_id,))
            return cursor.fetchone()
    finally:
        conn.close()

# ✅ 메시지 ID로 레이드 ID 조회 (버튼용)
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

# ✅ 레이드 삭제 (Soft Delete)
def delete_raid(raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE raids SET DeletedAt = NOW() WHERE Id = %s", (raid_id,))
            cursor.execute("UPDATE raidparticipants SET DeletedAt = NOW() WHERE RaidId = %s", (raid_id,))
        conn.commit()
    finally:
        conn.close()

# ✅ 레이드 시간 수정 (구버전, 덮어쓰기 방식)
def update_raid_time(raid_id, new_time):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE raids SET ScheduledTime = %s WHERE Id = %s AND DeletedAt IS NULL"
            cursor.execute(sql, (new_time, raid_id))
        conn.commit()
    finally:
        conn.close()

# ✅ 레이드 시간 수정 (신버전, 새 레코드 생성 + 참가자 복사)
def recreate_raid_with_new_time(old_raid_id, new_time):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ServerId, Title, CreatorId FROM raids WHERE Id = %s", (old_raid_id,))
            result = cursor.fetchone()
            if not result:
                raise ValueError("기존 레이드를 찾을 수 없습니다.")
            server_id, title, creator_id = result

            cursor.execute("UPDATE raids SET DeletedAt = NOW() WHERE Id = %s", (old_raid_id,))

            cursor.execute(
                """
                INSERT INTO raids (ServerId, Title, ScheduledTime, CreatorId)
                VALUES (%s, %s, %s, %s)
                """,
                (server_id, title, new_time, creator_id)
            )
            new_raid_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO raidparticipants (RaidId, UserId)
                SELECT %s, UserId FROM raidparticipants
                WHERE RaidId = %s AND DeletedAt IS NULL
                """,
                (new_raid_id, old_raid_id)
            )
        conn.commit()
        return new_raid_id
    finally:
        conn.close()

# ✅ 참가자 등록
def add_participant(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Id FROM raidparticipants WHERE RaidId = %s AND UserId = %s", (raid_id, user_id))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE raidparticipants SET DeletedAt = NULL WHERE Id = %s", (result[0],))
            else:
                cursor.execute("INSERT INTO raidparticipants (RaidId, UserId) VALUES (%s, %s)", (raid_id, user_id))
        conn.commit()
    finally:
        conn.close()

# ✅ 참가자 취소 (Soft Delete)
def remove_participant(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE raidparticipants
                SET DeletedAt = NOW()
                WHERE RaidId = %s AND UserId = %s AND DeletedAt IS NULL
                """,
                (raid_id, user_id)
            )
        conn.commit()
    finally:
        conn.close()

# ✅ 레이드 정보 + 참가자 목록 조회
def get_raid_info_with_participants(raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Title, ScheduledTime FROM raids WHERE Id = %s AND DeletedAt IS NULL", (raid_id,))
            raid = cursor.fetchone()
            if not raid:
                raise ValueError("해당 레이드를 찾을 수 없습니다.")
            title, time = raid

            cursor.execute("SELECT UserId FROM raidparticipants WHERE RaidId = %s AND DeletedAt IS NULL", (raid_id,))
            participants = [row[0] for row in cursor.fetchall()]
            return title, time, participants
    finally:
        conn.close()

# ✅ 오늘의 레이드 목록 조회 (슬래시 /목록 용)
def get_raid_list(server_id, start, end):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT Id, Title, ScheduledTime FROM raids
                WHERE ServerId = %s AND DeletedAt IS NULL AND ScheduledTime BETWEEN %s AND %s
                ORDER BY ScheduledTime ASC
                """,
                (server_id, start, end)
            )
            return cursor.fetchall()
    finally:
        conn.close()

def get_all_raids_with_count(server_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT R.Id, R.Title, R.ScheduledTime, COUNT(P.Id) AS ParticipantCount "
                "FROM raids R "
                "LEFT JOIN raidparticipants P ON R.Id = P.RaidId AND P.DeletedAt IS NULL "
                "WHERE R.ServerId = %s AND R.DeletedAt IS NULL AND R.ScheduledTime > NOW() "
                "GROUP BY R.Id ORDER BY R.CreatedAt DESC"
            )
            cursor.execute(sql, (server_id,))
            return cursor.fetchall()
    finally:
        conn.close()
