package org.example;

public class ChunkHeader {
    private byte[] Signature= new byte[8];
    private Long FirstEventRecordNumber;
    private Long LastEventRecordNumber;
    private Long FirstEventRecordIdentifier;
    private Long LastEventRecordIdentifier;
    private int HeaderSize;
    private int LastEventRecordDataOffset;
    private int FreeSpaceOffset;
    private int EventRecordsChecksum;
    private byte[] Empty=new byte[16];
    private int UnknownFlag;
    private int Checksum;

    public byte[] getSignature() {
        return Signature;
    }

    public void setSignature(byte[] signature) {
        Signature = signature;
    }

    public Long getFirstEventRecordNumber() {
        return FirstEventRecordNumber;
    }

    public void setFirstEventRecordNumber(Long firstEventRecordNumber) {
        FirstEventRecordNumber = firstEventRecordNumber;
    }

    public Long getLastEventRecordNumber() {
        return LastEventRecordNumber;
    }

    public void setLastEventRecordNumber(Long lastEventRecordNumber) {
        LastEventRecordNumber = lastEventRecordNumber;
    }

    public Long getFirstEventRecordIdentifier() {
        return FirstEventRecordIdentifier;
    }

    public void setFirstEventRecordIdentifier(Long firstEventRecordIdentifier) {
        FirstEventRecordIdentifier = firstEventRecordIdentifier;
    }

    public Long getLastEventRecordIdentifier() {
        return LastEventRecordIdentifier;
    }

    public void setLastEventRecordIdentifier(Long lastEventRecordIdentifier) {
        LastEventRecordIdentifier = lastEventRecordIdentifier;
    }

    public int getHeaderSize() {
        return HeaderSize;
    }

    public void setHeaderSize(int headerSize) {
        HeaderSize = headerSize;
    }

    public int getLastEventRecordDataOffset() {
        return LastEventRecordDataOffset;
    }

    public void setLastEventRecordDataOffset(int lastEventRecordDataOffset) {
        LastEventRecordDataOffset = lastEventRecordDataOffset;
    }

    public int getFreeSpaceOffset() {
        return FreeSpaceOffset;
    }

    public void setFreeSpaceOffset(int freeSpaceOffset) {
        FreeSpaceOffset = freeSpaceOffset;
    }

    public int getEventRecordsChecksum() {
        return EventRecordsChecksum;
    }

    public void setEventRecordsChecksum(int eventRecordsChecksum) {
        EventRecordsChecksum = eventRecordsChecksum;
    }

    public byte[] getEmpty() {
        return Empty;
    }

    public void setEmpty(byte[] empty) {
        Empty = empty;
    }

    public int getUnknownFlag() {
        return UnknownFlag;
    }

    public void setUnknownFlag(int unknownFlag) {
        UnknownFlag = unknownFlag;
    }

    public int getChecksum() {
        return Checksum;
    }

    public void setChecksum(int checksum) {
        Checksum = checksum;
    }
}
