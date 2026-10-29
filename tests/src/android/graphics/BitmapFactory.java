package android.graphics;
import java.io.*;
import java.nio.file.*;
import java.security.*;
import java.util.*;
public final class BitmapFactory {
    public static final class Options {
        public boolean inScaled,inPremultiplied;public Bitmap.Config inPreferredConfig;
    }
    public static Bitmap decodeByteArray(byte[] data,int offset,int length,Options options){
        try {
            byte[] hash=MessageDigest.getInstance("SHA-256").digest(Arrays.copyOfRange(data,offset,offset+length));
            StringBuilder key=new StringBuilder();for(byte b:hash)key.append(String.format("%02x",b&255));
            byte[] rgba=Files.readAllBytes(Paths.get(System.getProperty("fixture.dir"),key.toString()));
            int[] argb=new int[4096];
            if(rgba.length!=4096*4)throw new IOException("Unexpected fixture dimensions");
            for(int i=0;i<4096;i++){int j=i*4;argb[i]=((rgba[j+3]&255)<<24)|((rgba[j]&255)<<16)|((rgba[j+1]&255)<<8)|(rgba[j+2]&255);}
            return Bitmap.createBitmap(argb,64,64,Bitmap.Config.ARGB_8888);
        }catch(Exception e){throw new IllegalStateException(e);}
    }
}
