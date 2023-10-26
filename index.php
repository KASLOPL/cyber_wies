<?php 
session_start();

if(isset($_SESSION['zalogowany']) && ($_SESSION['zalogowany']==true))
{
    header('location: lobby.php');
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logowanie</title>
    <link rel="stylesheet" href="logowanie_css.css">
</head>
<body>
    <header class="header">
<div class="szaszki">
    <br><br><br><br><br><br>
<h1>SZASZKI.COM</h1>
</div>
<div class="logowanie">
    <p id="zawartosc">
        <form action="logowanie.php" method="post">
login: <input type="text" name="login"><br><br>
hasło: <input type="password" name="haslo" id="haslo"><br><br>
<?php
if(isset($_SESSION['zle_dane']))
echo $_SESSION['zle_dane'];
unset($_SESSION['zle_dane']);
?>
<input type="submit" value="Zaloguj się" name="loguj" class="przycisk"><br><br>
</form>
<form action="do_rejestracji.php" method="post">
<input type="submit" value="Zarejestruj się" name="rejestracja" class="przycisk">
</form>
    </p>
</div>
</header>
</body>
</html>