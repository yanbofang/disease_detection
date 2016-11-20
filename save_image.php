<?php

$data = $_POST['image'];

list($type, $data) = explode(';', $data);
list(, $data)      = explode(',', $data);
$data = base64_decode($data);

file_put_contents('uploads/face.png', $data);

?>