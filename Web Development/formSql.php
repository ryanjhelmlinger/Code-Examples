<?php

//$numLetters = $_REQUEST["numL"]; //parse int
//$fileName = "words.txt";
//$lines = file($fileName);

//$file = fopen($fileName, 'r');

$name = $_GET["name"];
$email = $_GET["email"];
$phone = $_GET["phone"];
$zip = $_GET["zip"];
$city = $_GET["city"];
$state = $_GET["state"];
$brand = $_GET["brand"];

$name = mysql_real_escape_string($name);
$email = mysql_real_escape_string($email);
$phone = mysql_real_escape_string($phone);
$zip = mysql_real_escape_string($zip);
$city = mysql_real_escape_string($city);
$state = mysql_real_escape_string($state);
$brand = mysql_real_escape_string($brand);

$db = new PDO('sqlite:hockeySticks.db');
$db->exec("INSERT INTO sticks(NAME, EMAIL, PHONE, ZIP, CITY, STATE, BRAND) VALUES ('$name', '$email', '$phone', '$zip', '$city', '$state', '$brand';");
//$searchFile = file_get_contents($fileName);

//$pattern = "/^a.{5}$/m";
//$pattern = "/^".$let.".{".$len."}$/m";
//$numMatches = preg_match_all($pattern, $searchFile, $matches);

//$str = "";
//for ($i = 0; $i < $numMatches; ++$i) {
		//echo $numMatches[$i];
        //$a[] = $matches[$i];
//        $str .= $matches[0][$i]."<br>";
 //   }


print "<table border=1>";
 print "<tr><td>firstname</td><td>lastname</td><td>username</td><td>password</td><td>gender</td><td>country</td></tr>";
$result = $db->query('SELECT * FROM registered_users');
foreach($result as $row)
{
  print "<tr><td>".$row['NAME']."</td>";
  print "<td>".$row['EMAIL']."</td>";
  print "<td>".$row['PHONE']."</td>";
  print "<td>".$row['ZIP']."</td>";
  print "<td>".$row['CITY']."</td>";
  print "<td>".$row['STATE']."</td>";
  print "<td>".$row['BRAND']."</td>";
}
print "</table>";

$db = NULL;
}
catch(PDOException $e)
{
print 'Exception : ' .$e->getMessage();
}



///echo($str);
//echo implode(" ", $a);
?>