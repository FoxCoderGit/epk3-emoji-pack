package android.graphics;
public final class Bitmap {
    public enum Config {ARGB_8888}
    private final int[] pixels;private final int width,height;
    private Bitmap(int[] p,int w,int h){pixels=p.clone();width=w;height=h;}
    public static Bitmap createBitmap(int[] p,int w,int h,Config config){return new Bitmap(p,w,h);}
    public int getWidth(){return width;}
    public int getHeight(){return height;}
    public void recycle(){}
    public void getPixels(int[] out,int offset,int stride,int x,int y,int w,int h){
        for(int row=0;row<h;row++)System.arraycopy(pixels,(y+row)*width+x,out,offset+row*stride,w);
    }
}
