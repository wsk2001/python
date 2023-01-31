# -*- coding: utf-8 -*-

import flet as ft
import json
from datetime import datetime

class XfcApi:
    def __init__(self):
        self.id = ft.TextField(label="ID")
        self.remark = ft.TextField(label="Remark")
        self.createTime = ft.TextField(label="Create Time")
        self.updateTime = ft.TextField(label="Update Time")

        self.platform = ft.TextField(label="platform")
        self.providerName = ft.TextField(label="provider Name")
        self.process = ft.TextField(label="process")
        self.ipAddr = ft.TextField(label="ip Address")
        self.macAddr = ft.TextField(label="MAC Address")
        self.modifiedDate = ft.TextField(label="수정 일자")
        self.domainKeyId = ft.TextField(label="도메인 Key Id")
        self.domainAlgorithm = ft.TextField(label="도메인 암호화 Algorithm")
        self.domainKeyLength = ft.TextField(label="도메인 키 길이")
        self.modulus = ft.TextField(label="modulus")
        self.publicExponent = ft.TextField(label="publicExponent")
        self.privateExponent = ft.TextField(label="privateExponent")
        self.domainCode = ft.TextField(label="도메인 코드")
        self.attributeKeyId = ft.TextField(label="attributeKeyId")
        self.attributeIv = ft.TextField(label="attributeIv")
        self.attributeAlgorithm = ft.TextField(label="attributeAlgorithm")
        self.attributeKeyLength = ft.TextField(label="attributeKeyLength")
        self.attributeChiperMode = ft.TextField(label="attributeChiperMode")
        self.attributePaddingMethod = ft.TextField(label="attributePaddingMethod")
        self.attributeKeyMaterial = ft.TextField(label="attributeKeyMaterial")
        self.contentsAlgorithm = ft.TextField(label="contentsAlgorithm")
        self.contentsKeyLength = ft.TextField(label="contentsKeyLength")
        self.readChk = ft.TextField(label="readChk")
        self.writeChk = ft.TextField(label="writeChk")
        self.excuteChk = ft.TextField(label="excuteChk")
        self.syncPeriod = ft.TextField(label="syncPeriod")
        self.logPeriod = ft.TextField(label="logPeriod")
        self.excludeExts = ft.TextField(label="excludeExts")
        self.decFileSize = ft.TextField(label="decFileSize")
        self.encErrorCode = ft.TextField(label="encErrorCode")
        self.decErrorCode = ft.TextField(label="decErrorCode")

    def clear(self):
        self.id.value = ""
        self.remark.value = ""
        self.createTime.value = ""
        self.updateTime.value = ""
        self.platform.value = ""
        self.providerName.value = ""
        self.process.value = ""
        self.ipAddr.value = ""
        self.macAddr.value = ""
        self.modifiedDate.value = ""
        self.domainKeyId.value = ""
        self.domainAlgorithm.value = ""
        self.domainKeyLength.value = ""
        self.modulus.value = ""
        self.publicExponent.value = ""
        self.privateExponent.value = ""
        self.domainCode.value = ""
        self.attributeKeyId.value = ""
        self.attributeIv.value = ""
        self.attributeAlgorithm.value = ""
        self.attributeKeyLength.value = ""
        self.attributeChiperMode.value = ""
        self.attributePaddingMethod.value = ""
        self.attributeKeyMaterial.value = ""
        self.contentsAlgorithm.value = ""
        self.contentsKeyLength.value = ""
        self.readChk.value = ""
        self.writeChk.value = ""
        self.excuteChk.value = ""
        self.syncPeriod.value = ""
        self.logPeriod.value = ""
        self.excludeExts.value = ""
        self.decFileSize.value = ""
        self.encErrorCode.value = ""
        self.decErrorCode.value = ""

    def view(self):
        print(self.platform.value)
        print(self.providerName.value)
        print(self.process.value)
        print(self.ipAddr.value)
        print(self.macAddr.value)
        print(self.modifiedDate.value)
        print(self.domainKeyId.value)
        print(self.domainAlgorithm.value)
        print(self.domainKeyLength.value)
        print(self.modulus.value)
        print(self.publicExponent.value)
        print(self.privateExponent.value)
        print(self.domainCode.value)
        print(self.attributeKeyId.value)
        print(self.attributeIv.value)
        print(self.attributeAlgorithm.value)
        print(self.attributeKeyLength.value)
        print(self.attributeChiperMode.value)
        print(self.attributePaddingMethod.value)
        print(self.attributeKeyMaterial.value)
        print(self.contentsAlgorithm.value)
        print(self.contentsKeyLength.value)
        print(self.readChk.value)
        print(self.writeChk.value)
        print(self.excuteChk.value)
        print(self.syncPeriod.value)
        print(self.logPeriod.value)
        print(self.excludeExts.value)
        print(self.decFileSize.value)
        print(self.encErrorCode.value)
        print(self.decErrorCode.value)


def load_json_file(page: ft.Page, filename, api):
    with open(filename) as json_file:
        json_data = json.load(json_file)
        api.platform.value = json_data["platform"]
        api.providerName.value = json_data["providerName"]
        api.process.value = json_data["process"]
        api.ipAddr.value = json_data["ipAddr"]
        api.macAddr.value = json_data["macAddr"]
        api.modifiedDate.value = json_data["modifiedDate"]
        api.domainKeyId.value = json_data["domainKeyId"]
        api.domainAlgorithm.value = json_data["domainAlgorithm"]
        api.domainKeyLength.value = json_data["domainKeyLength"]
        api.modulus.value = json_data["modulus"]
        api.publicExponent.value = json_data["publicExponent"]
        api.privateExponent.value = json_data["privateExponent"]
        api.domainCode.value = json_data["domainCode"]
        api.attributeKeyId.value = json_data["attributeKeyId"]
        api.attributeIv.value = json_data["attributeIv"]
        api.attributeAlgorithm.value = json_data["attributeAlgorithm"]
        api.attributeKeyLength.value = json_data["attributeKeyLength"]
        api.attributeChiperMode.value = json_data["attributeChiperMode"]
        api.attributePaddingMethod.value = json_data["attributePaddingMethod"]
        api.attributeKeyMaterial.value = json_data["attributeKeyMaterial"]
        api.contentsAlgorithm.value = json_data["contentsAlgorithm"]
        api.contentsKeyLength.value = json_data["contentsKeyLength"]
        api.readChk.value = json_data["readChk"]
        api.writeChk.value = json_data["writeChk"]
        api.excuteChk.value = json_data["excuteChk"]
        api.syncPeriod.value = json_data["syncPeriod"]
        api.logPeriod.value = json_data["logPeriod"]
        api.excludeExts.value = json_data["excludeExts"]
        api.decFileSize.value = json_data["decFileSize"]
        api.encErrorCode.value = json_data["encErrorCode"]
        api.decErrorCode.value = json_data["decErrorCode"]

        api.id.value = "API-" + json_data["ipAddr"]
        api.remark.value = "API-" + json_data["ipAddr"]
        api.createTime.value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        api.updateTime.value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        page.update()
