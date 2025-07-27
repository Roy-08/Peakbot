<?php
// Database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "user_data";
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$emailError = '';
$usernameError = '';
$passwordError = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $username = $_POST['username'];
    $password = $_POST['password'];

    if (strlen($username) < 6) {
        $usernameError = "Username must be at least 6 characters long.";
    } elseif (!preg_match('/[A-Z]/', $username)) {
        $usernameError = "Username must contain at least one uppercase letter.";
    } elseif (!preg_match('/\d/', $username)) {
        $usernameError = "Username must contain at least one number.";
    } elseif (!preg_match('/[!@#$%^&*]/', $username)) {
        $usernameError = "Username must contain at least one special character.";
    }

    if (strlen($password) < 6) {
        $passwordError = "Password must be at least 6 characters long.";
    }

    if (empty($usernameError) && empty($passwordError)) {
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        $stmt = $conn->prepare("INSERT INTO datas (email, username, password) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $email, $username, $hashed_password);

        if ($stmt->execute()) {
            echo json_encode(["status" => "success", "message" => "Sign up successful!"]);
        } else {
            echo json_encode(["status" => "error", "message" => "Error: " . $stmt->error]);
        }

        $stmt->close();
        exit;
    } else {
        echo json_encode(["status" => "error", "message" => "Validation failed.", "errors" => compact('usernameError', 'passwordError')]);
        exit;
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <style>
        body {
            font-family: Arial, sans-serif;
             background: linear-gradient(to bottom, #006064, #00BCD4); /* Dark to cyan gradient */
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

        form {
            max-width: 500px;
            background: rgba(0, 0, 0, 0.6); 
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 20px #00CED1, 0 0 40px #00CED1; 
            position: relative;
            transition: height 0.3s ease;
            height: 420px;
            z-index: 1;
        }

        h2 {
            text-align: center;
        }

        input {
            width: 90%;
            height: 20px;
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

        .requirement {
            display: none;
            align-items: center;
            margin: 5px 0;
        }

        .custom-checkbox {
            width: 15px;
            height: 15px;
            background: grey;
            margin-right: 10px;
        }

        .custom-checkbox.checked {
            background: #00FF7F; 
        }

        .requirement-instruction {
            color: white;
            font-size: 14px;
            margin: 0;
        }

        button {
            width: 100%;
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
    <form id="signup-form">
        <h2>Sign Up</h2>
        <input type="email" name="email" placeholder="Email" required>
        <input type="text" id="username" name="username" placeholder="Username" required>
        <div class="error" id="username-error"></div>

        <div class="requirement" id="length-check">
            <div class="custom-checkbox" id="length-checkbox"></div>
            <p class="requirement-instruction">At least 6 characters</p>
        </div>
        <div class="requirement" id="uppercase-check">
            <div class="custom-checkbox" id="uppercase-checkbox"></div>
            <p class="requirement-instruction">At least one uppercase letter</p>
        </div>
        <div class="requirement" id="number-check">
            <div class="custom-checkbox" id="number-checkbox"></div>
            <p class="requirement-instruction">At least one number</p>
        </div>
        <div class="requirement" id="special-check">
            <div class="custom-checkbox" id="special-checkbox"></div>
            <p class="requirement-instruction">At least one special character</p>
        </div>

        <input type="password" id="signup-password" name="password" placeholder="Password" required>
        <div class="error" id="password-error"></div>
        <input type="password" id="confirm-password" name="confirm_password" placeholder="Confirm Password" required>

        <button type="submit" name="sign_up">Sign Up</button>

        <div class="account-message">
            <p>Already have an account? <a href="login.php">Log in</a></p>
        </div>
    </form>

    <script>
        const usernameInput = document.getElementById('username');
        const form = document.getElementById('signup-form');
        const lengthCheck = document.getElementById('length-check');
        const uppercaseCheck = document.getElementById('uppercase-check');
        const numberCheck = document.getElementById('number-check');
        const specialCheck = document.getElementById('special-check');

        // Show username validation requirements
        usernameInput.addEventListener('input', function() {
            const username = usernameInput.value;

            if (username) {
                lengthCheck.style.display = 'flex';
                uppercaseCheck.style.display = 'flex';
                numberCheck.style.display = 'flex';
                specialCheck.style.display = 'flex';
                form.style.height = '520px';
            } else {
                lengthCheck.style.display = 'none';
                uppercaseCheck.style.display = 'none';
                numberCheck.style.display = 'none';
                specialCheck.style.display = 'none';
                form.style.height = '420px';
            }

            
            if (username.length >= 6) {
                document.getElementById('length-checkbox').classList.add('checked');
            } else {
                document.getElementById('length-checkbox').classList.remove('checked');
            }

            
            if (/[A-Z]/.test(username)) {
                document.getElementById('uppercase-checkbox').classList.add('checked');
            } else {
                document.getElementById('uppercase-checkbox').classList.remove('checked');
            }

           
            if (/\d/.test(username)) {
                document.getElementById('number-checkbox').classList.add('checked');
            } else {
                document.getElementById('number-checkbox').classList.remove('checked');
            }

            
            if (/[!@#$%^&*]/.test(username)) {
                document.getElementById('special-checkbox').classList.add('checked');
            } else {
                document.getElementById('special-checkbox').classList.remove('checked');
            }
        });

       
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);

            fetch('', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                    window.location.href = 'login.php'; 
                } else {
                    document.getElementById('username-error').innerText = data.errors.usernameError || '';
                    document.getElementById('password-error').innerText = data.errors.passwordError || '';
                }
            });
        });
    </script>
</body>
</html>
