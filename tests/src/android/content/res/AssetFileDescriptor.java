package android.content.res;
import java.io.*;
public final class AssetFileDescriptor implements AutoCloseable {
    private final File file; private final long start, length;
    public AssetFileDescriptor(File file,long start,long length) { this.file=file;this.start=start;this.length=length; }
    public long getLength(){return length;}
    public long getStartOffset(){return start;}
    public FileInputStream createInputStream() throws IOException {return new FileInputStream(file);}
    public void close(){}
}
