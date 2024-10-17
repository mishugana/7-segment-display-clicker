"""
7-Segment Display Selector

Author: Matt Sandler
Date: October 2024

Description:
This Python script allows users to interact with a 7-segment display by clicking
on its segments to toggle them on or off. The script supports multiple output formats
for the display values, such as binary, decimal, and customized segment codes.
Users can record values, clear them, and copy the recorded values to the clipboard.

License: MIT License
"""


import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("7-Segment Display Selector")

    # Create a canvas to draw the segments
    canvas = tk.Canvas(root, width=200, height=300)
    canvas.pack()

    # Define the coordinates for each segment
    segments = {
        'A': [(50, 20), (150, 20), (140, 30), (60, 30)],
        'B': [(150, 20), (160, 30), (160, 120), (150, 130), (140, 120), (140, 30)],
        'C': [(150, 140), (160, 150), (160, 240), (150, 250), (140, 240), (140, 150)],
        'D': [(50, 250), (150, 250), (140, 240), (60, 240)],
        'E': [(40, 140), (50, 150), (50, 240), (40, 250), (30, 240), (30, 150)],
        'F': [(40, 20), (50, 30), (50, 120), (40, 130), (30, 120), (30, 30)],
        'G': [(50, 130), (150, 130), (140, 140), (60, 140)],
    }

    # Store the canvas IDs and states of each segment
    segment_ids = {}
    segment_states = {key: False for key in segments.keys()}

    # List to store recorded values
    recorded_values = []

    # Output format options
    output_formats = [
        "ABCDEFG",
        "Binary (Cathode) (7bit)",
        "Binary (Anode) (7bit)",
        "Decimal (0-127)",
        "0123456 (A=0, B=1, ..., G=6)",
        "1234567 (A=1, B=2, ..., G=7)"
    ]

    # Default selected format
    selected_format = tk.StringVar(value=output_formats[0])

    # Function to toggle segment state
    def toggle_segment(event):
        for key, seg_id in segment_ids.items():
            if canvas.find_withtag('current')[0] == seg_id:
                # Toggle the segment state
                segment_states[key] = not segment_states[key]
                # Update the segment color
                color = 'red' if segment_states[key] else 'white'
                canvas.itemconfig(seg_id, fill=color)
                # Update the displayed value
                update_output()
                break

    # Draw the segments on the canvas
    for key, coords in segments.items():
        seg_id = canvas.create_polygon(coords, fill='white', outline='black', width=2)
        segment_ids[key] = seg_id
        canvas.tag_bind(seg_id, '<Button-1>', toggle_segment)

    # Function to get the current value based on the selected format
    def get_output_value():
        # Order of segments for the code
        order = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        # Create the segment code string
        binary_code = ''.join(['1' if segment_states[seg] else '0' for seg in order])
        binary_code = binary_code[::-1]  # Reverse the binary code
        format_choice = selected_format.get()
        if format_choice == "ABCDEFG":
            return ''.join([str(order[i]) if segment_states[order[i]] else '' for i in range(7)])
        if format_choice == "Binary (Cathode) (7bit)":
            # No changes needed for cathode binary
            return binary_code
        elif format_choice == "Binary (Anode) (7bit)":
            # Invert the binary code for anode (1 -> 0, 0 -> 1)
            anode_code = ''.join(['0' if bit == '1' else '1' for bit in binary_code])
            return anode_code
        elif format_choice == "Decimal (0-127)":
            return str(int(binary_code, 2))
        elif format_choice == "0123456 (A=0, B=1, ..., G=6)":
            return ''.join([str(i) if segment_states[order[i]] else '' for i in range(7)])
        elif format_choice == "1234567 (A=1, B=2, ..., G=7)":
            return ''.join([str(i + 1) if segment_states[order[i]] else '' for i in range(7)])

    # Label to display the current value
    output_label = tk.Label(root, text="Current Value: 0", font=("Helvetica", 16))
    output_label.pack(pady=10)

    # Function to update the output label
    def update_output():
        output_value = get_output_value()
        output_label.config(text=f"Current Value: {output_value}")

    # Function to record the current value and update the list
    def record_value():
        output_value = get_output_value()
        recorded_values.append(output_value)
        # Update the label showing the list of values
        values_label.config(text=f"Recorded Values: {recorded_values}")

    # Button to record the value
    record_button = tk.Button(root, text="Record Value", command=record_value)
    record_button.pack(pady=10)

    # Function to clear recorded values
    def clear_values():
        recorded_values.clear()
        values_label.config(text="Recorded Values: []")

    # Button to clear the recorded values
    clear_button = tk.Button(root, text="Clear Values", command=clear_values)
    clear_button.pack(pady=5)

    # Label to display the recorded values
    values_label = tk.Label(root, text="Recorded Values: []", font=("Helvetica", 12))
    values_label.pack(pady=10)

    # Dropdown menu for selecting output format
    format_menu = tk.OptionMenu(root, selected_format, *output_formats, command=lambda _: update_output())
    format_menu.pack(pady=10)

    # Function to copy current value to clipboard
    def copy_to_clipboard():
        root.clipboard_clear()
        formatted_values = []
        
        for value in recorded_values:
            # Check if the value is numeric (a decimal number)
            if value.isdigit():
                formatted_values.append(value)  # Leave it as is if it's a decimal
            else:
                formatted_values.append(f'"{value}"')  # Enclose in quotes if it's not a number
        
        # Join the formatted values into a single string and append to the clipboard
        root.clipboard_append("[" + ",".join(formatted_values) + "]")


    # Button to copy the current value to the clipboard
    copy_button = tk.Button(root, text="Copy values", command=copy_to_clipboard)
    copy_button.pack(pady=10)


    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
