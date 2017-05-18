<?php

$servername = "127.0.0.1";
$username = "django";
$password = "django";
//$username = "root";
//$password = "00051094-Aa";
$dbname = "django";

$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$xml = simplexml_load_file("prova.XML");
$xmlsaga = simplexml_load_file("dades-saga.xml");

//$cursos = array();
$num = 0;

foreach($xml->{'teachers'}->{'teacher'} as $profe){
    $id_profe = strval($profe['id']);
    
    $num++;

    if (($id_profe != "")||($profe->surname != "")||($profe->text != "")||($profe->teacher_department['id'] != "")) {
        $id_profe = sanstr($id_profe);
        $surname = sanstr($profe->surname);
        $text = sanstr($profe->text);
        $teacher_department_id = sanstr($profe->teacher_department['id']);
    }
    
    $sql = "INSERT INTO admincenter_files_professor (nom, departament_professor, professor_id_xml, text) VALUES ('".$surname."', '".$teacher_department_id."', '".$id_profe."', '".$text."')";

    if ($conn->query($sql) === TRUE) {
        echo "id_profes: ".$id_profe." / Nombre: ".$surname."\n";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
        echo "\n\n\n\n\n";
    }

}

foreach($xml->{'departments'}->{'department'} as $departments){
    $department = strval($departments['id']);
    

    if ($department != "") {
        $department = sanstr($department);
    }
    
    $sql = "INSERT INTO admincenter_files_department (nom) VALUES ('".$department."')";

    if ($conn->query($sql) === TRUE) {
        echo "Nom: ".$department."\n";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
        echo "\n\n\n\n\n";
    }

}

foreach($xml->{'rooms'}->{'room'} as $room){
    $id_room = strval($room['id']);
    $longname = strval($room->longname);
    

    if (($id_room != "")||($longname != "")) {
        $id_room = sanstr($id_room);
        $longname = sanstr($longname);
    }
    
    $sql = "INSERT INTO admincenter_files_room (id_xml, nom) VALUES ('".$id_room."', '".$longname."')";

    if ($conn->query($sql) === TRUE) {
        echo "Nom: ".$id_room."\n";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
        echo "\n\n\n\n\n";
    }

}

foreach($xml->{'classes'}->{'class'} as $class){
    $id_classe = strval($class['id']);
    $longname = strval($class->longname);
    $class_room = strval($class->class_room['id']);
    

    if (($id_classe != "")||($longname != "")||($class_room != "")) {
        $id_classe = sanstr($id_classe);
        $longname = sanstr($longname);
        $class_room = sanstr($class_room);
    }
    
    $sql = "INSERT INTO admincenter_files_classe (id_xml, nom, class_room) VALUES ('".$id_classe."', '".$longname."', '".$class_room."')";

    if ($conn->query($sql) === TRUE) {
        echo "Nom: ".$id_classe."\n";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
        echo "\n\n\n\n\n";
    }

}

foreach($xml->{'subjects'}->{'subject'} as $subject){
    $id_subject = strval($subject['id']);
    $longname = strval($subject->longname);
    $forecolor = strval($subject->forecolor);
    $backcolor = strval($subject->backcolor);
    

    if (($id_subject != "")||($longname != "")||($forecolor != "")||($backcolor != "")) {
        $id_subject = sanstr($id_subject);
        $longname = sanstr($longname);
        $forecolor = sanstr($forecolor);
        $backcolor = sanstr($backcolor);
    }
    
    $sql = "INSERT INTO admincenter_files_assignatura (id_xml, nom, forecolor, backcolor) VALUES ('".$id_subject."', '".$longname."', '".$forecolor."', '".$backcolor."')";

    if ($conn->query($sql) === TRUE) {
        echo "Nom: ".$id_subject."\n";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
        echo "\n\n\n\n\n";
    }

}

