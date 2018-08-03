package HIU;
import java.awt.*;
import java.awt.event.*;

public class Reidai3 {
	public static void main(String args[]) {
		MyFrame3 fm = new MyFrame3("マウスイベント処理");
		
		fm.setSize(300,150);
		fm.setVisible(true);	
	}
}

// MouseListener インタフェースを実装
class MyFrame3 extends Frame implements MouseListener {
	String s1 = "", s2 = "";
	int x = -1, y;
	
	MyFrame3(String title){
		super(title);
		addWindowListener(new WindowAdapter(){
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
		addMouseListener(this);			// マウスリスナを登録
	}
	public void paint(Graphics g) {
		g.drawString(s1,10,50);			// 文字列s1を表示
		g.drawString(s2,10,60);			// 文字列s2を表示
		if(x != -1) {
			g.drawLine(x-10,y,x+10,y);	// +マークを描画
			g.drawLine(x,y-10,x,y+10);
		}
	}
	public void mouseEntered(MouseEvent me) { 	// 領域に入った
		s1 = "mouseEntered";					// 識別文字列を設定
		repaint();								// 再描画
	}
	public void mouseExited(MouseEvent me) {	// 領域から出た
		s1 = "mouseExited";
		repaint();
	}
	public void mouseClicked(MouseEvent me) {	// マウスをクリックした
		x = me.getX();							// クリックしたx位置を取得
		y = me.getY();							// クリックしたy位置を取得
		repaint();
	}
	public void mousePressed(MouseEvent me) {	// マウスを押した
		s2 = "mousePressed";
		repaint();
	}
	public void mouseReleased(MouseEvent me) {	// マウスを離した
		s2 = "mouseReleased";
		repaint();
	}
}
