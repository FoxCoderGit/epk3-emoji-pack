package android.content.res;
import java.io.*;
public final class AssetManager {
    public AssetFileDescriptor openFd(String name) throws IOException {
        File file=new File(System.getProperty("fixture.asset"));
        return new AssetFileDescriptor(file,137,file.length()-144);
    }
}
