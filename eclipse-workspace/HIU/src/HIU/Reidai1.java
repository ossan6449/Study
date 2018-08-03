package HIU;
import java.awt.*;
import java.awt.event.*;

public class Reidai1 {
	public static void main(String args[]) {
		MyFrame1 fm = new MyFrame1("フレームテスト");
			// フレームオブジェクトを生成する
		fm.setSize(200, 150);	// 窓（ウィンドウ）サイズを横200,縦150にする
		fm.setVisible(true);	// フレーム（ウィンドウ）を表示する
	//	fm.show();
	}		
}

class MyFrame1 extends Frame { // Fream を継承したMyFream1 クラスを定義
	MyFrame1(String title){
		super(title);	// フレームのタイトルを設定する
		addWindowListener(new WindowAdapter(){
			public void windowClosing(WindowEvent e){
				System.exit(0);
			}
		});
	}
	
	public void paint(Graphics g) {
		g.drawString("最初のフレームテストです", 30, 60);
	}
}