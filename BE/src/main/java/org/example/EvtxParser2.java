package org.example;

import org.w3c.dom.*;
import org.xml.sax.InputSource;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.xpath.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class EvtxParser2 {
    public static void main(String[] args) {
        // 읽을 바이너리 파일 경로
        String filePath = "Security.evtx";
        String xmlFilePath = "cleaned_eventlog.xml";  // 저장할 XML 파일 경로

        try (FileInputStream fis = new FileInputStream(filePath)) {
            // 파일 크기 확인
            File file = new File(filePath);
            long fileLength = file.length();
            System.out.println("File Length: " + fileLength + " bytes");

            // 파일 전체 읽기
            byte[] buffer = new byte[(int) fileLength];
            fis.read(buffer);

            // 비정상적인 바이트(예: 0x00 ~ 0x1F 범위) 삭제
            byte[] cleanedBuffer = removeInvalidBytes(buffer);

            // 바이트 배열을 UTF-8 문자열로 변환
            String fileContent = new String(cleanedBuffer, StandardCharsets.US_ASCII);

            // "Event" 문자열 찾기
            findEventInText(fileContent);

            // XML 문서 생성
            Document doc = createXmlDocument(fileContent);

            // XML 파일로 저장
            saveXmlToFile(doc, xmlFilePath);
            System.out.println("XML saved to: " + xmlFilePath);

            // XML에서 <Event> 태그 찾기
            if (containsEventTag(doc)) {
                System.out.println("The XML contains <Event> tags.");
            } else {
                System.out.println("No <Event> tags found in the XML.");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 비정상적인 바이트(0x00 ~ 0x1F) 삭제하는 메서드
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

    // "Event" 문자열 찾기
    private static void findEventInText(String content) {
        int index = content.indexOf("Event");
        if (index != -1) {
            System.out.println("\"Event\" found at position: " + index);
        } else {
            System.out.println("\"Event\" not found in the file.");
        }
    }

    // XML 문서에서 <Event> 태그가 존재하는지 확인
    private static boolean containsEventTag(Document doc) throws Exception {
        XPathFactory xPathFactory = XPathFactory.newInstance();
        XPath xpath = xPathFactory.newXPath();
        XPathExpression expr = xpath.compile("//Event");

        Node eventNode = (Node) expr.evaluate(doc, XPathConstants.NODE);
        return eventNode != null;
    }

    // XML 문서 생성
    private static Document createXmlDocument(String fileContent) throws Exception {
        // DocumentBuilderFactory와 DocumentBuilder를 사용하여 XML 생성
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.newDocument();

        // root element 생성
        Element rootElement = doc.createElement("EventLog");
        doc.appendChild(rootElement);

        // content를 포함하는 <Event> 요소 생성
        Element eventElement = doc.createElement("Event");
        eventElement.appendChild(doc.createTextNode(fileContent)); // 파일 내용 추가

        rootElement.appendChild(eventElement);

        return doc;
    }

    // XML 파일로 저장
    private static void saveXmlToFile(Document doc, String xmlFilePath) throws Exception {
        // Transformer 객체 생성
        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer transformer = transformerFactory.newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");

        // XML을 파일로 저장
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(new File(xmlFilePath));
        transformer.transform(source, result);
    }
}
