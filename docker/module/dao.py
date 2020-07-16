import log

log = log.logging.getLogger(__name__)


class Database(object):
    def __init__(self, conn):
        self.conn = conn
    def queryTransmit(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * from transmit_record;")
            data = cursor.fetchall()
            return data
        except Exception as e:
            raise e
    
    def insertTransmit(self,dataForRakuten):
        cursor = self.conn.cursor()
        try:
            for record in dataForRakuten['data']:
                sql = "INSERT INTO db.transmit_record (session_id, transmit_date, transmit_status) \
    	  	            VALUES ( %s, CURDATE(), %s)ON DUPLICATE KEY UPDATE transmit_date=CURDATE(), transmit_status= %s ;"
                val = (record['session_id'], str(record['transmit_status']), str(record['transmit_status']))

                try:
                    cursor.execute(sql, val)
                except Exception as e:
                    log.info("query '{}' with params {} failed with {}".format(sql, val, e))
                    log.info( "\n executed sql: " + cursor._executed)
                    self.conn.rollback()
                # if cursor.rowcount != 1:
                log.info("insert success: " + record['session_id'])
                self.conn.commit()
        except Exception as e:
            raise str(e) 