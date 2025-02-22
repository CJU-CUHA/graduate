package org.example;


import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;


public class EvtxParser {
    private String filePath;
    private String saveFilePath;

    public EvtxParser(String filePath, String saveFilePath) {
        this.filePath = filePath;
        this.saveFilePath = saveFilePath;
    }

    public void parseEvtxFile() throws IOException {
        RandomAccessFile evtxFile = new RandomAccessFile(filePath, "r");
        evtxFile.seek(0);
        FileHeader fileHeader = new FileHeader();
        // Signature 읽기 (8바이트)
        byte[] signature = new byte[8];
        evtxFile.readFully(signature);
        fileHeader.setSignature(signature);

        // FirstChunkNumber (0x08)
        evtxFile.seek(0x08);
        fileHeader.setFirstChunkNumber(Long.reverseBytes(evtxFile.readLong()));

        // LastChunkNumber (0x10)
        evtxFile.seek(0x10);
        fileHeader.setLastChunkNumber(Long.reverseBytes(evtxFile.readLong()));

        // NextRecordIdentifier (0x18)
        evtxFile.seek(0x18);
        fileHeader.setNextRecordIdentifier(Long.reverseBytes(evtxFile.readLong()));

        // HeaderSize (0x20)
        evtxFile.seek(0x20);
        fileHeader.setHeaderSize(Integer.reverseBytes(evtxFile.readInt()));

        // MinorVersion (0x24)
        evtxFile.seek(0x24);
        fileHeader.setMinorVersion(Short.reverseBytes(evtxFile.readShort()));

        // MajorVersion (0x26)
        evtxFile.seek(0x26);
        fileHeader.setMajorVersion(Short.reverseBytes(evtxFile.readShort()));

        // HeaderBlockSize (0x28)
        evtxFile.seek(0x28);
        fileHeader.setHeaderBlockSize(Short.reverseBytes(evtxFile.readShort()));

        // OfChunks (0x2A)
        evtxFile.seek(0x2A);
        fileHeader.setOfChunks(Short.reverseBytes(evtxFile.readShort()));

        // Empty (0x2C, 12바이트)
        byte[] empty = new byte[12];
        evtxFile.seek(0x2C);
        evtxFile.readFully(empty);
        fileHeader.setEmpty(empty);

        // FileFlags (0x38)
        evtxFile.seek(0x38);
        fileHeader.setFileFlags(Integer.reverseBytes(evtxFile.readInt()));

        // Checksum (0x3C)
        evtxFile.seek(0x3C);
        fileHeader.setChecksum(Integer.reverseBytes(evtxFile.readInt()));

        // 첫 번째 청크의 오프셋 설정
        long offset = 4096L;// 일반적으로 4096 또는 64바이트
//        System.out.println("fileHeader.getHeaderSize() = " + fileHeader.getHeaderSize());
        for (long i = fileHeader.getFirstChunkNumber(); i <= fileHeader.getLastChunkNumber(); i++) {
            if (offset >= evtxFile.length()) {
                System.out.println("Reached the end of the file.");
                break;  // 파일의 끝에 도달하면 루프 종료
            }

            ChunkHeader chunkHeader = parseChunkHeader(evtxFile, offset);
//            System.out.println("offset = " + offset);
            if (chunkHeader == null) break;

            offset += 65536; // 일반적으로 EVTX 청크 크기는 64KB (65536바이트)
        }

        evtxFile.close();


    }

