import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    private static final String SERVER_ADDRESS = "localhost";
    private static final int PORT = 12345;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("\nChoose an option:");
            System.out.println("1. Submit Preference Form");
            System.out.println("2. Check Allocation Status");
            System.out.println("3. View Available Seats");
            System.out.println("4. Exit");

            String choice = scanner.nextLine();

            switch (choice) {
                case "1":
                    submitPreferenceForm(scanner);
                    break;
                case "2":
                    checkAllocationStatus(scanner);
                    break;
                case "3":
                    viewAvailableSeats();
                    break;
                case "4":
                    System.out.println("Exiting the program.");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid choice. Please select a valid option.");
            }
        }
    }

    private static void submitPreferenceForm(Scanner scanner) {
        try (Socket socket = new Socket(SERVER_ADDRESS, PORT);
             ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
             ObjectInputStream in = new ObjectInputStream(socket.getInputStream())) {

            // Send request type
            out.writeObject("SUBMIT_FORM");

            // Get student ID
            System.out.print("Enter Student ID: ");
            String studentId = scanner.nextLine();

            // Get preferences
            System.out.print("Enter 3 preferred courses (separated by comma): ");
            String[] preferences = scanner.nextLine().split(",");

            // Send student ID and preferences
            out.writeObject(studentId);
            out.writeObject(preferences);

            System.out.println("Preference form submitted successfully.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void checkAllocationStatus(Scanner scanner) {
        try (Socket socket = new Socket(SERVER_ADDRESS, PORT);
             ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
             ObjectInputStream in = new ObjectInputStream(socket.getInputStream())) {

            // Send request type
            out.writeObject("CHECK_STATUS");

            // Get student ID
            System.out.print("Enter Student ID: ");
            String studentId = scanner.nextLine();

            // Send student ID
            out.writeObject(studentId);

            // Receive and print allocation status
            String status = (String) in.readObject();
            System.out.println("Allocation status: " + status);
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    private static void viewAvailableSeats() {
        try (Socket socket = new Socket(SERVER_ADDRESS, PORT);
             ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
             ObjectInputStream in = new ObjectInputStream(socket.getInputStream())) {

            // Send request type
            out.writeObject("VIEW_SEATS");

            // Receive and print available seats
            String seatsInfo = (String) in.readObject();
            System.out.println("Available Seats per Course:");
            System.out.println(seatsInfo);
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
