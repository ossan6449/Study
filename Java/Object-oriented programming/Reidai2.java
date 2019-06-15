import java.awt.*;
import java.awt.event.*;

public class Reidai2{
    public static void main(String args[]){
        MyFrame1 fm = new MyFrame1("フレームへの描画");
        fm.setSize(300, 120);
        fm.setVisible(true);                             // ウィンドウを表示         
        // fm.show();                                    // 非推奨 
    }
}
class MyFrame1 extends Frame {
    MyFrame1(String title) {
        super(title);
        WinCloseOn();
    }
    private void WinCloseOn(){
        addWindowListener(new WindowAdapter(){
            public void windowClosing(WindowEvent e){
                System.exit(0);
            }
        });
    }
    public void paint(Graphics g){
        setBackground(Color.yellow);

        g.setColor(Color.blue);
        g.drawString("現在食：青",10,60);
        g.fillRect(100,40,200,28);

        g.setColor(new Color(0,255, 0));
        g.drawString("現在色：緑", 10,90);
        g.fillRect(100, 70, 200, 28);
    }
}
