# -*- coding: utf-8 -*-

import sqlite3


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
            'attributeKeyLength TEXT, attributeChiperMode TEXT, attributePaddingMethod TEXT, attributeKeyMaterial TEXT, ' +
            'contentsAlgorithm TEXT, contentsKeyLength TEXT, readChk TEXT, writeChk TEXT, excuteChk TEXT, syncPeriod '
            'TEXT, ' +
            'logPeriod TEXT, excludeExts TEXT, decFileSize TEXT, encErrorCode TEXT, decErrorCode TEXT ' +
            ')')
        conn.close()

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
