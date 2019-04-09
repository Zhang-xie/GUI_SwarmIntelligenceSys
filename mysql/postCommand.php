<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "swarmintelligence";

$commandID = isset($_POST['commandID']) ? htmlspecialchars($_POST['commandID']) : '';
$start_x = isset($_POST['start_x']) ? htmlspecialchars($_POST['start_x']) : '';
$start_y = isset($_POST['start_y']) ? htmlspecialchars($_POST['start_y']) : '';
$start_z = isset($_POST['start_z']) ? htmlspecialchars($_POST['start_z']) : '';
$end_x = isset($_POST['end_x']) ? htmlspecialchars($_POST['end_x']) : '';
$end_y = isset($_POST['end_y']) ? htmlspecialchars($_POST['end_y']) : '';
$end_z = isset($_POST['end_z']) ? htmlspecialchars($_POST['end_z']) : '';
$IDs = isset($_POST['IDs']) ? htmlspecialchars($_POST['IDs']) : '';


// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// 检测连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} 
 
$sql = "INSERT INTO `command` (`commandID`, `start_x`, `start_y`, `start_z`, `end_x`, `end_y`, `end_z`, `time`, `IDs`) VALUES ( $commandID, $start_x, $start_y, $start_z, $end_x, $end_y, $end_z, CURRENT_TIMESTAMP, $IDs)";
 
if ($conn->query($sql) === TRUE) {
    echo "新记录插入成功";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}
 
$conn->close();
?>
