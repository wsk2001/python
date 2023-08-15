import java.io.*;
import java.net.*;

public class UDP_Server {
    public static void main(String[] args) {
        DatagramSocket socket = null;
        try {
            socket = new DatagramSocket(20001);
            byte[] receiveData = new byte[1024];

            System.out.println("UDP server up and listening");

            while (true) {
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                socket.receive(receivePacket);
                
                String message = new String(receivePacket.getData(), 0, receivePacket.getLength());
                InetAddress clientAddress = receivePacket.getAddress();

                System.out.println("Message from Client: " + message);
                System.out.println("Client IP Address: " + clientAddress.getHostAddress());
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
        }
    }
}
