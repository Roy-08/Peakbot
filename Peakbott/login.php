<?php

session_start();

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "user_data";
$conn = new mysqli($servername, $username, $password, $dbname);


if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$errorMessage = '';


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $usernameInput = $_POST['username'];
    $passwordInput = $_POST['password'];

    
    $stmt = $conn->prepare("SELECT password FROM datas WHERE username = ?");
    $stmt->bind_param("s", $usernameInput);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($hashed_password);
        $stmt->fetch();
        
        
        if (password_verify($passwordInput, $hashed_password)) {
           
            $_SESSION['username'] = $usernameInput;                        
            header('Location: music.php');
            exit(); 
        } else {
            $errorMessage = "Invalid username or password.";
        }
    } else {
        $errorMessage = "Invalid username or password.";
    }

    $stmt->close();
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #006064, #00BCD4); 
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
            position: relative;
        }

        
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 50% 50%, rgba(0, 255, 255, 0.1), transparent 70%);
            opacity: 0.6;
            z-index: 0;
        }

        .frame {
            width: 18%;
            background: rgba(0, 0, 0, 0.6); 
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 20px #00CED1, 0 0 40px #00CED1; 
            position: relative;
            z-index: 1;
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        input {
            width: 90%;
            max-width: 400px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            transition: border-color 0.3s;
        }

        input:focus {
            border-color: #00CED1; 
            outline: none;
        }

        .error {
            color: red;
            font-size: 12px;
        }

        button {
            width: 100%;
            max-width: 400px;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background: #00CED1; 
            color: white;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
            transition: background-color 0.3s, box-shadow 0.3s;
        }

        button:hover {
            background: #00BFFF; 
            box-shadow: 0 0 20px #00CED1, 0 0 40px #00CED1; 
        }

        .account-message {
            text-align: center;
            margin-top: 15px;
        }

        .account-message a {
            color: #00CED1;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="frame">
        <form id="login-form" method="POST">
            <h2>Login</h2>
            <input type="text" id="username" name="username" placeholder="Username" required>
            <div class="error" id="username-error"></div>

            <input type="password" id="password" name="password" placeholder="Password" required>
            <div class="error" id="password-error"><?php echo $errorMessage; ?></div>
            
            <button type="submit">Login</button>
            
            <div class="account-message">
                <p>Don't have an account? <a href="signup.php">Sign up</a></p>
            </div>
        </form>
    </div>
</body>
</html>
