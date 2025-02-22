package org.example;

public class RecordStructure {
    byte[] Signature=new byte[4];
    private int size;  // 4바이트
    private long eventRecordIdentifier;  // 8바이트
    private long fileTimeTimestamp;  // 8바이트
    private byte[] event;  // 가변 크기
    private int size2;

    public byte[] getSignature() {
        return Signature;
    }

    public void setSignature(byte[] signature) {
        Signature = signature;
    }

    public int getSize() {
        return size;
    }

    public void setSize(int size) {
        this.size = size;
    }

    public long getEventRecordIdentifier() {
        return eventRecordIdentifier;
    }

    public void setEventRecordIdentifier(long eventRecordIdentifier) {
        this.eventRecordIdentifier = eventRecordIdentifier;
    }

    public long getFileTimeTimestamp() {
        return fileTimeTimestamp;
    }

    public void setFileTimeTimestamp(long fileTimeTimestamp) {
        this.fileTimeTimestamp = fileTimeTimestamp;
    }

    public byte[] getEvent() {
        return event;
    }

    public void setEvent(byte[] event) {
        this.event = event;
    }

    public int getSize2() {
        return size2;
    }

    public void setSize2(int size2) {
        this.size2 = size2;
    }
}
