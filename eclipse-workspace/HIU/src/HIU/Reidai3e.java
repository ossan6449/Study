package HIU;
import java.awt.*;
import java.awt.event.*;

public class Reidai3e {
	public static void main(String args[]) {
		MyFrame3e fm = new MyFrame3e("マウスの奇跡");
		
		fm.setSize(300, 150);
		fm.setVisible(true);
	}
}
class MyFrame3e extends Frame {
	int x1, y1, x2 = -1, y2;		// x2 = -1 のときは描画しない
	
	MyFrame3e(String title){
		super(title);
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
		addMouseListener(new MouseAdapter() {
			public void mousePressed(MouseEvent e) {
				x1 = e.getX();
				y1 = e.getY();
				repaint();
			}
			public void mouseReleased(MouseEvent e) {
				x2 = -1;
			}
		});
		
		addMouseMotionListener(new MouseMotionAdapter(){
			public void mouseDragged(MouseEvent e) {
				x2 = e.getX();
				y2 = e.getY();
				mypaint();
				x1 = x2; y1 = y2;
			}
		});
	}
	
	public void mypaint() {				// 独自のメソッドで描画
		Graphics mg = getGraphics();	// Graphicsオブジェクトを取得
		if (x2 != -1) {
			mg.drawLine(x1, y1, x2, y2); // 奇跡の描画
		}
	}
}