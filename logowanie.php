<?php

session_start();

require_once "connect.php";
mysqli_report(MYSQLI_REPORT_STRICT);
 
try
    {
        $baza = new mysqli($host, $db_user, $db_password, $db_name);
        if($baza->connect_errno!=0)
    {
    throw new Exception(mysqli_connect_errno());
    }
else
{
    $login = $_POST['login'];
    $haslo = $_POST['haslo'];

    $login = htmlentities($login, ENT_QUOTES);
                
                $data = date('Y-m-d H:i:s');
                $czas = time();

    if($rezultat = @$baza->query(
        sprintf("select * from gracze where login='%s'",
        mysqli_real_escape_string($baza,$login),
        mysqli_real_escape_string($baza,$haslo))))
    {   
        
        $ilu_userow = $rezultat->num_rows;
        if($ilu_userow>0)
        {
            $wiersz = $rezultat->fetch_assoc();

            if(password_verify($haslo, $wiersz['haslo']))
            {   
                $id = $wiersz['id_gracz'];

                $baza->query("insert into logowanie values (null, $id, '$data', $czas, 1)");

                $_SESSION['zalogowany'] = true;
                $_SESSION['id_gracz'] = $wiersz['id_gracz'];
                $_SESSION['login'] = $wiersz['login'];
                $_SESSION['elo'] = $wiersz['elo'];
                unset($_SESSION['zle_dane']);      
                $rezultat->close();
                header('location: lobby.php');
            }
            else {
                $id = $wiersz['id_gracz'];
                $baza->query("insert into logowanie values (null, $id, '$data', $czas, 0)");
                $_SESSION['zle_dane'] = '<p style="color: red; font-size: 20px;">nieprawidłowy login lub hasło<br><br></p>';
                header('location: index.php');
                }
        }else {
            $wiersz = $rezultat->fetch_assoc();
            $id = $wiersz['id_gracz'];
            $baza->query("insert into logowanie values (null, $id, '$data', $czas, 0)");
            $_SESSION['zle_dane'] = '<p style="color: red; font-size: 20px;">nieprawidłowy login lub hasło<br><br></p>';
            header('location: index.php');
              }   
    }

$baza->close();
}
}catch(Exception $e)
{
    echo'Błąd serwera ! Przepraszamy za niedogodności.'; exit();
}
?>