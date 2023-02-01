# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd


class XfcDB:
    def __init__(self):
        self.database_name = './dbms/xfc_policy.db'

    def create_api_policy_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS api_policy(id TEXT, remark TEXT, createTime TEXT, updateTime TEXT, ' +
            'platform TEXT, providerName TEXT, process TEXT, ipAddr TEXT, macAddr TEXT, modifiedDate TEXT, ' +
            'domainKeyId TEXT, domainAlgorithm TEXT, domainKeyLength TEXT, modulus TEXT, publicExponent TEXT, ' +
            'privateExponent TEXT, domainCode TEXT, attributeKeyId TEXT, attributeIv TEXT, attributeAlgorithm TEXT, ' +
            'attributeKeyLength TEXT, attributeChiperMode TEXT, attributePaddingMethod TEXT, ' +
            'attributeKeyMaterial TEXT, contentsAlgorithm TEXT, contentsKeyLength TEXT, readChk TEXT, writeChk TEXT, ' +
            'excuteChk TEXT, syncPeriod TEXT, logPeriod TEXT, excludeExts TEXT, decFileSize TEXT, encErrorCode TEXT, ' +
            'decErrorCode TEXT )'
        )
        conn.close()

    def get_api_policy_list(self):
        query = \
            "select id, ipAddr, Remark, createTime, updateTime, platform, domainKeyId from api_policy order by id;"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    def get_api_policy(self, api, api_id):
        query = \
            "select * from api_policy where id = \'" + api_id + "\';"

        conn = sqlite3.connect(self.database_name)
        df = pd.read_sql_query(query, conn)
        conn.close()
        value_list = df.values.tolist()

        for v in value_list:
            api.id.value = v[0]
            api.remark.value = v[1]
            api.createTime.value = v[2]
            api.updateTime.value = v[3]
            api.platform.value = v[4]
            api.providerName.value = v[5]
            api.process.value = v[6]
            api.ipAddr.value = v[7]
            api.macAddr.value = v[8]
            api.modifiedDate.value = v[9]
            api.domainKeyId.value = v[10]
            api.domainAlgorithm.value = v[11]
            api.domainKeyLength.value = v[12]
            api.modulus.value = v[13]
            api.publicExponent.value = v[14]
            api.privateExponent.value = v[15]
            api.domainCode.value = v[16]
            api.attributeKeyId.value = v[17]
            api.attributeIv.value = v[18]
            api.attributeAlgorithm.value = v[19]
            api.attributeKeyLength.value = v[20]
            api.attributeChiperMode.value = v[21]
            api.attributePaddingMethod.value = v[22]
            api.attributeKeyMaterial.value = v[23]
            api.contentsAlgorithm.value = v[24]
            api.contentsKeyLength.value = v[25]
            api.readChk.value = v[26]
            api.writeChk.value = v[27]
            api.excuteChk.value = v[28]
            api.syncPeriod.value = v[29]
            api.logPeriod.value = v[30]
            api.excludeExts.value = v[31]
            api.decFileSize.value = v[32]
            api.encErrorCode.value = v[33]
            api.decErrorCode.value = v[34]
            break

    def delete_api_policy(self, ipaddr: str):
        conn = sqlite3.connect(self.database_name)
        conn.execute('delete from api_policy where id = ' + '\'' + ipaddr + '\';')
        conn.commit()
        conn.close()

    def insert_api_policy(self, c):
        self.delete_api_policy(c.id.value)

        conn = sqlite3.connect(self.database_name)
        conn.execute("INSERT INTO api_policy VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
                     (c.id.value,
                      c.remark.value,
                      c.createTime.value,
                      c.updateTime.value,
                      c.platform.value,
                      c.providerName.value,
                      c.process.value,
                      c.ipAddr.value,
                      c.macAddr.value,
                      str(c.modifiedDate.value),
                      c.domainKeyId.value,
                      c.domainAlgorithm.value,
                      str(c.domainKeyLength.value),
                      str(c.modulus.value),
                      str(c.publicExponent.value),
                      str(c.privateExponent.value),
                      c.domainCode.value,
                      c.attributeKeyId.value,
                      c.attributeIv.value,
                      c.attributeAlgorithm.value,
                      str(c.attributeKeyLength.value),
                      c.attributeChiperMode.value,
                      c.attributePaddingMethod.value,
                      c.attributeKeyMaterial.value,
                      c.contentsAlgorithm.value,
                      str(c.contentsKeyLength.value),
                      c.readChk.value,
                      c.writeChk.value,
                      c.excuteChk.value,
                      str(c.syncPeriod.value),
                      str(c.logPeriod.value),
                      c.excludeExts.value,
                      str(c.decFileSize.value),
                      c.encErrorCode.value,
                      c.decErrorCode.value)
                     )
        conn.commit()
        conn.close()
