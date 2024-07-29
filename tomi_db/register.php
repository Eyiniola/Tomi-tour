<?php
session_start();

header('Content-Type: application/json');

// Include the database connection file
require 'db.php';


// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get and sanitize form data
    $name = $conn->real_escape_string($_POST['name']);
    $email = $conn->real_escape_string($_POST['email']);
    $phone = $conn->real_escape_string($_POST['phone']);
    $date_of_birth = $conn->real_escape_string($_POST['date-of-birth']);
    $username = $conn->real_escape_string($_POST['username']);
    $password = $conn->real_escape_string($_POST['password']);
    
    // Validate required fields
    if (empty($name) || empty($email) || empty($phone) || empty($date_of_birth) || empty($username) || empty($password)) {
        echo "All fields are required.";
        exit();
    }

    // Check if email or username already exists
    $stmt = $conn->prepare("SELECT id FROM user WHERE email = ? OR username = ?");
    $stmt->bind_param("ss", $email, $username);
    $stmt->execute();
    $stmt->store_result();
    
    if ($stmt->num_rows > 0) {
        echo "Email or Username already exists.";
        $stmt->close();
        $conn->close();
        exit();
    }
    $stmt->close();

    // Hash the password
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Prepare and execute the insert query
    $stmt = $conn->prepare("INSERT INTO user (name, email, phone, date_of_birth, username, password) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssss", $name, $email, $phone, $date_of_birth, $username, $hashed_password);

    if ($stmt->execute()) {
        // Set session variables if needed
        $_SESSION['username'] = $username;
        $_SESSION['email'] = $email;

        // Redirect to home.html
        header('Location: ../home.html');
        exit();
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
    $conn->close();
} else {
    // If not a POST request
    http_response_code(405); // Method Not Allowed
    echo "Method not allowed.";
}
?>
