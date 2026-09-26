# Let every player use /trigger menu
scoreboard players enable @a hub.menu
execute as @a[scores={hub.menu=1..}] run function hub:trigger_menu

# Menu cooldown (prevents the dialog reopening every tick while the item is held)
scoreboard players remove @a[scores={hub.cd=1..}] hub.cd 1

# Give the item back after respawn (@e[type=player] only matches living players)
execute as @e[type=player,scores={hub.deaths=1..}] run function hub:respawn

# Menu items can't be dropped: remove any that end up on the ground
execute as @e[type=item] if items entity @s contents *[custom_data~{hub_menu:1b}] run kill @s
