<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "swarmintelligence";
 
 class User
 {
    public $ID;
    public $X;
    public $Y;
    public $Z;
    public $speed;
    public $pitch;
    public $roll;
    public $azimuth;
    public $time;
 }
// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} 
 
// $sql = "SELECT * FROM location JOIN (SELECT ";
$sql = "SELECT en.ID, en.X, en.Y,en.Z,en.speed,en.pitch,en.roll,en.azimuth,en.time FROM location en 
    JOIN (
        SElECT ID, max(time)up_time 
        FROM location 
        GROUP BY ID ORDER BY TIME DESC 
        ) tmp 
    ON en.ID = tmp.ID AND en.time = tmp.up_time";


$result = $conn->query($sql);
 


if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        $user = new User();
        $user->ID = $row["ID"];
        $user->X = $row["X"];
        $user->Y = $row["Y"];
        $user->Z = $row["Z"];
        $user->speed = $row["speed"];
        $user->pitch = $row["pitch"];
        $user->roll = $row["roll"];
        $user->azimuth = $row["azimuth"];
        $user->time = $row["time"];
        $data[] = $user;

    }
    echo json_encode($data);
} else {
    echo "0 结果";
}

$conn->close();
?>
