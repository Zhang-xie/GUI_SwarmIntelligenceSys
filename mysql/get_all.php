<!-- 获取每个ID下的最新数据 -->

<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "swarmintelligence";
 
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
    	 echo json_encode($row);

        // echo "id: " . $row["ID"]. " X: " . $row["X"]. " Y " . $row["Y"]." Z: " . $row["Z"]. "<br>";
    }
} else {
    echo "0 结果";
}
$conn->close();
?>