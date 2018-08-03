package HIU;
import java.awt.*;
import java.awt.event.*;

public class Reidai3b {
	public static void maint(String args[]) {
		MyFrame3b fm = new MyFrame3b("マウスアダプタ");
		fm.setSize(300,150);
		fm.setVisible(true);
	}
}
class MyFrame3b extends Frame {
	String s1 = "", s2 = "";
	int x = -1, y;
	
	MyFrame3b(String title) {
		super(title);
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
		addMouseListener(new MyMouseListener(this));	// マウスリストを登録
	}
	
	public void paint(Graphics g) {
		if(x != -1) {
			g.drawLine(x-10,y,x+10,y);		// +マークを描画
			g.drawLine(x,y-10,x,y+10);
		}
	}
	// MouseListenerインターフェースではなくMouseAdapterクラスを使う
	class MyMouseListener extends MouseAdapter {
		MyFrame3b mf;
		
		public MyMouseListener(MyFrame3b mfr) {
			mf = mfr;		// MyFrame3bオブジェクト
		}
		public void mouseClicked(MouseEvent me) {
			mf.x = me.getX();
			mf.y = me.getY();
			mf.repaint();
		}
	}
}