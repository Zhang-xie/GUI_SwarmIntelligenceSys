<?php
$ID = isset($_POST['ID']) ? htmlspecialchars($_POST['ID']) : '';
// $ID = $_GET["ID"];
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
 
$sql = "SELECT * FROM location WHERE ID = $ID ORDER BY TIME DESC";
$result = $conn->query($sql);
 
if ($result->num_rows > 0) {
    // 输出数据
    // while($row = $result->fetch_assoc()) {//return all the data of the car
    // 	 echo json_encode($row);

    //     // echo "id: " . $row["ID"]. " X: " . $row["X"]. " Y " . $row["Y"]." Z: " . $row["Z"]. "<br>";
    // }
    $row = $result->fetch_assoc();//return the latest data of the car;
    echo json_encode($row);
} else {
    echo "0 结果";
}
$conn->close();
?>