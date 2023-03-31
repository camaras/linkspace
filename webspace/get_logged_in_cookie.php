<?php
require_once($argv[1].'/wp-load.php');

$time = time();
$expire_time = $time + 3600;

$login_cookie = wp_generate_auth_cookie(1, $expire_time, 'logged_in');
print $login_cookie;

?>
