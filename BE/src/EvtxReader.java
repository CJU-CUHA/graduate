import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import org.apache.commons.text.StringEscapeUtils;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class EvtxReader {
    private String filePath;

    public EvtxReader(String filePath) {
        this.filePath = filePath;
    }

    public void parseEvtxFile(long offset) {
        try (RandomAccessFile raf = new RandomAccessFile(filePath, "r")) {
            // EVTX 파일 시그니처 확인
            byte[] signature = new byte[8];
            raf.read(signature);

            if (!Arrays.equals(signature, "ElfFile\0".getBytes(StandardCharsets.UTF_8))) {
                System.out.println("Invalid EVTX file signature");
                return;
            }
            System.out.println("ElfFile detected!");

            // 0x28 위치에서 헤더 크기 확인
            raf.seek(offset + 0x28);
            short headerSize = Short.reverseBytes(raf.readShort());
            System.out.println("Header Size: " + headerSize);

            // 청크 파싱 시작
            parseChunks(raf, offset + headerSize);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void parseChunks(RandomAccessFile raf, long offset) throws IOException {
        raf.seek(offset);
        System.out.println("Parsing Chunk at offset: " + offset);

        byte[] chunkSignature = new byte[8];
        raf.read(chunkSignature);
        String chunkSignatureStr = new String(chunkSignature, StandardCharsets.UTF_8);
        System.out.println("chunkSignatureStr = " + chunkSignatureStr);
        if (!Arrays.equals(chunkSignature, "ElfChnk\0".getBytes(StandardCharsets.UTF_8))) {
            System.out.println("Invalid Chunk Signature");
            return;
        }
        System.out.println("ElfChnk detected!");

        // 0x28 위치에서 헤더 크기 확인
        raf.seek(offset + 0x28);
        int headerSize = Integer.reverseBytes(raf.readInt());
        System.out.println("Chunk Header Size: " + headerSize);

        // 이벤트 레코드 시작 위치 계산
        long eventRecordsOffset = offset + Integer.parseInt(Integer.toOctalString(headerSize));
//        System.out.println("offset = " + offset);
//        System.out.println("eventRecordsOffset = " + eventRecordsOffset);
        parseEventRecords(raf, eventRecordsOffset);
    }

    private static void parseEventRecords(RandomAccessFile raf, long offset) throws IOException {
        raf.seek(offset+312);
        List<EventRecord> eventRecords = new ArrayList<>();
        System.out.println("raf.getFilePointer() = " + raf.getFilePointer());
        while (raf.getFilePointer() < raf.length()) {
            long position = raf.getFilePointer();
            System.out.println("Parsing record at position: " + position);

            // 4바이트 레코드 시그니처 확인 (0x2A 2A 00 00)
            int signature = Integer.reverseBytes(raf.readInt());
            if (signature != 0x00002A2A) {
                System.out.println("Invalid Record Signature: " + Integer.toHexString(signature));
                break;
            }

            // 4바이트 크기 (Little Endian)
            int recordSize = Integer.reverseBytes(raf.readInt());
            System.out.println("Record Size: " + recordSize);

            if (recordSize <= 24) continue;

            // 8바이트 레코드 번호
            long recordNumber = Long.reverseBytes(raf.readLong());

            // 8바이트 타임스탬프 (Windows FILETIME -> UNIX timestamp 변환)
            long rawTimestamp = Long.reverseBytes(raf.readLong());
            LocalDateTime timestamp = convertWindowsFileTime(rawTimestamp);

            // XML 데이터 읽기
            byte[] xmlData = new byte[recordSize - 24];
            raf.read(xmlData);
            String xmlString = new String(xmlData);
            // 이벤트 레코드를 리스트에 추가
            eventRecords.add(new EventRecord(recordNumber, rawTimestamp, xmlString,"EventData","Data"));
            System.out.println("Event #" + recordNumber + " (Timestamp: " + timestamp + ")");
            System.out.println("XML Data:\n" + xmlString);
            System.out.println("----------------------------------------------");

            // 다음 레코드로 이동
            raf.seek(position + recordSize);
        }
        saveXMLToFile(eventRecords);
    }

    private static LocalDateTime convertWindowsFileTime(long fileTime) {
        long unixTime = (fileTime - 116444736000000000L) / 10000;
        return LocalDateTime.ofInstant(Instant.ofEpochMilli(unixTime), ZoneOffset.UTC);
    }
    // 이벤트 레코드를 XML 파일로 저장하는 메서드
    private static void saveXMLToFile(List<EventRecord> eventRecords) {
        try {
            // XML 문서 빌더 준비
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.newDocument();

            // 루트 엘리먼트 생성
            Element root = document.createElement("EventRecords");
            document.appendChild(root);

            // 모든 이벤트 레코드를 XML로 추가
            for (EventRecord record : eventRecords) {
                Element eventElement = document.createElement("EventRecord");

                // 레코드 번호
                Element recordNumElement = document.createElement("RecordNumber");
                recordNumElement.appendChild(document.createTextNode(String.valueOf(record.getRecordNumber())));
                eventElement.appendChild(recordNumElement);

                // 타임스탬프
                Element timestampElement = document.createElement("Timestamp");
                timestampElement.appendChild(document.createTextNode(String.valueOf(record.getTimestamp())));
                eventElement.appendChild(timestampElement);

                // EventData (새로운 데이터 항목 추가)
                Element eventDataElement = document.createElement("EventData");
                eventDataElement.appendChild(document.createTextNode(record.getEventData()));
                eventElement.appendChild(eventDataElement);

                // Provider (새로운 데이터 항목 추가)
                Element providerElement = document.createElement("Provider");
                providerElement.appendChild(document.createTextNode(record.getProvider()));
                eventElement.appendChild(providerElement);

                // XML 데이터를 sanitize 후 추가
                String sanitizedXmlData = sanitizeXMLString(record.getXmlData());
                Element xmlElement = document.createElement("XMLData");
                xmlElement.appendChild(document.createTextNode(StringEscapeUtils.unescapeHtml4(sanitizedXmlData).replace("�","1")));
                eventElement.appendChild(xmlElement);

                root.appendChild(eventElement);
            }

            // Transformer 설정
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");

            // 결과를 파일로 출력
            StreamResult result = new StreamResult("evtx_all_events.xml");
            DOMSource source = new DOMSource(document);
            transformer.transform(source, result);

            System.out.println("XML file saved: evtx_all_events.xml");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 유효하지 않은 XML 문자를 제거하는 메서드 (0x00-0x1F 및 0x7F 제어 문자 제거)
    private static String sanitizeXMLString(String input) {
        // XML에서 유효하지 않은 문자 (제어 문자 등) 제거
        return input.replaceAll("[\\x00-\\x1F\\x7F]", "");
    }

    // 예시로 이벤트 레코드를 만드는 메서드 (실제로는 EvtxReader에서 읽은 데이터를 사용)
    private static List<EventRecord> getEventRecords() {
        // 실제 이벤트 로그 데이터를 기반으로 EventRecord 객체를 생성
        EventRecord record = new EventRecord(1, 1628876884000L, "Sample XML Data with some invalid characters \u0000\u001F\u007F", "EventData Example", "Provider Example");
        return List.of(record);
    }

    // 이벤트 레코드 클래스
    private static class EventRecord {
        private long recordNumber;
        private long timestamp;
        private String xmlData;
        private String eventData;
        private String provider;

        public EventRecord(long recordNumber, long timestamp, String xmlData, String eventData, String provider) {
            this.recordNumber = recordNumber;
            this.timestamp = timestamp;
            this.xmlData = xmlData;
            this.eventData = eventData;
            this.provider = provider;
        }

        public long getRecordNumber() {
            return recordNumber;
        }

        public long getTimestamp() {
            return timestamp;
        }

        public String getXmlData() {
            return xmlData;
        }

        public String getEventData() {
            return eventData;
        }

        public String getProvider() {
            return provider;
        }
    }
}
