package org.example;

public class FileHeader {
    private byte[] signature = new byte[8];
    private Long FirstChunkNumber;
    private Long LastChunkNumber;
    private Long NextRecordIdentifier;
    private int HeaderSize;
    private short MinorVersion;
    private short MajorVersion;
    private short HeaderBlockSize;
    private short OfChunks;
    private byte[] Empty=new byte[12];
    private int FileFlags;
    private int Checksum;

    public byte[] getSignature() {
        return signature;
    }

    public void setSignature(byte[] signature) {
        this.signature = signature;
    }

    public Long getFirstChunkNumber() {
        return FirstChunkNumber;
    }

    public void setFirstChunkNumber(Long firstChunkNumber) {
        FirstChunkNumber = firstChunkNumber;
    }

    public Long getLastChunkNumber() {
        return LastChunkNumber;
    }

    public void setLastChunkNumber(Long lastChunkNumber) {
        LastChunkNumber = lastChunkNumber;
    }

    public Long getNextRecordIdentifier() {
        return NextRecordIdentifier;
    }

    public void setNextRecordIdentifier(Long nextRecordIdentifier) {
        NextRecordIdentifier = nextRecordIdentifier;
    }

    public int getHeaderSize() {
        return HeaderSize;
    }

    public void setHeaderSize(int headerSize) {
        HeaderSize = headerSize;
    }

    public short getMinorVersion() {
        return MinorVersion;
    }

    public void setMinorVersion(short minorVersion) {
        MinorVersion = minorVersion;
    }

    public short getMajorVersion() {
        return MajorVersion;
    }

    public void setMajorVersion(short majorVersion) {
        MajorVersion = majorVersion;
    }

    public short getHeaderBlockSize() {
        return HeaderBlockSize;
    }

    public void setHeaderBlockSize(short headerBlockSize) {
        HeaderBlockSize = headerBlockSize;
    }

    public short getOfChunks() {
        return OfChunks;
    }

    public void setOfChunks(short ofChunks) {
        OfChunks = ofChunks;
    }

    public byte[] getEmpty() {
        return Empty;
    }

    public void setEmpty(byte[] empty) {
        Empty = empty;
    }

    public int getFileFlags() {
        return FileFlags;
    }

    public void setFileFlags(int fileFlags) {
        FileFlags = fileFlags;
    }

    public int getChecksum() {
        return Checksum;
    }

    public void setChecksum(int checksum) {
        Checksum = checksum;
    }
}
