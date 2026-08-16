"""
Raspberry Pi Pico - SX1262 LoRa Driver
Low-level driver for Semtech SX1262 module
"""

import machine
import time
from micropython import const

# SX1262 Pin Configuration
NSS_PIN = 5      # Chip Select
BUSY_PIN = 4     # Busy signal
DIO1_PIN = 3     # Interrupt
RESET_PIN = 2    # Reset
SCK_PIN = 18     # SPI Clock
MOSI_PIN = 19    # SPI MOSI
MISO_PIN = 16    # SPI MISO

# SX1262 Register Addresses
REG_SYNC_WORD_0 = 0x0740
REG_SYNC_WORD_1 = 0x0741
REG_PA_CONFIG = 0x0895
REG_TX_PARAMS = 0x08BB
REG_MODULATION_PARAMS = 0x8B
REG_PACKET_PARAMS = 0x8C
REG_CRC_POLY_0 = 0x08C7
REG_CRC_POLY_1 = 0x08C8

# SX1262 Commands
CMD_RESET = 0x09
CMD_SET_SLEEP = 0x84
CMD_SET_STANDBY = 0x80
CMD_SET_FS = 0xC1
CMD_SET_TX = 0x83
CMD_SET_RX = 0x82
CMD_READ_REGISTER = 0x1D
CMD_WRITE_REGISTER = 0x0D
CMD_WRITE_BUFFER = 0x0E
CMD_READ_BUFFER = 0x1E
CMD_GET_STATUS = 0xC0
CMD_IRQ_STATUS = 0x12
CMD_CLEAR_IRQ = 0x02


class SX1262:
    """
    Semtech SX1262 LoRa transceiver driver
    """
    
    def __init__(self):
        """
        Initialize SX1262 module
        """
        # Setup GPIO
        self.nss = machine.Pin(NSS_PIN, machine.Pin.OUT)
        self.busy = machine.Pin(BUSY_PIN, machine.Pin.IN)
        self.dio1 = machine.Pin(DIO1_PIN, machine.Pin.IN)
        self.reset = machine.Pin(RESET_PIN, machine.Pin.OUT)
        
        # Setup SPI
        self.spi = machine.SPI(
            1,
            baudrate=1000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=machine.SPI.MSB,
            sck=machine.Pin(SCK_PIN),
            mosi=machine.Pin(MOSI_PIN),
            miso=machine.Pin(MISO_PIN)
        )
        
        self.nss.on()  # NSS high (inactive)
        self.reset.on()
        self.tx_buffer = bytearray(256)
        self.rx_buffer = bytearray(256)
        self.packet_received = False
        
        # Initialize module
        self._reset()
        time.sleep(0.1)
        self._init_module()
    
    def _wait_busy(self, timeout=1000):
        """
        Wait for BUSY pin to go low
        """
        start = time.ticks_ms()
        while self.busy.value() and (time.ticks_ms() - start) < timeout:
            time.sleep(0.001)
    
    def _reset(self):
        """
        Reset the SX1262 module
        """
        self.reset.off()
        time.sleep(0.01)
        self.reset.on()
        time.sleep(0.05)
        self._wait_busy()
    
    def _spi_write(self, data):
        """
        Write data via SPI
        """
        self.nss.off()
        time.sleep(0.001)
        self.spi.write(data)
        time.sleep(0.001)
        self.nss.on()
        self._wait_busy()
    
    def _spi_read(self, length):
        """
        Read data via SPI
        """
        self.nss.off()
        time.sleep(0.001)
        data = self.spi.read(length)
        time.sleep(0.001)
        self.nss.on()
        self._wait_busy()
        return data
    
    def _init_module(self):
        """
        Initialize LoRa parameters
        """
        # Set to standby mode
        self._spi_write(bytes([CMD_SET_STANDBY, 0x00]))
        time.sleep(0.01)
        
        # Configure modulation (LoRa mode)
        self._spi_write(bytes([CMD_SET_FS]))
        time.sleep(0.01)
    
    def set_frequency(self, freq):
        """
        Set operating frequency
        """
        # Calculate frequency bytes
        frf = int((freq << 25) / 32000000)
        bytes_freq = bytes([
            (frf >> 16) & 0xFF,
            (frf >> 8) & 0xFF,
            frf & 0xFF
        ])
        
        cmd = bytes([CMD_WRITE_REGISTER, 0x06, 0xB8]) + bytes_freq
        self._spi_write(cmd)
    
    def send(self, data):
        """
        Send LoRa packet
        """
        # Write data to TX buffer
        cmd = bytes([CMD_WRITE_BUFFER, 0x00]) + data
        self._spi_write(cmd)
        
        # Set TX mode
        self._spi_write(bytes([CMD_SET_TX, 0x00, 0x00, 0x00]))
        time.sleep(0.1)
    
    def receive(self, timeout=5000):
        """
        Receive LoRa packet
        Returns: (data, rssi, snr) or None
        """
        # Set RX mode
        self._spi_write(bytes([CMD_SET_RX, 0xFF, 0xFF, 0xFF]))
        
        start = time.ticks_ms()
        while (time.ticks_ms() - start) < timeout:
            if self.dio1.value():
                # Packet received
                irq_status = self._spi_read(3)
                
                # Read packet
                cmd = bytes([CMD_READ_BUFFER, 0x00])
                packet = self._spi_read(257)
                
                # Clear IRQ
                self._spi_write(bytes([CMD_CLEAR_IRQ, 0xFF, 0xFF]))
                
                return packet[2:], 0, 0  # Simplified: return data only
            
            time.sleep(0.01)
        
        return None
    
    def get_rssi(self):
        """
        Get RSSI (signal strength)
        """
        return -120  # Placeholder
    
    def get_snr(self):
        """
        Get SNR (signal to noise ratio)
        """
        return 0  # Placeholder
