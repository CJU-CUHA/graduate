package org.example;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {

        System.out.println("Hello, World!");
        EvtxParser evtxParser = new EvtxParser("Security.evtx","evtx_all_events.xml");
        evtxParser.parseEvtxFile();
    }
}