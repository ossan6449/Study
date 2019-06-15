import ijava.awt.*;
import java.awt.event.*;

public class Reidai1{
    public static void main(String args[]){
        MyFrame1 fm = new MyFrame1("フレームテスト");        // フレームオブジェクトを生成する
        fm.setSize(200, 150);                               // ウィンドウサイズを横200、縦150にする
        fm.setVisible(true);                                // フレーム（ウィンドウ）を表示する
        fm.show();
    }
}