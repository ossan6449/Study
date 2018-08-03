package HIU;
import java.awt.*;
import java.awt.event.*;

public class Reidai3c {
	public static void main(String args[]) {
		MyFrame3c fm = new MyFrame3c("マウスドラッグ");
		
		fm.setSize(300,150);
		fm.setVisible(true);
	}
}
// MouseListenerと MouseMotionListenerの2つのインターフェースを実装
class MyFrame3c extends Frame implements MouseListener, MouseMotionListener{
	int x1 = -1, y1, x2, y2;	// x1 = -1 のときは描画しない
	
	MyFrame3c(String title){
		super(title);
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
		addMouseListener(this);			// マウスリスナを登録
		addMouseMotionListener(this);	// マウスモーションリスナを登録
	}
	
	public void paint(Graphics g) {
		if(x1 != -1) {
			g.drawLine(x1, y1, x2, y2);
		}
	}
	// 使わないメソッド
	public void mouseEntered(MouseEvent e) {}
	public void mouseExited(MouseEvent e) {}
	public void mouseClicked(MouseEvent e) {}
	public void mouseReleased(MouseEvent e) {}
	
	public void mousePressed(MouseEvent e) {	// マウスを押したときの処理
		x1 = x2 = e.getX();		// 直線の視点を設定
		y1 = y2 =e.getY();
		repaint();				// 描画
	}
	
	public void mouseDragged(MouseEvent e) {	// ドラッグ処理
		x2 = e.getX();			// 直線の終点を設定
		y2 = e.getY();
		repaint();
	}
	
	public void mouseMoved(MouseEvent me) {}	// 使わないメソッド
	
}