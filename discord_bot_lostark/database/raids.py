import pymysql
from config import DB_CONFIG
from database.participants import copy_participants  # 꼭 추가해야 함

# 레이드 등록 함수 (보스명 + 시간 중복 등록 방지)
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

# 가장 최신 레이드 ID 조회
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

# 모든 레이드 목록 + 참가자 수 조회
def get_all_raids_with_count(server_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT R.Id, R.Title, R.ScheduledTime, COUNT(P.Id) AS ParticipantCount "
                "FROM raids R "
                "LEFT JOIN raidparticipants P ON R.Id = P.RaidId AND P.DeletedAt IS NULL "
                "WHERE R.ServerId = %s "
                "AND R.DeletedAt IS NULL "
                "AND R.ScheduledTime > NOW() "
                "GROUP BY R.Id "
                "ORDER BY R.CreatedAt DESC"
            )
            cursor.execute(sql, (server_id,))
            return cursor.fetchall()
    finally:
        conn.close()


# 보스명으로 가장 최근 레이드 + 참가자 리스트 조회
def get_raid_with_participants_by_title(server_id, title):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql_raid = """
                SELECT Id, Title, ScheduledTime
                FROM raids
                WHERE ServerId = %s AND Title = %s AND DeletedAt IS NULL
                ORDER BY CreatedAt DESC
                LIMIT 1
            """
            cursor.execute(sql_raid, (server_id, title))
            raid = cursor.fetchone()
            if not raid:
                return None, []
            raid_id, title, time = raid

            sql_participants = """
                SELECT UserId FROM raidparticipants
                WHERE RaidId = %s AND DeletedAt IS NULL
            """
            cursor.execute(sql_participants, (raid_id,))
            participants = cursor.fetchall()
            return (raid_id, title, time), [row[0] for row in participants]
    finally:
        conn.close()

# 보스명 + 시간으로 특정 레이드 조회
def get_raid_by_title_and_time(server_id, title, hour, minute):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT Id, CreatorId
                FROM raids
                WHERE ServerId = %s AND Title = %s
                AND HOUR(ScheduledTime) = %s
                AND MINUTE(ScheduledTime) = %s
                AND DeletedAt IS NULL
                ORDER BY CreatedAt DESC
                LIMIT 1
            """
            cursor.execute(sql, (server_id, title, hour, minute))
            return cursor.fetchone()
    finally:
        conn.close()

# 보스명 기준 최근 레이드 ID + 작성자 조회
def get_raid_with_creator_by_title(server_id, title):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT Id, CreatorId
                FROM raids
                WHERE ServerId = %s AND Title = %s
                AND HOUR(ScheduledTime) = %s
                AND MINUTE(ScheduledTime) = %s
                AND DeletedAt IS NULL
                ORDER BY CreatedAt DESC
                LIMIT 1
            """
            cursor.execute(sql, (server_id, title))
            return cursor.fetchone()
    finally:
        conn.close()

# 레이드 및 관련 참가자 Soft Delete
def delete_raid(raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE raids SET DeletedAt = NOW() WHERE Id = %s", (raid_id,))
            cursor.execute("UPDATE raidparticipants SET DeletedAt = NOW() WHERE RaidId = %s", (raid_id,))
        conn.commit()
    finally:
        conn.close()

# 미래 레이드 목록 조회 (알림 재등록용)
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

# 레이드 시간 수정 함수 (참가자 복사 포함)
def recreate_raid_with_new_time(old_raid_id, new_time):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # 1. 기존 레이드 데이터 조회
            sql_select = "SELECT ServerId, Title, CreatorId FROM raids WHERE Id = %s"
            cursor.execute(sql_select, (old_raid_id,))
            result = cursor.fetchone()
            if not result:
                raise ValueError("기존 레이드를 찾을 수 없습니다.")

            server_id, title, creator_id = result

            # 2. 기존 레이드 Soft Delete 처리
            sql_delete = "UPDATE raids SET DeletedAt = NOW() WHERE Id = %s"
            cursor.execute(sql_delete, (old_raid_id,))

            # 3. 새 레이드 INSERT
            sql_insert = """
                INSERT INTO raids (ServerId, Title, ScheduledTime, CreatorId)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (server_id, title, new_time, creator_id))

            # 4. 새 레이드 ID 획득
            new_raid_id = cursor.lastrowid

            # 5. 기존 참가자 복사
            copy_sql = """
                INSERT INTO raidparticipants (RaidId, UserId)
                SELECT %s, UserId
                FROM raidparticipants
                WHERE RaidId = %s AND DeletedAt IS NULL
            """
            cursor.execute(copy_sql, (new_raid_id, old_raid_id))

        conn.commit()
        return new_raid_id

    finally:
        conn.close()

# ✅ 메시지 ID로 레이드 ID 조회 (버튼 클릭 시 사용)
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

# ✅ 참가자 등록 (중복 방지 + Soft Delete 복구)
def add_participant(raid_id, user_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # Soft-deleted 기록이 있는지 확인
            check_sql = """
                SELECT Id FROM raidparticipants
                WHERE RaidId = %s AND UserId = %s
            """
            cursor.execute(check_sql, (raid_id, user_id))
            result = cursor.fetchone()

            if result:
                # 기존 Soft-Delete 참가 복구
                undelete_sql = """
                    UPDATE raidparticipants
                    SET DeletedAt = NULL
                    WHERE Id = %s
                """
                cursor.execute(undelete_sql, (result[0],))
            else:
                # 신규 참가 등록
                insert_sql = """
                    INSERT INTO raidparticipants (RaidId, UserId)
                    VALUES (%s, %s)
                """
                cursor.execute(insert_sql, (raid_id, user_id))

        conn.commit()
    finally:
        conn.close()

# ✅ 참가자 취소 (Soft Delete)
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

# ✅ 레이드 정보 + 참가자 목록 조회
def get_raid_info_with_participants(raid_id):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # 레이드 기본 정보
            sql_raid = """
                SELECT Title, ScheduledTime FROM raids
                WHERE Id = %s AND DeletedAt IS NULL
            """
            cursor.execute(sql_raid, (raid_id,))
            raid = cursor.fetchone()
            if not raid:
                raise ValueError("해당 레이드를 찾을 수 없습니다.")
            title, time = raid

            # 참가자 목록
            sql_participants = """
                SELECT UserId FROM raidparticipants
                WHERE RaidId = %s AND DeletedAt IS NULL
            """
            cursor.execute(sql_participants, (raid_id,))
            participants = [row[0] for row in cursor.fetchall()]

            return title, time, participants
    finally:
        conn.close()
