<?php
session_start();

if(isset($_POST['email']) && isset($_POST['login']) && isset($_POST['haslo']) && isset($_POST['haslo_powtorz']))
{
    $walidacja = true;

    $login = $_POST['login'];
    if(3>strlen($login) || strlen($login)>20)
    {
        $walidacja = false;
        $_SESSION['e_login']='<p style="color: red; font-size: 20px;">login musi posiadać od 3 do 20 znaków</p>';
    }
    if(ctype_alnum($login) == false)
    {
        $walidacja = false;
        $_SESSION['e_login']='<p style="color: red; font-size: 20px;">login może się składać tylko z liter i cyfr</p>';
    }
    if($login == "")
    {
        $walidacja = false;
        $_SESSION['e_login']='<p style="color: red; font-size: 20px;">login nie może być pusty</p>';
    }

    $email = $_POST['email'];
    $email_dobry = filter_var($email, FILTER_SANITIZE_EMAIL);
    
    if((filter_var($email_dobry, FILTER_SANITIZE_EMAIL) == false) || ($email_dobry!=$email))
    {
        $walidacja = false;
        $_SESSION['e_email']='<p style="color: red; font-size: 20px;">email nie poprawny</p>';
    }
    if($email == "")
    {
        $walidacja = false;
        $_SESSION['e_email']='<p style="color: red; font-size: 20px;">email nie może być pusty</p>';
    }

    $haslo1 = $_POST['haslo'];
    $haslo2 = $_POST['haslo_powtorz'];

    if(strlen($haslo1)<8 || strlen($haslo2)>20)
    {
        $walidacja = false;
        $_SESSION['e_haslo']='<p style="color: red; font-size: 20px;">hasło musi posiadać od 8 do 20 znaków</p>';
    }
    if($haslo1 != $haslo2)
    {
        $walidacja = false;
        $_SESSION['e_haslo']='<p style="color: red; font-size: 20px;">oba hasła muszą być takie same</p>';
    }
    if($haslo1 == "")
    {
        $walidacja = false;
        $_SESSION['e_haslo']='<p style="color: red; font-size: 20px;">hasło nie może być puste</p>';
    }
    $haslo_hash = password_hash($haslo1, PASSWORD_DEFAULT);

    $_SESSION['zapamietaj_login'] = $login;
    $_SESSION['zapamietaj_email'] = $email;
    $_SESSION['zapamietaj_haslo1'] = $haslo1;
    $_SESSION['zapamietaj_haslo2'] = $haslo2;


    require_once "connect.php";
    mysqli_report(MYSQLI_REPORT_STRICT);

    try
    {
        $baza = new mysqli($host, $db_user, $db_password, $db_name);
        if($baza->connect_errno!=0)
    {
    throw new Exception(mysqli_connect_errno());
    } else 
        {
            $rezultat = $baza->query("select id_gracz from gracze where email='$email'");
            if(!$rezultat) throw new Exception($baza->error);

            $ile_emaili = $rezultat->num_rows;
            if($ile_emaili > 0)
            {
                $walidacja = false;
                $_SESSION['e_email']='<p style="color: red; font-size: 20px;">istnieje już konto przypisane do tego emaila</p>';
            }

            $rezultat = $baza->query("select id_gracz from gracze where login='$login'");
            if(!$rezultat) throw new Exception($baza->error);

            $ile_loginow = $rezultat->num_rows;
            if($ile_loginow > 0)
            {
                $walidacja = false;
                $_SESSION['e_login']='<p style="color: red; font-size: 20px;">istnieje już konto z takim loginem</p>';
            }

            if($walidacja == true)
    {
        if($baza->query("insert into gracze values (null, '$login', '$haslo_hash', '$email',1000)"))
        {
            $_SESSION['udana_rejestracja'] = true;
            header('location: witamy.php');
        }
        else
        {
            throw new Exception($baza->error);
        }
    }
    else 
    {
        header('location: index_rejestracja.php');
    }

            $baza->close();
        }   

    }catch(Exception $e)
    {
        echo'Błąd serwera ! Przepraszamy za niedogodności.';
    }

    
}
?>