# SpyWatch

## Inspiration
We were interested in the Symphonic Labs API and it's potential in audioless environments. As we were discussing potential uses, we got our hands on a Tello drone with full video streaming capabilities and realized that this drone has no audio. What kind of spy drone can't even peep in on your target's conversations? So we applied our idea of using the Symphonic Labs API in tandem with the Tello drone to create SpyWatch, a drone surveillance software that lets you easily and reliably listen in on conversations, without needing to actually listen!

## What it does
Spy on conversations using a live drone video feed and the Symphonic Labs lip reading technology.

## How we built it
- Python, Tello Drone SDK, Symphonic Labs API, WebSockets
- Connected to the Tello Drone using a command line application via the Tello Drone API
- Obtained and decoded the drone video stream using FFmpeg
- Directly saved and sent drone video data to the Symphonic API for AI lip reading

## Challenges we ran into
- Limitations with the drone hardware
   - The drone has difficulties supporting multiple connected input devices, so we couldn't simultaneously use the native phone application and run the computer program. We solved this by developing our own application for controlling the drone using the Tello Drone API directly in the command line
   - The drone connects to your computer through a Wi-Fi connection, but the Symphonic API call requires us to be connected to an active internet connection. We got around this by using an external USB Wi-Fi adapter to maintain two Wi-Fi connections on the same device simultaneously.

## Accomplishments that we're proud of
We determined that the Symphonic Labs lip reading AI technology is best suited for environments with poor audio conditions. We also quickly discovered that drones are extremely loud and thus have very poor audio quality. We are very proud of developing a software solution that solves both of these problems, and turns these weaknesses into strengths.

## What we learned
- Working with third party APIs and documentation
- Learned how to cleanly communicate with various platforms and APIs simultaneously
- Learned how to fly a drone (kind of)

## What's next for SpyWatch
- Interactive UI with fully interactive and easy-to-use drone controls
- Multiple lip reading streams to detect conversations between multiple people
- Live video stream for faster lip reading analysis

