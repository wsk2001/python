import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;

public class ReqXfcPolicy {

	public static String ReqPolicy(InputStream is, OutputStream os, String c_policy_type, String c_ip, String c_policy)
	{
		String sRes = null;

        byte[] bytes = null;
        String message = null;

        try {
	        message = "{ \"policyType\": \"" + c_policy_type + "\", " +
	        		  "\"ip\": \"" + c_ip + "\", " +
	        		  "\"policy\": \"" + c_policy + "\" }";
	        		
	        bytes = message.getBytes();
	        os.write(bytes);
	        os.flush();
	       
			Thread.sleep(10);
	        bytes = new byte[4096];
	        int readByteCount = is.read(bytes);
	
	        sRes = new String(bytes,0,readByteCount,"UTF-8");
	       
        } catch (Exception e) {
            e.printStackTrace();
        }
        
		return sRes;
	}
	
		
	public static String ReqAPiPolicy(InputStream is, OutputStream os, String c_ip, String c_policy)
	{
		return ReqPolicy(is, os, "api_policy", c_ip, c_policy);
	}

	public static String ReqLaPolicy(InputStream is, OutputStream os, String c_ip, String c_policy)
	{
		return ReqPolicy(is, os, "la_policy", c_ip, c_policy);
	}

	public static String ReqSaPolicy(InputStream is, OutputStream os, String c_ip, String c_policy)
	{
		return ReqPolicy(is, os, "sa_policy", c_ip, c_policy);
	}
	
	
    public static void main(String[] args) {

        Socket  socket      = null;
    	String 	server_ip   = "localhost";
    	int		server_port = 9999;
        
        try {
        	if(socket == null)
        		socket = new Socket();
        	
            System.out.println("[Request Connect]");

            socket.connect(new InetSocketAddress(server_ip, server_port));
	        OutputStream os = socket.getOutputStream();
	        InputStream is = socket.getInputStream();

	        System.out.println("[Success Connect]");
            
            String msg = null;
            msg = ReqAPiPolicy(is, os, "192.168.60.190", null);
            if(msg != null)
            	System.out.println("[Received API policy]: " + msg);
            Thread.sleep(2000);
            
            msg = ReqLaPolicy(is, os, "192.168.60.190", "LA001");
            if(msg != null)
            	System.out.println("[Received Local Agent policy]: " + msg);
            Thread.sleep(2000);

            msg = ReqSaPolicy(is, os, "192.168.60.190", "SAwin002");
            if(msg != null)
            	System.out.println("[Received Schedule Agent policy]: " + msg);
            Thread.sleep(2000);
            
            is.close();
            os.close();
            
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