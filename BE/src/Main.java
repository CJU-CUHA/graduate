import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {

        EvtxReader evtxReader = new EvtxReader("Security.evtx");
        evtxReader.parseEvtxFile(0);
    }
}