"""
main.py 
"""

from serial import Serial

END_OF_FILE_MARKER = b"\n__IMAGE_EOF__\n"


class USBConnection:
    def __init__(
        self,
        port: str,
        baudrate: int,
        destination_file: str ="frame_output.jpg",
        payload: bytearray = bytearray(),
    ):
        self.payload = payload
        self.port = port
        self.baudrate = baudrate

        # View frame
        # Temporary code to save a current frame
        self.destination_file_name = destination_file
        
        self.serial_connection = None
        self.chunk_data = None
        self.frame_data = None

    def open_connection(self):
        # only open a connection if there does not currently exist one.
        assert not self.serial_connection

        # Create Serial Connection
        self.serial_connection = Serial(port=self.port, baudrate=self.baudrate)

        # the first line is the header of the file set by the PICO
        header_line = (
            self.serial_connection
                .readline()
                .decode("utf-8", errors="replace")
                .strip()
        )
        print(f"Reported Pico Frame: {header_line}")
        
        

    def read_frame_data(self, byte_size:int = 1_000_000):
        """
        Function: read_frame_data
        This function handles the connection/read loop.
        The algorithm fetches data from the PICO,
        Extends the `self.payload` byte array,
        Terminates once the serial connection reads a b"EOF", which must be configured on the RasperryPI Pico
        ARGS: 
            byte_size: int, defaults to 1 Mbps, this simply sets the rate at which the USB cord will 
            fetch data provided by the PICO
        RETURN: Nothing
        """
        
        while True:
            self.chunk_data = self.serial_connection.read(byte_size)
            if not self.chunk_data:
                continue
            if self.chunk_data == b"EOF":
                break
            self.payload.extend(self.chunk_data)
            if self.payload.endswith(END_OF_FILE_MARKER):
                print("End of file marker received. Writing to file.")
                break
            print(f"Received {len(self.chunk_data)} bytes, total received: {len(self.payload)} bytes")

       
    def write_frame_data(self):
        """
        write_frame_data recieves the completed payload bytearray and sets `self.frame_data`
        and attempts to write the completed frame data to the temporary destination file 
        """
        
        self.file = open(self.destination_file_name, "wb")
        self.frame_data = self.payload[: -len(END_OF_FILE_MARKER)]


        soi_index = self.frame_data.find(b"\xff\xd8")
        if soi_index != -1:
            self.frame_data = self.frame_data[soi_index:]
        else:
            print("Warning: JPEG SOI marker (FF D8) not found! File may be invalid.")
        
        try:
            self.file.write(self.frame_data)
        except Exception as err:
            print(err)

    def clean_up(self):
        """
        Cleans up the payload byte array
        closes the file
        and closes the serial connection
        """
        
        self.file.close()
        self.serial_connection.close()
        self.payload.clear()




if __name__ == "__main__":
    # This is hardcoded and changes by Machine 
    # I recommend using Linux when developing in this Repo as the file system is easier to use 
    # CHANGE THIS TO MATCH THE PORT ON THE OUTPUT LAPTOP (CHECK README.md)
    port = "/dev/ttyACM0"
    
    payload = bytearray()
    
    # COULD BE MODIYFIED TO INCREASE TRANSFER SPEED
    baudrate = 115200
    
    
    usbcon: USBConnection = USBConnection(port=port, baudrate=baudrate, payload=payload)
    
    # Open Connection
    usbcon.open_connection()
    
    # Read from USB
    usbcon.read_frame_data()
    
    # Write frame data
    usbcon.write_frame_data()
    
    # Clean Up environment
    usbcon.clean_up()