
import xml.etree.ElementTree as ET
from Evtx.Evtx import Evtx
import json
def parse_evtx(file_path):
    events = []  # 이벤트 데이터를 저장할 리스트
    with Evtx(file_path) as log:
        for record in log.records():
            xml_data = record.xml()
            try:
                # XML 파싱 (이벤트 XML은 기본 네임스페이스 사용)
                root = ET.fromstring(xml_data)
                ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}

                # 이벤트 아이디: /Event/System/EventID 텍스트
                event_id_elem = root.find('./ns:System/ns:EventID', ns)
                event_id = event_id_elem.text if event_id_elem is not None else 'N/A'

                # 이벤트 발생 시각: /Event/System/TimeCreated 요소의 SystemTime 속성
                time_created_elem = root.find('./ns:System/ns:TimeCreated', ns)
                time_created = time_created_elem.attrib.get('SystemTime') if time_created_elem is not None else 'N/A'

                # 요약 정보: EventData 섹션의 각 Data 요소
                event_data_elem = root.find('./ns:EventData', ns)
                summary_list = []
                if event_data_elem is not None:
                    for data in event_data_elem.findall('ns:Data', ns):
                        name = data.attrib.get('Name', '').strip()
                        value = data.text.strip() if data.text else ''
                        if name:
                            summary_list.append({name: value})
                        else:
                            summary_list.append(value)

                # 이벤트 데이터를 하나의 dict로 구성 (요약정보는 JSON 형식의 리스트)
                event_record = {
                    "event_id": event_id,
                    "time_created": time_created,
                    "summary": summary_list
                }

                # 콘솔 출력 (디버깅용)
                print("===== 이벤트 시작 =====")
                print("Event ID      :", event_id)
                print("Time Created  :", time_created)
                print("Summary       :", json.dumps(summary_list, ensure_ascii=False, indent=2))
                print("===== 이벤트 종료 =====\n")

                events.append(event_record)
            except Exception as e:
                print("XML 파싱 중 오류 발생:", e)
    return events

if __name__ == "__main__":
    # EVTX 파일의 경로 (필요에 따라 경로 수정)
    evtx_file = "BE\\app\\evtx\\Security.evtx"
    events = parse_evtx(evtx_file)

    # 파싱된 이벤트 데이터를 JSON 파일로 저장
    output_file = "events_output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

    print(f"\n총 {len(events)}개의 이벤트가 '{output_file}'에 저장되었습니다.")
