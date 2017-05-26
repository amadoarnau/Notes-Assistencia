<?php

/* TODO
- Coger grupos establecidos en un array.
- Hacer query de todos los grupos para sacar todos los miembros en un array total
- Hacer array unique para quitar repes.
- Sacar datos de contacto básicos de todos los UID que hay, y registrarlos en el Moodle.
- LDAP[uidNumber] = Moodle[idnumber], NO Moodle[id].

*/

//require 'LdapUtils.php';
require 'MoodleRest.php';

$config = require 'config.php';

//$moodle = new MoodleRest($config["url"], $config["token"]);
$url = "http://etldap.duhowpi.net";
$token = "8e645c89dca53418046b53a4124d1df5";

$moodle = new MoodleRest($url, $token);
$moodle->type("rest");

function user_exists($user, $field = "username"){
	global $moodle;

	$search = [
    	"field" => $field,
    	"values" => [$user]
    ];

    $res = $moodle->query("core_user_get_users_by_field", $search, "id");
    return $res;
}

$user = (user_exists("17179975059", "idnumber"));

if(count($user) != 1){ exit(); }

$user = $user[0];

$res = $moodle->query("core_course_get_contents", ["courseid" => 165]);

$acts = array();

foreach($res as $topic){
	foreach($topic->modules as $mod){
		$acts[$mod->id] = $mod->name;
	}
}

$res = $moodle->query("gradereport_user_get_grade_items", ["userid" => $user, "courseid" => 165]);

$grades = $res->usergrades[0]->gradeitems;

foreach($grades as $grade){
	echo $grade->percentageformatted ." , ";
	if(isset($acts[$grade->id])){
		echo $acts[$grade->id];
	}else{
		echo $grade->id;
	}
	echo "\n";
}

?>
