<!-- <?php
// 定义变量并默认设置为空值
// $ID = $_GET["ID"]; 
// $ID = 211;

// $servername = "localhost";
// $username = "root";
// $password = "";
// $dbname = "swarmintelligence";

// $jason='';
// $data = array();

// class User 
// {
// 	public $ID;
// 	public $X;
// 	public $Y;
// 	public $Z;
// 	public $speed;
// 	public $pitch;
// 	public $roll;
// 	public $azimuth;
// 	public $time;
	
// }
// 创建连接
// $conn = new mysqli($servername, $username, $password, $dbname);
// 检测连接
// if ($conn->connect_error) {
//     die("连接失败: " . $conn->connect_error);
// } 
// mysqli_query($conn , "set names utf8");
 
// $sql = "SElECT X,Y,Z,speed,pitch,roll,azimuth,time FROM location WHERE ID=$ID ORDER BY TIME DESC";

// $sql = "SElECT * FROM location";

// $retval = mysqli_query( $conn, $sql );

// if(! $retval )
// {
//     die('无法读取数据: ' . mysqli_error($conn));
// }
// else {
// 	$row = $result->fetch_assoc();
// 	// $row = mysqli_fetch_array($result,MYSQLI_BOTH); //,MYSQL_ASSOC  MYSQLI_NUM
// 	$user = new User();

// 	$user->ID = $row["ID"];
//     $user->X = $row["X"];
//     $user->Y = $row["Y"];
//     $user->Z = $row["Z"];
//     $user->speed = $row["speed"];
//     $user->pitch = $row["pitch"];
//     $user->roll = $row["roll"];
//     $user->azimuth = $row["azimuth"];
//     $user->time = $row["time"];
// 	$data[]=$user;
// 	$json = json_encode($data);//把数据转换为JSON数据.
//     echo "{".'"user"'.":".$json."}";
// }
 
// $conn->close();

?> -->

<!-- 获取指定的ID的最新数据 -->


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