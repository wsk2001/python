import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;

public class GetXfcApiPolicy {

    public static void main(String[] args) {

        Socket socket = null;

        try {
            socket = new Socket();
            System.out.println("[Request Connect]");
            socket.connect(new InetSocketAddress("localhost", 9999));
            System.out.println("[Success Connect]");
           
            byte[] bytes = null;
            String message = null;

            OutputStream os = socket.getOutputStream();
            message = "192.168.90.190";
            //bytes = message.getBytes("UTF-8");
            bytes = message.getBytes();
            os.write(bytes);
            os.flush();
            System.out.println("[Success Data Send]");
           
			Thread.sleep(1000);
            InputStream is = socket.getInputStream();
            bytes = new byte[4096];
            int readByteCount = is.read(bytes);
			System.out.println("readByteCount: " + Integer.toString(readByteCount));

            message = new String(bytes,0,readByteCount,"UTF-8");
            System.out.println("[Success Receive Data] " + message);
           
            os.close();
            is.close();
           
        } catch (Exception e) {
            e.printStackTrace();
        }
       
        if (!socket.isClosed()) {
            try {
                socket.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }

}