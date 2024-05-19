<?php


$input = json_decode(file_get_contents('php://input'), true);
if (!isset($input["code"])) {
    echo json_encode(array("error" => "no input data"));
    die();
}

$tmpfname = tempnam("/tmp", "lolpython_prog_");
$handle = fopen($tmpfname, "w");
fwrite($handle, $input["code"]);
fclose($handle);

$stdout = shell_exec("python2 /opt/lolcode.py $tmpfname");

echo(json_encode(array("result" => $stdout)));
?>