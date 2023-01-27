# -*- coding: utf-8 -*-

import sqlite3


class XfcDB:
    def __init__(self):
        self.database_name = './dbms/xfc_policy.db'

    def create_api_policy_table(self):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'CREATE TABLE IF NOT EXISTS api_policy(id TEXT, remark TEXT, createTime TEXT, updateTime TEXT, ' +
            'platform TEXT, providerName TEXT, process TEXT, ipAddr TEXT, macAddr TEXT, modifiedDate INT, ' +
            'domainKeyId TEXT, domainAlgorithm TEXT, domainKeyLength INT, modulus BIGINT, publicExponent INT, ' +
            'privateExponent BIGINT, domainCode TEXT, attributeKeyId TEXT, attributeIv TEXT, attributeAlgorithm TEXT, ' +
            'attributeKeyLength INT, attributeChiperMode TEXT, attributePaddingMethod TEXT, attributeKeyMaterial TEXT, ' +
            'contentsAlgorithm TEXT, contentsKeyLength INT, readChk TEXT, writeChk TEXT, excuteChk TEXT, syncPeriod INT, ' +
            'logPeriod INT, excludeExts TEXT, decFileSize INT, encErrorCode TEXT, decErrorCode TEXT ' +
            ')')
        conn.close()

    def delete_api_policy(self, ipaddr: str):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'delete from api_policy where id = ' + '\'' + ipaddr + '\';')
        conn.close()

    def insert_api_policy(self, c):
        conn = sqlite3.connect(self.database_name)
        conn.execute(
            'INSERT INTO api_policy VALUES(' + c.id + ',' + c.remark + ',' + c.createTime + ',' + c.updateTime + ',' +
            c.platform + ',' + c.providerName + ',' + c.process + ',' + c.ipAddr + ',' + c.macAddr + ',' +
            c.modifiedDate + ',' + c.domainKeyId + ',' + c.domainAlgorithm + ',' + c.domainKeyLength + ',' +
            c.modulus + ',' + c.publicExponent + ',' + c.privateExponent + ',' + c.domainCode + ',' +
            c.attributeKeyId + ',' + c.attributeIv + ',' + c.attributeAlgorithm + ',' + c.attributeKeyLength + ',' +
            c.attributeChiperMode + ',' + c.attributePaddingMethod + ',' + c.attributeKeyMaterial + ',' +
            c.contentsAlgorithm + ',' + c.contentsKeyLength + ',' + c.readChk + ',' + c.writeChk + ',' +
            c.excuteChk + ',' + c.syncPeriod + ',' + c.logPeriod + ',' + c.excludeExts + ',' + c.decFileSize + ',' +
            c.encErrorCode + ',' + c.decErrorCode + ')')
        conn.close()
