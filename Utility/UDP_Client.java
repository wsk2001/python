import java.io.*;
import java.net.*;

public class UDP_Client {
	// static String log_server_ip = "192.168.60.190";
	static String log_server_ip = "127.0.0.1";
	static int log_server_port = 20001;
	static DatagramSocket socket = null;

	private static void send_server(String msg)
	{
        try {
            socket = new DatagramSocket();
            InetAddress serverAddress = InetAddress.getByName(log_server_ip);

            byte[] sendData = msg.getBytes();

            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, serverAddress, log_server_port);
            socket.send(sendPacket);

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
        }
	}

    public static void main(String[] args) {       

		String user_name = "wonsool";
		String client_ip = "192.168.60.190";
		String os_name = "Windows 10";
		String client_type = "API";
		String mode = "E";
		String dt = "2023-08-03 12:33:48.361";
		String strFileName = "/home/wonsool/IQFile/test/enc/data07/data_5128.txt";
		String fileSize = "127736";
		String hashcode = "6887e03db9e82b5fcd749c279f282817aa357367a990b3a8bb98cdec449669c5";
		String duration = "0.004";
		String status = "Success";

		String msg = "[{";
		msg += "\"userId\":\"" + user_name + "\"";  
		msg += ",\"accIp\":\"" + client_ip + "\"";  
		msg += ",\"enpIp\":\"" + client_ip + "\"";  
		msg += ",\"agtEnpPlatform\":\"" + os_name + "\"";  
		msg += ",\"agtType\":\"" + client_type + "\"";  
		msg += ",\"jobOperation\":\"" + mode + "\"";  
		msg += ",\"agtDate\":\"" + dt + "\"";  
		msg += ",\"agtFilename\":\"" + strFileName + "\"";  
		msg += ",\"agtFilesize\":" + fileSize;  
		msg += ",\"agtFilehash\":\"" + hashcode + "\"";  
		msg += ",\"agtDuration\":" + duration;  
		msg += ",\"agtResult\":\"" + status + "\"";                  
		msg += "}]";

		send_server(msg);
    }
}