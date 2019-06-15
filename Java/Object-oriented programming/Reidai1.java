import java.awt.*;
import java.awt.event.*;

public class Reidai1{
    public static void main(String args[]){
        MyFrame1 fm = new MyFrame1("フレームテスト");
        fm.setSize(200, 150);
        fm.setVisible(true);
//      fm.show();
    }
}
class MyFrame1 extends Frame{
    MyFrame1(String title){
        super(title);
        WinCloseOn();
    }
    private void WinCloseOn(){                          // 閉じるボタン処理をメソッド化
        addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent e){
                System.exit(0);
            }
        });
    }
    public void paint(Graphics g){
        g.drawString("最初のフレームテストです",30,60);
    }
}

