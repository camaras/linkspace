<?php
require_once($argv[1].'/wp-load.php');

$time = time();
$expire_time = $time + 360000;

$manager = WP_Session_Tokens::get_instance( 1 );
$token   = $manager->create( $expire_time );

$auth_cookie = wp_generate_auth_cookie(1, $expire_time, "secure_auth", $token);

print $auth_cookie;

?>
