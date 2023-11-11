import time
import board
import neopixel

def wheel(pos):
    if pos < 128:
        return (255 - pos * 2, pos * 2, 0)
    else:
        pos -= 128
        return (0, 255 - pos * 2, pos * 2)

def rainbow_single_led(pixels, wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int((i * 256 / len(pixels)) + j)
            pixels[i] = wheel(idx & 255)
            pixels.show()  # Show the color on this LED
            time.sleep(wait)  # Wait before moving to the next LED

pixels = neopixel.NeoPixel(board.D18, 12)

try:
    while True:
        for i in range(len(pixels)):
            pixels.fill((0, 0, 0))  # Clear all LEDs
            pixels[i] = (255, 255, 255)  # Activate the current LED
            pixels.show()  # Show the LED activation
            time.sleep(0.1)  # Wait before moving to the next LED
            rainbow_single_led(pixels, 0.5)  # Apply rainbow effect
except KeyboardInterrupt:
    pixels.fill((0, 0, 0))
    pixels.show()
