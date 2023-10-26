<?php 
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rejestracja</title>
    <link rel="stylesheet" href="rejestracja_css.css">
</head>
<body>
    <header class="header">
<div class="szaszki">
    <br><br><br><br>
<h1>SZASZKI.COM</h1>
</div>
<div class="logowanie">
    <p id="zawartosc">
        <form action="rejestracja.php" method="post">
login: <input type="text" name="login" value="<?php 
if(isset($_SESSION['zapamietaj_login']))
{
    echo $_SESSION['zapamietaj_login'];
    unset($_SESSION['zapamietaj_login']);
}
?>"><br><br>
<?php
if(isset($_SESSION['e_login']))
echo $_SESSION['e_login'];
unset($_SESSION['e_login']);
?>
email: <input type="text" name="email" value="<?php
if(isset($_SESSION['zapamietaj_email']))
{
    echo $_SESSION['zapamietaj_email'];
    unset($_SESSION['zapamietaj_email']);
}
?>"><br><br>
<?php
if(isset($_SESSION['e_email']))
echo $_SESSION['e_email'];
unset($_SESSION['e_email']);
?>
hasło: <input type="password" name="haslo" value="<?php
if(isset($_SESSION['zapamietaj_haslo1']))
{
    echo $_SESSION['zapamietaj_haslo1'];
    unset($_SESSION['zapamietaj_haslo1']);
}
?>"><br><br>
powtórz hasło: <input type="password" name="haslo_powtorz" value="<?php
if(isset($_SESSION['zapamietaj_haslo2']))
{
    echo $_SESSION['zapamietaj_haslo2'];
    unset($_SESSION['zapamietaj_haslo2']);
}
?>"><br><br>
<?php
if(isset($_SESSION['e_haslo']))
echo $_SESSION['e_haslo'];
unset($_SESSION['e_haslo']);
?>
<br><input type="submit" value="Utwórz konto" name="loguj" class="przycisk"><br><br>
</form>
    <form action="do_logowania.php" method="post">
    <input type="submit" value="Logowanie" name="loguj" class="przycisk">
    </form>

    </p>
</div>
</header>
</body>
</html>