    public ChunkHeader parseChunkHeader(RandomAccessFile raf, long offset) throws IOException {
        long num = offset;
        raf.seek(offset);
        ChunkHeader chunkHeader = new ChunkHeader();

        byte[] signature = new byte[8];
        raf.readFully(signature);
        chunkHeader.setSignature(signature);

        raf.seek(offset + 0x08);
        chunkHeader.setFirstEventRecordNumber(Long.reverseBytes(raf.readLong()));
        raf.seek(offset + 0x10);
        chunkHeader.setLastEventRecordNumber(Long.reverseBytes(raf.readLong()));
        raf.seek(offset + 0x18);
        chunkHeader.setFirstEventRecordIdentifier(Long.reverseBytes(raf.readLong()));
        raf.seek(offset + 0x20);
        chunkHeader.setLastEventRecordIdentifier(Long.reverseBytes(raf.readLong()));
        raf.seek(offset + 0x28);
        chunkHeader.setHeaderSize(Integer.reverseBytes(raf.readInt()));
        raf.seek(offset + 0x2A);
        chunkHeader.setLastEventRecordDataOffset(Integer.reverseBytes(raf.readInt()));
        raf.seek(offset + 0x3C);
        chunkHeader.setFreeSpaceOffset(Integer.reverseBytes(raf.readInt()));
        raf.seek(offset + 0x40);
        chunkHeader.setEventRecordsChecksum(Integer.reverseBytes(raf.readInt()));

        byte[] empty = new byte[16];
        raf.readFully(empty);
        chunkHeader.setEmpty(empty);

        chunkHeader.setUnknownFlag(Integer.reverseBytes(raf.readInt()));
        raf.seek(offset + 0x48);
        chunkHeader.setChecksum(Integer.reverseBytes(raf.readInt()));

        for (long i = chunkHeader.getFirstEventRecordNumber(); i <= chunkHeader.getLastEventRecordNumber(); i++) {
            // 파일 끝에 도달한 경우
            if (raf.getFilePointer() >= raf.length()) {
                System.out.println("Reached the end of the file.");
                break;  // 파일의 끝에 도달하면 루프 종료
            }

            try {
                // 레코드 파싱
                HashMap<String, String> map = parseRecords(raf, num);

                // 파싱된 결과에서 xmlData를 출력
                if (map != null && map.containsKey("xmlData")) {
                    System.out.println(map.get("xmlData"));
//                    appendXmlToFile(map.get("xmlData"));
                    num += 65536;
                } else {
                    System.out.println("No xmlData found for this record.");
                }

                // 다음 레코드로 이동 (EVTX 청크 크기 64KB)


            } catch (IOException e) {
                // 파일 읽기 오류 처리
                System.err.println("Error reading record at offset " + num + ": " + e.getMessage());
                break;  // 오류 발생 시 루프 종료
            }
        }

        return chunkHeader;
    }
    public HashMap<String,String> parseRecords(RandomAccessFile raf, long offset) throws IOException {

        RecordStructure recordStructure = new RecordStructure();
        raf.seek(offset + 0x10200);  // 오프셋 이동
//        System.out.println("Seek to offset: " + (offset + 0x10200));

        byte[] signature = new byte[4];

        // EOF 방지: 파일 크기보다 작을 때만 읽기
        if (raf.getFilePointer() + 4 > raf.length()) {

        }

        raf.readFully(signature);  // 서명 읽기
        recordStructure.setSignature(signature);
//        System.out.println("Signature: " + new String(signature, StandardCharsets.US_ASCII));

        raf.seek(offset + 0x10204);  // 기록 크기 읽을 위치로 이동

        // EOF 방지: 파일 크기보다 작을 때만 읽기
        if (raf.getFilePointer() + 4 > raf.length()) {
            throw new IOException("Unexpected end of file while reading record size.");
        }

        recordStructure.setSize(Integer.reverseBytes(raf.readInt()));  // 크기 읽기
//        System.out.println("Size: " + recordStructure.getSize());

        raf.seek(offset + 0x1E);  // EventRecordIdentifier 읽을 위치로 이동
//        System.out.println("Seek to offset for EventRecordIdentifier: " + (offset + 0x1E));

        // EOF 방지: 파일 크기보다 작을 때만 읽기
        if (raf.getFilePointer() + 8 > raf.length()) {
            throw new IOException("Unexpected end of file while reading EventRecordIdentifier.");
        }

        recordStructure.setEventRecordIdentifier(Long.reverseBytes(raf.readLong()));  // EventRecordIdentifier 읽기
//        System.out.println("Event Record Identifier: " + recordStructure.getEventRecordIdentifier());

        raf.seek(offset + 0x20);  // FileTimeTimestamp 읽을 위치로 이동
//        System.out.println("Seek to offset for FileTimeTimestamp: " + (offset + 0x20));

        // EOF 방지: 파일 크기보다 작을 때만 읽기
        if (raf.getFilePointer() + 8 > raf.length()) {
            throw new IOException("Unexpected end of file while reading FileTimeTimestamp.");
        }

        recordStructure.setFileTimeTimestamp(Long.reverseBytes(raf.readLong()));  // FileTimeTimestamp 읽기
//        System.out.println("File Time Timestamp: " + recordStructure.getFileTimeTimestamp());

        // XML 데이터 읽기
        int eventSize = recordStructure.getSize();  // RecordStructure의 size 값을 가져옴
//        System.out.println("Event size: " + eventSize);

        long remainingBytes = raf.length() - raf.getFilePointer();
//        System.out.println("Remaining bytes: " + remainingBytes);

        if (remainingBytes < eventSize) {
            throw new IOException("Not enough data to read the expected event record.");
        }

        // size에 맞는 만큼 데이터를 읽어옴
        byte[] xmlDataBytes = new byte[eventSize];

        // EOF 방지: 파일 크기보다 작을 때만 읽기
        if (raf.getFilePointer() + eventSize > raf.length()) {
            throw new IOException("Unexpected end of file while reading XML data.");
        }

        raf.readFully(xmlDataBytes);  // xml 데이터 읽기
        recordStructure.setEvent(xmlDataBytes);  // RecordStructure에 xml 데이터 저장

        // 바이트 배열을 UTF-8로 변환
        String xmlData = new String(removeInvalidBytes(xmlDataBytes), StandardCharsets.US_ASCII);
//        System.out.println("xmlData.length() = " + xmlData.length());
        HashMap<String,String> map = new HashMap<>();
        map.put("signature",new String(recordStructure.getSignature(), StandardCharsets.US_ASCII));
        map.put("size",String.valueOf(recordStructure.getSize()));
        map.put("eventRecordIdentifier " ,String.valueOf(recordStructure.getEventRecordIdentifier()));
        map.put("fileTimeStamp ",String.valueOf(recordStructure.getFileTimeTimestamp()));
        map.put("xmlData", xmlData);

        // 결과 문자열 배열 반환
        return map;

    }
    private static byte[] removeInvalidBytes(byte[] input) {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        for (byte b : input) {
            // 비정상적인 바이트가 아니면 outputStream에 추가
            if (b >= 0x20) {
                outputStream.write(b);
            }
        }

        return outputStream.toByteArray();
    }
    // Append new xmlData to existing XML file
    private void appendXmlToFile(String xmlData) {
        try {
            // Load existing XML document (if exists)
            Document document;
            File xmlFile = new File(saveFilePath);
            if (xmlFile.exists()) {
                DocumentBuilderFactory documentFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder documentBuilder = documentFactory.newDocumentBuilder();
                document = documentBuilder.parse(xmlFile);
            } else {
                // Create a new document if the file doesn't exist
                DocumentBuilderFactory documentFactory = DocumentBuilderFactory.newInstance();
                DocumentBuilder documentBuilder = documentFactory.newDocumentBuilder();
                document = documentBuilder.newDocument();
                Element root = document.createElement("Records");
                document.appendChild(root);
            }

            // Append new xmlData as a new record in the XML file
            Element root = document.getDocumentElement();
            Element recordElement = document.createElement("Record");
            recordElement.appendChild(document.createTextNode(xmlData));
            root.appendChild(recordElement);

            // Save the updated document back to the file
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            DOMSource domSource = new DOMSource(document);
            StreamResult streamResult = new StreamResult(xmlFile);
            transformer.transform(domSource, streamResult);

            System.out.println("xmlData appended to existing XML file.");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
