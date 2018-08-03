package HIU;
import java.awt.*;
import java.awt.event.*;

public class Reidai3d {
	public static void main(String args[]) {
		MyFrame3d fm = new MyFrame3d("マウスドラッグ");
		
		fm.setSize(300,150);
		fm.setVisible(true);
	}
}
class MyFrame3d extends Frame {
	int x1 = -1, y1, x2, y2;
	
	MyFrame3d(String title){
		super(title);
		addWindowListener(new WindowAdapter(){
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
		// マウスアダプタを利用
		addMouseListener(new MouseAdapter() {
			public void mousePressed(MouseEvent e) {
				x1 = x2 = e.getX();
				y1 = y2 = e.getY();
				repaint();
			}
		});
		// マウスモーションアダプタを利用
		addMouseMotionListener(new MouseMotionAdapter(){
			public void mouseDragged(MouseEvent e) {
				x2 = e.getX();
				y2 = e.getY();
				repaint();
			}
		});
	}
	public void paint(Graphics g) {
		if(x1 != -1) {
			g.drawLine(x1, y1, x2, y2);
		}
	}	
}