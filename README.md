# Ship-Defenders
Ship Defenders is a crappy little game I made for a game jam between me and a friend of mine. This was made for learning, and, for fun.

The highest score I've ever gotten was 1055800, when I reached wave 51.

### Controls
W: Forward

A: Turn left

D: Turn right

SPACEBAR: Shoot bullets

E: Shoot missiles, if you have any

ESCAPE: Exit the game.


## GAME MECHANICS


### The Playable Space

The playable space is a large, open area. Any projectile or ship that goes beyond the boundaries of the map will apear on the opposite side of where they came through.

### The Player

![The Player](/images/ship_idle.png)  ![Bullet](/images/bullet.png)  ![Missile](/images/ship_missile.png) The player is a fast moving ship, that can shoot a large amount of bullets, and missiles, if the player has any. The player can obtain more missiles from their starting 3 missiles from powerups that appear randomly on the map.


### Waves

Every new wave will have an enemy count which is the same as the wave count. Example: Wave 6 will have 6 enemies.

A wave will only end when all enemies and enemy projectiles are dead. Any remaining allied ships will carry over to the next wave.

Every 3rd wave, an enemy missile boat will spawn. They have a firerate that's double the length of a regular enemy, but instead they shoot guided missiles that will target the nearest friendly ship.

Roughly every 4th wave, an allied ship will spawn. They're identical to enemy ships, except that ther're allies.

And roughly every 7th wave, an allied missile boat will spawn. They're identical to enemy missile boats, except they're allies and shoot allied missiles which target the nearest enemy.

The wave counter will slowly turn redder, and redder with each additional wave. Past wave 40, the counter does not become redder.

EXAMPLES:

Wave 6 will have 6 enemy ships, 2 enemy missile boats, and 1 allied ship.
Wave 12 wil have 12 enemy ships, 4 enemy missile boats, 3 allied ships, and 1 allied missile boat.


### Enemies and allies


**Enemy Ship**

![Enemy Ship](/images/ship_idle_enemy.png)  ![Enemy Bullet](/images/bullet_enemy.png) Your standard enemy ship. Every 2 seconds, they fire a fast moving red bullet. When said bullet comes in to contact with any friendly ship or projectile, it destroys itself and whatever it hit. They are easy to destroy, as 1 shot kills them instantly. They will spawn far away from the player, facing a random direction. Every enemy ship has a dark gray hull, and a red glass cockpit.

**Enemy Missile Boat (MB)**

![Enemy Missile Boat](/images/ship_enemy_mb.png)  ![Enemy Missile](/images/ship_missile_enemy.png) This enemy ship is twice as slow as a regular enemy. As the name suggests, they fire missiles instead of bullets. They have a fire rate that's twice as slow as regular enemy ships, which means they shoot every 4 seconds. The missiles they fire are fast, and faster than the player, but turn slowly. Use this to your advantage by out maneuvering their missiles! The missiles can be shot down with a precise shot, or until they die after 12 seconds of flying around. They have a bulky, fat appearence, with the same dark gray hull and red glass cockpit.

**Friendly Ship**

![Friendly Ship](/images/ship_idle_ally.png)  ![Bullet](/images/bullet.png) Allied ships will apear starting from wave 4. They will attack the nearest enemy, even if it means ramming in to them, which destroys them both. Their friendly projectiles do no damage to the player. Allied ships will spawn anywhere near the player, instead of far away from the player, but they will face a random direction. Other than being friendly, they are identical to their enemy counterparts. They have a light gray hull, and a lime green cockpit.

![Friendly Missile Boat](/images/ship_friendly_mb.png)  ![Missile](/images/ship_missile.png)
 Allied missile boats start appearing at wave 7, and onwards. They will attack the nearest enemy. They are identical in strength to their enemy counterparts, with the exception of being friendly and their projectiles being friendly. They are bulky, fat, and have a light gray hull, with a lime green cockpit.


### Powerups


![Powerup](/images/missile_powerup.png) Every 20 seconds in the game, a power up will spawn anywhere on the map, that is far away from the player. When it collides with the player, it will be picked up, and the player will receive 1 additional missile that they can use.


### Score


For every enemy ship that gets destroyed, the score counter will go up by 600. Any enemy missiles that are destroyed will add a score of 100 to the counter. 
