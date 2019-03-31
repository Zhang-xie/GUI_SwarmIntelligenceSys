
<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "swarmintelligence";
 
// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// 检测连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} 
 
$sql = "INSERT INTO `command` (`commandID`, `start_x`, `start_y`, `start_z`, `end_x`, `end_y`, `end_z`, `time`, `IDs`) VALUES ('001', '1.2', '2.4', '22', '1.2', '12.', '12', CURRENT_TIMESTAMP, '1034')";
 
if ($conn->query($sql) === TRUE) {
    echo "新记录插入成功";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}
 
$conn->close();
?>
