<?php 
session_start();

if(!isset($_SESSION['udana_rejestracja']))
{
    header('location: index.php');
    exit();
}
else
{
    unset($_SESSION['udana_rejestracja']);
}

if(isset($_SESSION['zapamietaj_login'])) unset($_SESSION['zapamietaj_login']);
if(isset($_SESSION['zapamietaj_email'])) unset($_SESSION['zapamietaj_email']);
if(isset($_SESSION['zapamietaj_haslo1'])) unset($_SESSION['zapamietaj_haslo1']);
if(isset($_SESSION['zapamietaj_haslo2'])) unset($_SESSION['zapamietaj_haslo2']);

if(isset($_SESSION['e_login'])) unset($_SESSION['e_login']);
if(isset($_SESSION['e_email'])) unset($_SESSION['e_email']);
if(isset($_SESSION['e_haslo'])) unset($_SESSION['e_haslo']);

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logowanie</title>
    <link rel="stylesheet" href="witamy.css">
</head>
<body>
    <header class="header">
<div class="szaszki">
    <br><br><br><br><br><br>
<h1>SZASZKI.COM</h1>
</div>
<div class="logowanie">
    <p id="zawartosc">
    Dziękujemy za utworzenie konta!<br><br><br><br><br>
    <form action="do_logowania.php" method="post">
    <input type="submit" value="Logowanie" name="loguj" class="przycisk">
    </form>
    </p>
</div>
</header>
</body>
</html>