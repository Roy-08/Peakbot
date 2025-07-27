<?php
session_start(); 


if (isset($_POST['logout'])) {
    session_unset();
    session_destroy();
    header("Location: music.php"); 
    exit();
}


$userProfileImage = 'profile.png'; 
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PeakBot - Music Platform</title>
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
	.circle-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            margin-top:-380px;
			margin-left: -200px; 
			padding-left: 1px;			
            min-height: 100vh;
        }

        
        .circle {
            width: 150px; 
            height: 150px; 
            background-color: rgba(255, 255, 255, 0.1); 
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px;
            position: relative;
            text-align: center;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
            color: #ffffff;
            font-size: 1.5em; 
            overflow: hidden;
			font-family:'times new roman'; 
			transition: box-shadow 0.3s ease;
        }
		.circle.glow {
			box-shadow: 0 0 30px rgba(0, 255, 255, 1), 0 0 60px rgba(0, 255, 255, 0.7), 0 0 100px rgba(0, 255, 255, 0.5); 
		}
        
        .circle:before {
            content: '';
            position: absolute;
            top: -5px;
            left: -5px;
            right: -5px;
            bottom: -5px;
            border-radius: 50%;
            border: 3px solid #00ffcc; 
            filter: blur(5px);
            z-index: -1;
        }
        #loading {
            display: none; 
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            font-family: Arial, sans-serif;
            color: #fff;
        }

        .cylinder {
            width: 300px;
            height: 600px;
            background: url('lyric.png');
            background-size: cover;
            background-position: center;
            border-radius: 150px;
            position: absolute;
            left: 68%;
            top: 370%;
            transform: translate(-50%, -50%);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            outline: 4px dashed white;
            outline-offset: 10px;
        }

        .small-cylinder {
            width: 200px;
            height: 400px;
            background: url('lyr.jpg');
            background-size: cover;
            background-position: center top;
            border-radius: 100px;
            position: absolute;
            right: calc(10% + 20px);
            top: 380%;
            transform: translate(0, -50%);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            outline: 4px dashed white;
            outline-offset: 10px;
        }

        
        .large-circle {
            width: 90px;
            height: 90px;
            background: url('symbol.png');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            border-radius: 50%;
            position: absolute;
            right: calc(-1% + 100px);
            top: 370%;
            transform: translate(0, -30%);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }

        .content {
            position: relative;
            z-index: 1;
            padding: 20px;
            color: white;
        }
        header {
            display: flex;
			position: relative; 
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background-color: transparent;
            height: 130px;
			z-index:1;
        }

        .logo img {
            height: 130px;
            width: auto;
        }

		.nav-container {
			flex-grow: 1;
			position: relative;
			display: flex;
			justify-content: center;
			overflow-x: auto; 
			white-space: nowrap; 
		}

		.nav-links {
			list-style: none;
			display: flex;
			align-items: center;
			flex-wrap: nowrap; 
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
		.conten{
            width: 1200px;
            height: auto;
            margin: auto;
            color: #fff;
            position: relative;
        }
        .conten{
	        margin-left: 50px; 
	        padding-left: 50px;
	        margin-top: -70px;
	        text-align:left;
        }
        .conten .par{
            padding-left: 20px;
            padding-bottom: 25px;
            font-family: 'Times New Roman';
            letter-spacing: 1.2px;
            line-height: 40px;
        }
        .conten .cn{
            width: 160px;
            height: 40px;
            background: #ff7200;
            border: none;
            margin-bottom: 10px;
            margin-left: 20px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            transition: .4s ease;
        }
        .conten h1{
            font-family: 'Times New Roman';
            font-size: 50px;
            padding-left: 20px;
            margin-top: 9%;
            letter-spacing: 2px;
        }
        .conten span{
            color: cyan;
            font-size: 65px;
        }
		.quote-text {
			margin-top:30px;
			color: #00A3B2;
			margin-left: 20px; 
			padding-left: 1px;
			font-size: 32px; 
			color: white; 
			font-family: 'times new roman',serif; 
			letter-spacing: 1.5px; 
			font-weight: bold;
		}
		.conn{
			color: white;
			margin-top: 30px;
			margin-left: 20px; 
			padding-left: 1px;
			font-size: 32px;
			letter-spacing: 1.5px;
			font-family: 'times new roman',serif;
		}

        .auth-buttons {
            display: flex;
            align-items: center;
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

        footer {
            background-color: #343a40;
            color: white;
            text-align: center;
            padding: 15px 0;
            position: absolute;
            bottom: 0;
            width: 100%;
        }

        
        .feedback-form {
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

        .feedback-form-content {
            background: #1A1A1A;
            padding: 30px;
            border-radius: 20px;
            width: 400px;
            text-align: center;
            position: relative;
            color: #FFFFFF;
        }

        .feedback-form-content input,
        .feedback-form-content textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
        }

        .close-feedback {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 20px;
            color: white;
        }
		.content h2 {
            font-family: 'times new roman'; 
            color: #FFFFE0;
            font-size: 2.5em;
            margin-top: 65px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            position: relative;
            text-align: center;
        }
		.start{
			font-family:'times new roman';
			margin-top:-350px;
			margin-left: 20px; 
			font-size:24px;
			
		}
		.start h2 strong{
			animation: blink-animation 1.5s infinite;
		}
		@keyframes blink-animation {
            0% { color: cyan; opacity: 1; }   /* Red at 0% */
            25% { color:white; opacity: 0.7; }  /* Blue at 25% */
            50% { color: cyan; opacity: 1; }  /* Green at 50% */
            75% { color: white; opacity: 0.7; } /* Yellow at 75% */
            100% { color: white; opacity: 1; }  /* Back to red at 100% */
    }
        
    </style>
</head>
<body>
	
    <header>
        <div class="logo">
            <img src="PeakBot_logo.png" alt="PeakBot Logo">
        </div>
		
		 <div class="cylinder"></div>


    <div class="small-cylinder"></div>
	
    <div class="large-circle"></div>
        <div class="nav-container">
            <nav>
                <ul class="nav-links">
                    <li><a href="music.php">Home</a></li>
                    <li><a href="about.php">About</a></li>
                    <li><a href="run_flask.php" id="chatButton">Chat</a></li>
                    <li><a href="javascript:void(0)" onclick="openFeedbackForm()">Feedback</a></li>
                </ul>
            </nav>
        </div>
		<div id="loading">Loading chatbot...</div>

    <script>
        document.getElementById('chatButton').addEventListener('click', function (e) {
            e.preventDefault(); 

            
            document.getElementById('loading').style.display = 'block';

            setTimeout(function () {
                window.location.href = 'run_flask.php';
            }, 500); 
        });
    </script>
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

    
    <div class="profile-modal" id="profileModal">
        <div class="profile-modal-content">
            <span class="close-profile" onclick="closeProfileModal()">&times;</span>
            <h2>Profile</h2>
            <p>Welcome, <?php echo isset($_SESSION['username']) ? htmlspecialchars($_SESSION['username']) : 'User'; ?>!</p>
            <form method="post" action="">
                <button type="submit" name="logout" class="logout-button">Logout</button>
            </form>
        </div>
    </div>

    
    <div class="feedback-form" id="feedbackForm">
        <div class="feedback-form-content">
            <span class="close-feedback" onclick="closeFeedbackForm()">&times;</span>
            <h2>Feedback</h2>
            <form method="POST">
                <input type="text" name="name" placeholder="Your Name" required>
                <input type="email" name="email" placeholder="Your Email" required>
                <textarea name="feedback" rows="4" placeholder="Your Feedback" required></textarea>
                <button type="submit" class="login-button">Submit Feedback</button>
            </form>
        </div>
    </div>
<?php
$conn = new mysqli("localhost", "root", "", "user_data");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    
    if (isset($_POST['name']) && isset($_POST['email']) && isset($_POST['feedback'])) {
       
        $name = $conn->real_escape_string($_POST['name']);
        $email = $conn->real_escape_string($_POST['email']);
        $feedback = $conn->real_escape_string($_POST['feedback']);

        
        $sql = "INSERT INTO feedback (name, email, feedback) VALUES ('$name', '$email', '$feedback')";

        if ($conn->query($sql) === TRUE) {
            
            echo "<script>alert('Thank you for your feedback!');</script>";
            } else {
            echo "<script>alert('Error: " . $conn->error . "');</script>";
        }
    } else {
        echo "<script>alert('Error: Missing form fields!');</script>";
    }
}


$conn->close();
?>



	
<div class="conten">
            <h1>Welcome to <br><span>PeakBot</span> The Music World</h1>
        <div>

<p class='conn'>
            At PeakBot, we believe that conversations should be engaging,<br>
			insightful, and fun! Our advanced chatbot is designed to help<br>
			you explore various topics, get instant responses, and provide<br>
			you with a delightful interaction experience.
        </p>	
		
     <h2 class='content'style="font-family:'times new roman';font-size:28px">Why Choose PeakBot?</h2>
        <div class="circle-container">
            <div class="circle">24/7 Availability</div>
            <div class="circle">User-Friendly Interface</div>
            <div class="circle">Sentiment Detection</div>
            <div class="circle">Music Recommend</div>
            <div class="circle">Feedback Integration</div>
        </div>
      <div class='start'>
	  
	  <h2><strong> Click the chat button and start your conversation.</strong></h2>
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
