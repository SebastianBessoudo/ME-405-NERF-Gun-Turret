# ME-405-NERF-Gun-Turret
Calpoly ME 405 Class term project in building a NERF gun turret that can auto-fire on a target
## Authors:
Sebastian Bessoudo and Nathaniel Davis
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
Each test served as a preparatory phase for the final design. Initially, our focus was on testing the motor's ability to rotate to the designated setpoint upon button activation. We verified this by leveraging our encoder class to provide precise motor position feedback.

We then proceeded to evaluate the performance of the infrared camera using mlx_cam.py to ensure it captured the necessary images accurately. Upon confirmation, our attention shifted to assessing the camera's ability to capture multiple snapshots while concurrently coordinating with the motor through main.py.

Following successful tests on motor-camera coordination, we examined the system's ability to align the motor based on camera feedback and initiate the NERF gun projectile launch via servo motor triggering. Though most tests yielded positive results, we encountered challenges with the servo motor's functionality.

Specifically, we encountered difficulties with the MG995 servo motor, which proved unsuitable for our project due to several factors. These included its excessive current requirement of 1.2A, surpassing our project's 0.5A limit from the DC power supply, instances of unintended continuous rotation, and frequent overshooting of designated setpoints. These issues collectively hindered the servo motor's ability to reliably perform its intended function of pulling the NERF gun trigger.
## Lessons Learned and Final Recommendations
The primary takeaway from our project was the critical importance of careful electronics selection. The MG995 servo motor posed challenges because of its inability to consistently and accurately rotate to the designated setpoint. It also caused unexpected computer shutdowns when connected to the Nucleo during testing.

The issue stemmed from the servo motor attempting to draw excessive current from the computer while both were linked to the Nucleo. Consequently, whenever we executed the code, the computer repeatedly shut down. To avoid such complications in the future, it's essential to opt for either an alternative gear motor or a servo motor with the appropriate current requirements.

For instance, the HXT900 micro servo emerges as a promising alternative. It not only meets the project's current requirements but also offers reliability. Although it possesses lower torque compared to the MG995 servo motor, which is crucial for triggering the NERF gun, crafting a mechanism with the servo motor to engage the trigger remains a viable and potentially successful approach.
