<?php
session_start(); 

$userProfileImage = 'profile.png'; 
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PeakBot - About Us</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to bottom, #003366, #004d66, #006655, #007766);
            color: #ffffff;
            overflow: hidden;
            background-size: cover;
            background-repeat: no-repeat;
            min-height: 100vh;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background-color: transparent;
            height: 130px;
            z-index: 1;
        }

        .logo img {
            height: 130px;
            width: auto;
        }

        .nav-container {
            flex-grow: 1;
            display: flex;
            justify-content: center;
            overflow-x: auto;
            white-space: nowrap;
        }

        .nav-links {
            list-style: none;
            display: flex;
            align-items: center;
        }

        .nav-links li {
            margin: 0 15px;
        }

        .nav-links a {
            color: #FFFFFF;
            text-decoration: none;
            font-size: 18px;
            transition: background 0.4s ease, color 0.3s ease;
            padding: 10px 15px;
            border-radius: 10px;
            display: inline-block;
        }

        .nav-links a:hover {
            background: linear-gradient(45deg, #00CFFF, #76C76D);
            color: #000000;
        }

        .content {
            width: 1200px;
            height: auto;
            margin: auto;
            color: #fff;
            position: relative;
            padding: 20px;
            text-align: left;
        }
		 .profile-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: #00CFFF;
            margin-left: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }

        .profile-icon img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 50%;
        }

        .profile-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .profile-modal-content {
            background: #1A1A1A;
            padding: 30px;
            border-radius: 20px;
            width: 400px;
            text-align: center;
            position: relative;
            color: #FFFFFF;
        }

        .profile-modal-content input {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
        }

        .close-profile {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 20px;
            color: white;
        }
        .content h1 {
            font-family: 'Times New Roman';
            font-size: 50px;
            margin-top: 20px;
            letter-spacing: 2px;
        }

        .content p {
            font-family: 'Times New Roman';
            font-size: 24px;
            line-height: 1.6;
            padding: 20px 0;
        }

        footer {
            background-color: #343a40;
            color: white;
            text-align: center;
            padding: 15px 0;
            position: absolute;
            bottom: 0;
            width: 100%;
        }
		.login-button,
        .signup-button,
        .logout-button {
            background: linear-gradient(45deg, #00CFFF, #76C76D);
            border: none;
            border-radius: 30px;
            padding: 12px 30px;
            cursor: pointer;
            font-weight: 600;
            color: #000000;
            transition: background-color 0.3s;
            font-size: 16px;
            margin-left: 10px;
        }

        .login-button:hover,
        .signup-button:hover,
        .logout-button:hover {
            background: linear-gradient(45deg, #00A3B2, #5FAF5D);
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">
            <img src="PeakBot_logo.png" alt="PeakBot Logo">
        </div>

        <div class="nav-container">
            <nav>
                <ul class="nav-links">
                    <li><a href="music.php">Home</a></li>
                    <li><a href="about.php">About</a></li>
                    <li><a href="run_flask.php">Chat</a></li>
                    <li><a href="javascript:void(0)" onclick="openFeedbackForm()">Feedback</a></li>
                </ul>
            </nav>
        </div>

        <div class="auth-buttons">
            <?php if (isset($_SESSION['username'])): ?>
                <div class="profile-icon" onclick="openProfileModal()">
                    <img src="<?php echo htmlspecialchars($userProfileImage); ?>" alt="Profile">
                </div>
            <?php else: ?>
                <button class="signup-button" onclick="window.location.href='signup.php'">Sign Up</button>
                <button class="login-button" onclick="window.location.href='login.php'">Login</button>
            <?php endif; ?>
        </div>
    </header>

    <div class="content">
        <h1>About PeakBot</h1>
        <p>Welcome to PeakBot, your ultimate music companion! At PeakBot, we are dedicated to enhancing your music experience through advanced technology and user-friendly interfaces.</p>
        <p>Our platform leverages AI to provide personalized music recommendations, sentiment analysis, and engaging conversations, ensuring you always find the right tune for your mood.</p>
        <p>Join us as we explore the world of music together, and experience the joy of discovering new sounds, artists, and genres.</p>
    </div>

   

    <script>
        function openProfileModal() {
            document.getElementById('profileModal').style.display = 'flex';
        }

        function closeProfileModal() {
            document.getElementById('profileModal').style.display = 'none';
        }

        function openFeedbackForm() {
            document.getElementById('feedbackForm').style.display = 'flex';
        }

        function closeFeedbackForm() {
            document.getElementById('feedbackForm').style.display = 'none';
        }
    </script>
</body>
</html>
