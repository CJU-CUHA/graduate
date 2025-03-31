from Evtx.Evtx import Evtx
import json
import xmltodict
import datetime
from lxml import etree as ET  # lxml 사용

start = datetime.datetime.now()
namespace = {'ns0': 'http://schemas.microsoft.com/win/2004/08/events/event'}

# 파일 경로 설정
evtx_file = "evtx\\Security.evtx"
json_file = "json\\data3.json"

# 삭제할 태그 리스트 (System 태그 안의 하위 요소만 삭제)
tags_to_remove = {"Provider", "Version", "Level", "Task", "Opcode", 
                  "Keywords", "Correlation", "Execution", "Channel", 
                  "Computer", "Security"}

events = []

with Evtx(evtx_file) as log:
    for record in log.records():
        
        root = ET.fromstring(record.xml().encode("utf-8"))  # XML 파싱
        
        # Event 태그 순회
            # System 태그 찾기
        system_elem = root.find(".//ns0:System", namespaces=namespace)

        if system_elem is not None:
        # System 내부에서만 삭제
            for tag in tags_to_remove:
                for elem in system_elem.findall(f"ns0:{tag}", namespaces=namespace):
                    system_elem.remove(elem)  # 태그 삭제

        # XML -> JSON 변환 후 리스트에 추가
        # 수정된 XML을 문자열로 변환
        modified_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")

# 수정된 XML을 딕셔너리로 변환
        xml_dict = xmltodict.parse(modified_xml)
        events.append(xml_dict)

# JSON 파일로 저장
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(events, f, indent=4, ensure_ascii=False)

end = datetime.datetime.now()
print("✅ convert xml to json 완료")
print(f"⏳ duration: {end - start}")
