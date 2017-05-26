<?php
return [
    'url' => "http://etldap.duhowpi.net",
    'token' => "8e645c89dca53418046b53a4124d1df5",
    'debug' => FALSE,
    'student' => 5, // ID de rol de student.
    'teacher' => 3, // ID de rol de profe.
    'from' => "2017-09-21", // Fecha inicio matricula
    'to' => "2018-06-25", // Fecha final matricula

    'ldap' => [
        'host' => 'localhost',
        'user' => 'cn=admin,dc=ester,dc=cat',
        'password' => 'P@ssw0rd',
        'domain' => 'ester.cat',
    ],

    'mysql' => [
        'host' => 'localhost',
        'username' => 'root',
        'passwd' => '',
        'dbname' => 'django',
    ],
];

?>
