import java.io.FileInputStream;
import java.security.MessageDigest;

public class Hasher {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: java Hasher <file_path>");
            System.exit(1);
        }

        String filePath = args[0];
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            FileInputStream fis = new FileInputStream(filePath);

            byte[] byteArray = new byte[1024];
            int bytesCount;
            while ((bytesCount = fis.read(byteArray)) != -1) {
                digest.update(byteArray, 0, bytesCount);
            }
            fis.close();

            byte[] bytes = digest.digest();

            // Convert to hex string
            StringBuilder sb = new StringBuilder();
            for (byte b : bytes) {
                sb.append(String.format("%02x", b));
            }
            System.out.println(sb.toString());

        } catch (Exception e) {
            System.err.println("Error hashing file: " + e.getMessage());
        }
    }
}
