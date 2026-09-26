advancement revoke @s only hub:use_menu
execute if score @s hub.cd matches 1.. run return 0
scoreboard players set @s hub.cd 10
dialog show @s hub:servers
