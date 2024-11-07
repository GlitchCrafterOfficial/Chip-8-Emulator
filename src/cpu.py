import numpy as np
from src.screen import Screen
from src.ram import RAM
from src.keyboard import Keyboard

class CPU:
    def __init__(self, screen):
        self.memory = RAM()
        self.pc = 0x200
        self.sp = 0
        self.vx = 0
        self.vy = 0
        self.i = 0
        self.delay_timer = 0
        self.sound_timer = 0
        self.stack = []
        self.screen = screen
        self.keyboard = Keyboard()  # Instancia única de teclado
        
        self.register = np.zeros((16,), dtype=int).tolist()
        self.speed = 10

    def update_timer(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def process(self, byte):
        self.vx = (byte & 0x0F00) >> 8
        self.vy = (byte & 0x00F0) >> 4

        match byte & 0xF000:
            case 0x0000:
                match byte & 0x00FF:
                    case 0xE0:
                        self.screen.clear_display()
                    case 0xEE:
                        self.pc = self.stack.pop()
            case 0x1000:
                self.pc = byte & 0xFFF
                return
            case 0x2000:
                self.stack.append(self.pc)
                self.pc = byte & 0xFFF
                return
            case 0x3000:
                if self.register[self.vx] == byte & 0xFF:
                    self.pc += 2
            case 0x4000:
                if self.register[self.vx] != byte & 0xFF:
                    self.pc += 2
            case 0x5000:
                if self.register[self.vx] == self.register[self.vy]:
                    self.pc += 2
            case 0x6000:
                self.register[self.vx] = byte & 0xFF
            case 0x7000:
                self.register[self.vx] = (self.register[self.vx] + byte & 0xFF) & 0xFF
            case 0x8000:
                match byte & 0x000F:
                    case 0x0:
                        self.register[self.vx] = self.register[self.vy]
                    case 0x1:
                        self.register[self.vx] |= self.register[self.vy]
                    case 0x2:
                        self.register[self.vx] &= self.register[self.vy]
                    case 0x3:
                        self.register[self.vx] ^= self.register[self.vy]
                    case 0x4:
                        add = self.register[self.vx] + self.register[self.vy]
                        self.register[0xF] = int(add > 0xFF)
                        self.register[self.vx] = add & 0xFF
                    case 0x5:
                        self.register[0xF] = int(self.register[self.vx] > self.register[self.vy])
                        self.register[self.vx] = (self.register[self.vx] - self.register[self.vy]) & 0xFF
                    case 0x6:
                        self.register[0xF] = self.register[self.vx] & 1
                        self.register[self.vx] >>= 1
                    case 0x7:
                        self.register[0xF] = int(self.register[self.vy] > self.register[self.vx])
                        self.register[self.vx] = (self.register[self.vy] - self.register[self.vx]) & 0xFF
                    case 0xE:
                        self.register[0xF] = (self.register[self.vx] >> 7) & 1
                        self.register[self.vx] <<= 1
            case 0xA000:
                self.i = byte & 0xFFF
            case 0xB000:
                self.pc = (byte & 0xFFF) + self.register[0]
                return
            case 0xC000:
                self.register[self.vx] = np.random.randint(0, 256) & (byte & 0xFF)
            case 0xD000:
                w = 8
                h = byte & 0xF
                for row in range(h):
                    sprite = self.memory[self.i + row]
                    for col in range(w):
                        if sprite & (0x80 >> col):
                            x = (self.register[self.vx] + col) % self.screen.width
                            y = (self.register[self.vy] + row) % self.screen.height
                            if self.screen.draw_pixel(x, y):
                                self.register[0xF] = 1
            case 0xE000:
                match byte & 0xFF:
                    case 0x9E:
                        if self.keyboard.is_pressed(self.register[self.vx]):
                            self.pc += 2
                    case 0xA1:
                        if not self.keyboard.is_pressed(self.register[self.vx]):
                            self.pc += 2
            case 0xF000:
                match byte & 0xFF:
                    case 0x07:
                        self.register[self.vx] = self.delay_timer
                    case 0x0A:
                        self.register[self.vx] = self.keyboard.wait_for_keypress()
                    case 0x15:
                        self.delay_timer = self.register[self.vx]
                    case 0x18:
                        self.sound_timer = self.register[self.vx]
                    case 0x1E:
                        self.i += self.register[self.vx]
                    case 0x29:
                        self.i = self.register[self.vx] * 5
                    case 0x33:
                        self.memory[self.i] = self.register[self.vx] // 100
                        self.memory[self.i + 1] = (self.register[self.vx] % 100) // 10
                        self.memory[self.i + 2] = self.register[self.vx] % 10
                    case 0x55:
                        for j in range(self.vx + 1):
                            self.memory[self.i + j] = self.register[j]
                    case 0x65:
                        for j in range(self.vx + 1):
                            self.register[j] = self.memory[self.i + j]

    def cycle(self):
        for _ in range(self.speed):
            opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
            self.process(opcode)
            if not (opcode & 0xF000 in {0x1000, 0x2000, 0xB000}):
                self.pc += 2
