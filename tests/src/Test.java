import java.io.*;
import android.graphics.Bitmap;
import io.github.foxcodergit.epk3.EmojiPack;
public final class Test {
    public static void main(String[] args) throws Exception {
        EmojiPack pack=new EmojiPack(new android.content.Context());
        try(DataInputStream input=new DataInputStream(new FileInputStream(args[0]))) {
            int count=input.readInt();if(input.readInt()!=count)throw new AssertionError();
            int[] pixels=new int[4096];
            for(int i=0;i<count;i++){
                int key=input.readUnsignedShort();input.readUnsignedShort();
                Bitmap bitmap=pack.getEmoji(key/4096,key%4096);
                if(bitmap==null)throw new AssertionError("Missing key "+key);
                bitmap.getPixels(pixels,0,64,0,0,64,64);
                for(int j=0;j<4096;j++)if(pixels[j]!=input.readInt())throw new AssertionError("RGBA mismatch "+key+":"+j);
                bitmap.recycle();pack.clearCache();
            }
        }
        System.out.println("PASS: Java decoder matches independent RGBA fixtures");
    }
}
