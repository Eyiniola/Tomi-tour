<?php
session_start();

header('Content-Type: application/json');

$response = [
    'username' => isset($_SESSION['username']) ? $_SESSION['username'] : '',
    'email' => isset($_SESSION['email']) ? $_SESSION['email'] : '',
    'phone' => isset($_SESSION['phone']) ? $_SESSION['phone'] : '',
    'date_of_birth' => isset($_SESSION['date_of_birth']) ? $_SESSION['date_of_birth'] : '',
    'name' => isset($_SESSION['name']) ? $_SESSION['name'] : ''
];

echo json_encode($response);
?>