import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

public class CourseManager {
    private Map<String, String[]> coursePreferences;
    private Map<String, String> courseAllocation;
    private Map<String, Integer> availableSeats;

    public CourseManager() {
        coursePreferences = new HashMap<>();
        courseAllocation = new HashMap<>();
        availableSeats = new HashMap<>();
        availableSeats.put("Math", 2);
        availableSeats.put("Physics", 2);
        availableSeats.put("Chemistry", 2);
    }

    public void startServer() {
        try (ServerSocket serverSocket = new ServerSocket(12345)) {
            System.out.println("Server is running and waiting for connections...");

            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("Client connected: " + socket);

                new Thread(() -> handleClient(socket)).start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void handleClient(Socket socket) {
        try (ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
             ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream())) {

            String requestType = (String) in.readObject();
            switch (requestType) {
                case "SUBMIT_FORM":
                    String studentId = (String) in.readObject();
                    String[] preferences = (String[]) in.readObject();
                    submitPreferenceForm(studentId, preferences);
                    break;
                case "CHECK_STATUS":
                    studentId = (String) in.readObject();
                    checkAllocationStatus(out, studentId);
                    break;
                case "VIEW_SEATS":
                    viewAvailableSeats(out);
                    break;
                default:
                    System.out.println("Unknown request type: " + requestType);
            }
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    private synchronized void submitPreferenceForm(String studentId, String[] preferences) {
        coursePreferences.put(studentId, preferences);
        System.out.println("Request received from Student ID " + studentId);
        allocateCourses();
    }

    private synchronized void allocateCourses() {
        for (Map.Entry<String, String[]> entry : coursePreferences.entrySet()) {
            String studentId = entry.getKey();
            String[] preferences = entry.getValue();
            boolean allocated = false;
            for (String course : preferences) {
                if (availableSeats.containsKey(course) && availableSeats.get(course) > 0) {
                    courseAllocation.put(studentId, course);
                    availableSeats.put(course, availableSeats.get(course) - 1);
                    System.out.println("Course " + course + " allocated to Student ID " + studentId);
                    allocated = true;
                    break;
                }
            }
            if (!allocated) {
                System.out.println("No available courses for Student ID " + studentId);
            }
        }
        coursePreferences.clear();
    }

    private synchronized void checkAllocationStatus(ObjectOutputStream out, String studentId) throws IOException {
        String status = courseAllocation.get(studentId);
        if (status != null) {
            out.writeObject("Course allocated: " + status);
        } else {
            out.writeObject("No course allocated yet.");
        }
    }

    private synchronized void viewAvailableSeats(ObjectOutputStream out) throws IOException {
        StringBuilder seatsInfo = new StringBuilder();
        for (Map.Entry<String, Integer> entry : availableSeats.entrySet()) {
            seatsInfo.append(entry.getKey()).append(": ").append(entry.getValue()).append(" seats\n");
        }
        out.writeObject(seatsInfo.toString());
    }

    public static void main(String[] args) {
        CourseManager courseManager = new CourseManager();
        courseManager.startServer();
    }
}
