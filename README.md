# ME-405-NERF-Gun-Turret
Calpoly ME 405 Class term project in building a NERF gun turret that can auto-fire on a target
## Authors:
Sebastian Bessoudo, Nathaniel Davis
## Introduction
The goal of this project is to design an autonomous NERF gun turret that detects and tracks a target and fires a projectile. For the tournament, the launcher must turn 180 degrees with a motor and align itself using an infrared camera to face and hit the target within 10 seconds.  There must also be an emergency shutdown button that can be pushed or a red exposed wire that can be pulled  to stop the automation of the turret at any time. 
## Hardware Design
Our design comprises four wooden blocks supporting a slender 3D-printed component below a Lazy Susan. This Susan is linked to a laser-cut wooden piece equipped with a rail attachment for the NERF gun and an additional compartment designed to house the servo for trigger firing. The underside of the 3D-printed component securely fastens the front section of a DC motor (37d 50-70 encoder), while its tip connects to the laser-cut wooden piece, facilitating rotation of the upper system via the Lazy Susan mechanism. The rail attachment accommodates the NERF gun and also features a dedicated compartment for a torque servo motor positioned at a higher level to engage the trigger mechanism. Rubber bands are employed to secure all components in place to prevent the servo motor from dislodging. The wooden blocks, 3D-printed pieces, and the lower section of the Lazy Susan are firmly fastened together with screws, while the upper portion is assembled using nuts and bolts for added stability. Additionally, an 'L'-shaped metal prop away from the assembly to support the infrared camera in place.
### Assembly Drawing
![CAD_assembly_nerfgun](https://github.com/SebastianBessoudo/ME-405-NERF-Gun-Turret/assets/158110649/d03cb37d-e48a-47d4-a11a-a31d389f993b)
### Physical Design
![nerfgun_fullview](https://github.com/SebastianBessoudo/ME-405-NERF-Gun-Turret/assets/158110649/0ec6d961-f92d-474d-a493-f477a6092209)
![nerfgun_closeup](https://github.com/SebastianBessoudo/ME-405-NERF-Gun-Turret/assets/158110649/cdad0554-61df-45a7-9649-c126f3c83d9f)
## Software Design
The software for this project is a cooperative multitasking system that contains three tasks: a mastermind task, a motor control task, and a camera task.
The mastermind task in charge of running the main code instructs what the turret is supposed to do in its movement, alignment, triggering, and shooting of the projectile. It also configures the intertask variables ir_angle and motor_setpoint for the utilization of the other tasks.
The motor control task uses the intertask variable motor_setpoint to have the motor rotate in a certain direction and setpoint. It is used for moving the motor in the phase of turning the turret 180 degrees and its alignment toward the target. 
The camera task takes a snapshot from an infrared camera and prints a CSV image that shows numbers based on the intensity of the heat signature. It also reads the CSV image and computes ir_angle for the direction of the highest intensity (or numbers) for the alignment of the turret.

See a full description of our software and FSM and Task Diagram in the link to our repository: [ Github Page](https://sebastianbessoudo.github.io/ME-405-NERF-Gun-Turret/)
## Testing