foreach($xml->{'lessons'}->{'lesson'} as $lesson){
    $id_lesson = strval($lesson['id']);
    $periods = strval($lesson->periods);
    $lesson_subject = strval($lesson->lesson_subject['id']);
    $lesson_teacher = strval($lesson->lesson_teacher['id']);
    $teacher_value = strval($lesson->teacher_value);
    $effectivebegindate = strval($lesson->effectivebegindate);
    $effectiveenddate = strval($lesson->effectiveenddate);

    if (($id_lesson != "")||($periods != "")||($lesson_subject != "")||($lesson_teacher != "")||($teacher_value != "")||($effectivebegindate != "")||($effectiveenddate != "")) {
        $id_lesson = sanstr($id_lesson);
        $periods = sanstr($periods);
        $lesson_subject = sanstr($lesson_subject);
        $lesson_teacher = sanstr($lesson_teacher);
        $teacher_value = sanstr($teacher_value);
        $effectivebegindate = sanstr($effectivebegindate);
        $effectiveenddate = sanstr($effectiveenddate);
    }

    //foreach($lesson->times->time as $time){
    //foreach($lesson->times as $times){
        foreach($lesson->times->time as $time){
            $assigned_day = strval($time->assigned_day);
            $assigned_period = strval($time->assigned_period);
            $assigned_starttime = strval($time->assigned_starttime);
            $assigned_endtime = strval($time->assigned_endtime);

            $num++;

            $sql = "INSERT INTO admincenter_files_llico (id_xml, periods, lesson_subject, lesson_teacher, teacher_value, effectivebegindate, effectiveenddate, assigned_day, assigned_period, assigned_starttime, assigned_endtime) VALUES ('".$id_lesson."', '".$periods."', '".$lesson_subject."', '".$lesson_teacher."','".$teacher_value."', '".$effectivebegindate."', '".$effectiveenddate."','".$assigned_day."', '".$assigned_period."', '".$assigned_starttime."', '".$assigned_endtime."')";

            if ($conn->query($sql) === TRUE) {
                echo "Nom: ".$id_lesson."\n";
            } else {
                echo "Error: " . $sql . "<br>" . $conn->error;
                echo "\n\n\n\n\n";
            }  
        }
}

foreach($xml->{'timeperiods'}->{'timeperiod'} as $timeperiod){
    $id_timeperiod = strval($timeperiod['id']);
    $day = strval($timeperiod->day);
    $period = strval($timeperiod->period);
    $starttime = strval($timeperiod->starttime);
    $endtime = strval($timeperiod->endtime);
    

    if (($id_timeperiod != "")||($day != "")||($period != "")||($starttime != "")||($endtime != "")) {
        $id_timeperiod = sanstr($id_timeperiod);
        $day = sanstr($day);
        $period = sanstr($period);
        $starttime = sanstr($starttime);
        $endtime = sanstr($endtime);
    }
    
    $sql = "INSERT INTO admincenter_files_horari (id_xml, day, period, starttime, endtime) VALUES ('".$id_timeperiod."', '".$day."', '".$period."', '".$starttime."', '".$endtime."')";

    if ($conn->query($sql) === TRUE) {
        echo "Nom: ".$id_timeperiod."\n";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
        echo "\n\n\n\n\n";
    }

}

foreach($xmlsaga->{'grups'}->{'grup'} as $grup){

    $id_grup = strval($grup['id']);
    $codi = strval($grup['codi']);
    $nom = strval($grup['nom']);
    $etapa = strval($grup['etapa']);
    $subetapa = strval($grup['subetapa']);
    $nivell = strval($grup['nivell']);
    $regim = strval($grup['regim']);

    foreach($grup->alumnes->alumne as $alumne){
        $id_alumne = strval($alumne['id']);
        $num++;

        //echo "id_grup: ".$id_grup." / codi: ".$codi." / Nom: ".$nom." / etapa: ".$etapa." / subetapa: ".$subetapa." / nivell: ".$nivell." / regim: ".$regim." / id_alumne: ".$id_alumne."\n\n";

        $sql = "INSERT INTO admincenter_files_alumne (id_grup, codi, nom, etapa, subetapa, nivell, regim, id_alumne) VALUES ('".$id_grup."','".$codi."', '".$nom."', '".$etapa."','".$subetapa."', '".$nivell."', '".$regim."', '".$id_alumne."')";
        if ($conn->query($sql) === TRUE) {
            echo "Nom: ".$id_alumne."\n";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
            echo "\n\n\n\n\n";
        }
    }

    /*$day = strval($timeperiod->day);
    $period = strval($timeperiod->period);
    $starttime = strval($timeperiod->starttime);
    $endtime = strval($timeperiod->endtime);*/
    

    
    
    

}

echo $num;

$conn->close();


function sanstr($text){
    $text = str_replace(["à", "è", "ò", "ù", "'"], ["a", "e", "o", "u", ""], $text);
    $text = str_replace(["À", "È", "Ò", "Ù"], ["A", "E", "O", "U"], $text);
    $text = str_replace(["á", "é", "í", "ó", "ú"], ["a", "e", "i", "o", "u"], $text);
    $text = str_replace(["Á", "É", "Í", "Ó", "Ú"], ["A", "E", "I", "O", "U"], $text);
    return $text;
}