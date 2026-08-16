"""
Raspberry Pi Pico - LoRa Mesh Configuration
Device configuration and constants
"""

import os

# Device Identification
DEVEUI = "0102030405060708"  # Unique device ID (8 bytes hex)
DEVICE_NAME = "LoRa-Pico-001"

# LoRa Configuration
LORA_FREQUENCY = 915000000  # 915 MHz in Hz
LORA_TX_POWER = 20  # dBm
LORA_BANDWIDTH = 125000  # 125 kHz
LORA_SPREADING_FACTOR = 7  # SF7-SF12
LORA_CODING_RATE = 5  # 4/5 to 4/8

# Server Configuration
SERVER_DEVEUI = "FFFFFFFFFFFFFFFF"  # Will be set from Android app
SERVER_ID = "server_main"  # Friendly name

# Mesh Protocol
MAX_HOPS = 10  # Maximum relay hops
MESH_TIMEOUT = 5000  # ms, timeout for mesh packet
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1000  # ms

# GPS Configuration
GPS_UPDATE_INTERVAL = 60000  # ms, send GPS every 60 seconds
GPS_UART = 0  # UART 0 for GPS data from Android via serial
GPS_BAUD = 9600

# Message Configuration
MAX_MESSAGE_LENGTH = 240  # bytes
MAX_NODES_IN_NETWORK = 100

# Bluetooth Configuration
BLE_NAME = "LoRa-Pico"
BLE_SERVICE_UUID = "12345678-1234-5678-1234-567812345678"
BLE_CHAR_RX = "12345678-1234-5678-1234-56781234567a"  # Receive from app
BLE_CHAR_TX = "12345678-1234-5678-1234-56781234567b"  # Send to app

# USB Serial Configuration
USB_BAUD = 115200

# Packet Types
PKT_TYPE_GPS = 0x01        # GPS location data
PKT_TYPE_MESSAGE = 0x02    # Text message
PKT_TYPE_ACK = 0x03        # Acknowledgment
PKT_TYPE_DISCOVER = 0x04   # Node discovery
PKT_TYPE_CONFIG = 0x05     # Configuration

# Storage
CONFIG_FILE = "/config.json"
