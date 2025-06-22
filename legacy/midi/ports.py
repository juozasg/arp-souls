import mido


# Global variables to store the current ports
_current_output_port = None
_current_input_port = None

def get_output_port() -> mido.ports.BaseOutput:
    assert _current_output_port is not None, "Output port not initialized"
    return _current_output_port

def get_input_port() -> mido.ports.BaseInput:
    assert _current_input_port is not None, "Input port not initialized"
    return _current_input_port

def open_midi_ports():
    global _current_output_port
    global _current_input_port
    # Open the specified MIDI output port
    out_port_name = 'Virtual Raw MIDI 6-0:VirMIDI 6-0 40:0'
    _current_output_port = open_midi_output_port(out_port_name)

    # Open the specified MIDI input port
    in_port_name = 'KeyLab mkII 61:KeyLab mkII 61 MIDI 32:0'
    _current_input_port = open_midi_input_port(in_port_name)

def close_midi_ports():
    if _current_output_port:
        # Close the port
        _current_output_port.close()
        print("MIDI output port closed")

    if _current_input_port:
        # Close the input port
        _current_input_port.close()
        print("MIDI input port closed")


def open_midi_output_port(port_name):
    try:
        output_port: mido.ports.BaseOutput = mido.open_output(port_name) # type: ignore
        print(f"Opened MIDI output port: {port_name}")
        return output_port
    except Exception as e:
        print(f"Error opening MIDI output port: {e}")
        return None


def open_midi_input_port(port_name):
    try:
        input_port: mido.ports.BaseInput = mido.open_input(port_name) # type: ignore
        print(f"Opened MIDI input port: {port_name}")
        return input_port
    except Exception as e:
        print(f"Error opening MIDI input port: {e}")
        return None


def list_midi_ports():
    input_ports = mido.get_input_names() # type: ignore
    output_ports = mido.get_output_names() # type: ignore

    print("Available MIDI Input Ports:")
    if input_ports:
        for i, port in enumerate(input_ports):
            print(f"  {i}: {port}")
    else:
        print("  None found")

    print("\nAvailable MIDI Output Ports:")
    if output_ports:
        for i, port in enumerate(output_ports):
            print(f"  {i}: {port}")
    else:
        print("  None found")

    return input_ports, output_ports
